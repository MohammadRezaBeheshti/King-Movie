import json
from decimal import Decimal, InvalidOperation
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.dateparse import parse_date
from django.utils.text import slugify

from media_library.models import (
    Actor,
    Country,
    Director,
    Episode,
    Genre,
    Media,
    MediaStatus,
    MediaType,
    Season,
)


MEDIA_TYPE_MAP = {
    "MOVIE": MediaType.MOVIE,
    "SERIES": MediaType.SERIES,
    "ANIME": MediaType.ANIME,
    "ANIMATION": MediaType.ANIMATION,
}

STATUS_MAP = {
    "RELEASED": MediaStatus.RELEASED,
    "UPCOMING": MediaStatus.UPCOMING,
    "ENDED": MediaStatus.ENDED,
    "CANCELED": MediaStatus.CANCELED,
    "CANCELLED": MediaStatus.CANCELED,
    # The dataset uses ONGOING for active shows. "released" is the closest
    # existing project status without changing models.
    "ONGOING": MediaStatus.RELEASED,
}

COUNTRY_CODE_MAP = {
    "USA": "USA",
    "UNITED STATES": "USA",
    "UK": "UK",
    "UNITED KINGDOM": "UK",
    "IRAN": "IRN",
    "JAPAN": "JPN",
    "CHINA": "CHN",
    "ITALY": "ITA",
    "SPAIN": "ESP",
    "NEW ZEALAND": "NZL",
    "WEST GERMANY": "DEU",
}


class Command(BaseCommand):
    help = "Import media, relations, seasons, and episodes from data/media_dataset.json."

    def handle(self, *args, **options):
        dataset_path = Path("data") / "media_dataset.json"
        if not dataset_path.exists():
            raise CommandError(
                f"Dataset file not found: {dataset_path}. "
                "Place your JSON at data/media_dataset.json."
            )

        payload = self.load_dataset(dataset_path)
        media_items = payload.get("media")
        if not isinstance(media_items, list):
            raise CommandError('Invalid JSON structure: expected top-level key "media" as a list.')

        counters = {
            "genres": 0,
            "actors": 0,
            "directors": 0,
            "countries": 0,
            "media_created": 0,
            "media_updated": 0,
            "seasons": 0,
            "episodes": 0,
            "errors": 0,
        }

        for index, item in enumerate(media_items, start=1):
            try:
                item_counters = {
                    "genres": 0,
                    "actors": 0,
                    "directors": 0,
                    "countries": 0,
                    "media_created": 0,
                    "media_updated": 0,
                    "seasons": 0,
                    "episodes": 0,
                }
                with transaction.atomic():
                    self.import_media_item(item, item_counters)
                self.merge_counters(counters, item_counters)
            except Exception as exc:
                counters["errors"] += 1
                identifier = item.get("slug") or item.get("title") or f"row {index}"
                self.stderr.write(self.style.ERROR(f"[{identifier}] {exc}"))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Import finished."))
        self.stdout.write(f"Imported genres: {counters['genres']}")
        self.stdout.write(f"Imported actors: {counters['actors']}")
        self.stdout.write(f"Imported directors: {counters['directors']}")
        self.stdout.write(f"Imported countries: {counters['countries']}")
        self.stdout.write(
            f"Imported media: {counters['media_created'] + counters['media_updated']}"
        )
        self.stdout.write(f"Created media: {counters['media_created']}")
        self.stdout.write(f"Updated media: {counters['media_updated']}")
        self.stdout.write(f"Imported seasons: {counters['seasons']}")
        self.stdout.write(f"Imported episodes: {counters['episodes']}")
        if counters["errors"]:
            self.stdout.write(self.style.WARNING(f"Errors: {counters['errors']}"))

    def load_dataset(self, dataset_path):
        try:
            return json.loads(dataset_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise CommandError(f"Invalid JSON in {dataset_path}: {exc}") from exc

    def merge_counters(self, counters, item_counters):
        for key, value in item_counters.items():
            counters[key] += value

    def import_media_item(self, item, counters):
        if not isinstance(item, dict):
            raise ValueError("Each media item must be a JSON object.")

        slug = self.resolve_slug(item)
        media_defaults = self.build_media_defaults(item)
        media, created = Media.objects.update_or_create(
            slug=slug,
            defaults=media_defaults,
        )

        counters["media_created" if created else "media_updated"] += 1

        media.genres.set(self.resolve_genres(item.get("genres"), counters))
        media.actors.set(self.resolve_actors(item.get("actors"), counters))
        media.directors.set(self.resolve_directors(item.get("directors"), counters))
        media.countries.set(self.resolve_countries(item.get("countries"), counters))

        if media.media_type in {MediaType.SERIES, MediaType.ANIME, MediaType.ANIMATION}:
            self.import_seasons(media, item.get("seasons"), counters)

    def build_media_defaults(self, item):
        return {
            "title": self.clean_text(item.get("title")) or self.clean_text(item.get("original_title")) or "بدون عنوان",
            "persian_title": self.clean_text(item.get("persian_title")) or "",
            "original_title": self.clean_text(item.get("original_title")) or "",
            "media_type": self.normalize_media_type(item.get("media_type")),
            "status": self.normalize_status(item.get("status")),
            "overview": self.clean_text(item.get("overview")) or "",
            "release_date": self.parse_optional_date(item.get("release_date")),
            "runtime": self.parse_optional_int(item.get("runtime")),
            "imdb_rating": self.parse_optional_decimal(item.get("imdb_rating")),
            "trailer": self.clean_text(item.get("trailer")) or "",
        }

    def resolve_slug(self, item):
        slug = self.clean_text(item.get("slug"))
        if slug:
            return slug

        base_text = (
            self.clean_text(item.get("title"))
            or self.clean_text(item.get("original_title"))
            or self.clean_text(item.get("persian_title"))
        )
        generated_slug = slugify(base_text or "", allow_unicode=False)
        if generated_slug:
            return generated_slug

        raise ValueError("Missing slug and no usable title for slug generation.")

    def resolve_genres(self, genre_names, counters):
        genres = []
        for name in self.clean_string_list(genre_names):
            genre, created = Genre.objects.get_or_create(
                slug=slugify(name, allow_unicode=True),
                defaults={"name": name},
            )
            if not created and genre.name != name:
                genre.name = name
                genre.save(update_fields=["name"])
            if created:
                counters["genres"] += 1
            genres.append(genre)
        return genres

    def resolve_actors(self, actor_names, counters):
        actors = []
        for full_name in self.clean_string_list(actor_names):
            actor, created = Actor.objects.get_or_create(full_name=full_name)
            if created:
                counters["actors"] += 1
            actors.append(actor)
        return actors

    def resolve_directors(self, director_names, counters):
        directors = []
        for full_name in self.clean_string_list(director_names):
            director, created = Director.objects.get_or_create(full_name=full_name)
            if created:
                counters["directors"] += 1
            directors.append(director)
        return directors

    def resolve_countries(self, country_values, counters):
        countries = []
        for raw_value in self.clean_string_list(country_values):
            country_name = raw_value
            country_code = self.resolve_country_code(country_name)

            country, created = Country.objects.get_or_create(
                code=country_code,
                defaults={"name": country_name},
            )

            if not created and country.name != country_name:
                country.name = country_name
                country.save(update_fields=["name"])

            if created:
                counters["countries"] += 1
            countries.append(country)
        return countries

    def import_seasons(self, media, seasons_payload, counters):
        if not isinstance(seasons_payload, list):
            return

        for season_item in seasons_payload:
            if not isinstance(season_item, dict):
                continue

            season_number = self.parse_optional_int(season_item.get("season_number"))
            if season_number is None:
                continue

            season, created = Season.objects.get_or_create(
                media=media,
                season_number=season_number,
            )
            if created:
                counters["seasons"] += 1

            episodes_payload = season_item.get("episodes")
            if not isinstance(episodes_payload, list):
                continue

            for episode_item in episodes_payload:
                if not isinstance(episode_item, dict):
                    continue

                episode_number = self.parse_optional_int(episode_item.get("episode_number"))
                if episode_number is None:
                    continue

                default_title = f"قسمت {episode_number}"
                _, episode_created = Episode.objects.update_or_create(
                    season=season,
                    episode_number=episode_number,
                    defaults={
                        "title": self.clean_text(episode_item.get("title")) or default_title,
                        "runtime": self.parse_optional_int(episode_item.get("runtime")),
                        "release_date": self.parse_optional_date(episode_item.get("release_date")),
                    },
                )
                if episode_created:
                    counters["episodes"] += 1

    def normalize_media_type(self, raw_value):
        if raw_value is None:
            return MediaType.MOVIE

        normalized = MEDIA_TYPE_MAP.get(str(raw_value).strip().upper())
        return normalized or MediaType.MOVIE

    def normalize_status(self, raw_value):
        if raw_value is None:
            return MediaStatus.RELEASED

        normalized = STATUS_MAP.get(str(raw_value).strip().upper())
        return normalized or MediaStatus.RELEASED

    def resolve_country_code(self, country_name):
        normalized_name = self.clean_text(country_name).upper()
        mapped_code = COUNTRY_CODE_MAP.get(normalized_name)
        if mapped_code:
            return mapped_code

        compact_name = normalized_name.replace(".", "").replace("-", " ")
        pieces = [piece for piece in compact_name.split() if piece]
        if len(pieces) > 1:
            base_code = "".join(piece[0] for piece in pieces)[:3]
        else:
            letters_only = "".join(ch for ch in compact_name if ch.isalpha())
            base_code = (letters_only[:3] or "CTR").upper()

        base_code = base_code.ljust(3, "X")[:3]
        return self.ensure_unique_country_code(base_code, country_name)

    def ensure_unique_country_code(self, code, country_name):
        existing = Country.objects.filter(code=code).first()
        if existing is None or existing.name == country_name:
            return code

        for suffix in "123456789":
            candidate = f"{code[:2]}{suffix}"
            existing = Country.objects.filter(code=candidate).first()
            if existing is None or existing.name == country_name:
                return candidate

        raise ValueError(f"Could not generate unique country code for {country_name!r}.")

    def clean_string_list(self, values):
        if not isinstance(values, list):
            return []

        cleaned = []
        seen = set()
        for value in values:
            text = self.clean_text(value)
            if not text:
                continue
            key = text.casefold()
            if key in seen:
                continue
            seen.add(key)
            cleaned.append(text)
        return cleaned

    def clean_text(self, value):
        if value is None:
            return ""
        return str(value).strip()

    def parse_optional_int(self, value):
        if value in (None, ""):
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    def parse_optional_decimal(self, value):
        if value in (None, ""):
            return None
        try:
            return Decimal(str(value))
        except (InvalidOperation, TypeError, ValueError):
            return None

    def parse_optional_date(self, value):
        if not value:
            return None
        return parse_date(str(value))
