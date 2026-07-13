from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand

from media_library.models import (
    Actor,
    Country,
    Director,
    Genre,
    Media,
    MediaStatus,
    MediaType,
    Season,
    Episode,
)


class Command(BaseCommand):
    help = "Create sample King Movie media records for development and admin testing."

    def handle(self, *args, **options):
        genres = self.create_genres()
        actors = self.create_actors()
        directors = self.create_directors()
        countries = self.create_countries()

        movie = self.create_media(
            slug="sample-movie-pars",
            title="The Last Frame",
            persian_title="آخرین قاب",
            original_title="The Last Frame",
            media_type=MediaType.MOVIE,
            status=MediaStatus.RELEASED,
            overview="یک فیلم درام معمایی درباره کارگردانی که گذشته خود را در یک حلقه فیلم پیدا می‌کند.",
            release_date=date(2024, 3, 14),
            runtime=118,
            imdb_rating=Decimal("7.8"),
            genres=[genres["drama"], genres["mystery"]],
            actors=[actors["navid"], actors["sara"]],
            directors=[directors["asghar"]],
            countries=[countries["ir"]],
            is_featured=True,
        )

        series = self.create_media(
            slug="sample-series-shadow-city",
            title="Shadow City",
            persian_title="شهر سایه‌ها",
            original_title="Shadow City",
            media_type=MediaType.SERIES,
            status=MediaStatus.RELEASED,
            overview="یک سریال جنایی شهری با پرونده‌های پیوسته و شخصیت‌های چندلایه.",
            release_date=date(2023, 9, 22),
            runtime=50,
            imdb_rating=Decimal("8.3"),
            genres=[genres["crime"], genres["drama"]],
            actors=[actors["peyman"], actors["sara"]],
            directors=[directors["narges"]],
            countries=[countries["ir"]],
        )
        self.create_episodes(
            series,
            {
                1: [
                    ("رد پا", 48, date(2023, 9, 22)),
                    ("پرونده باز", 51, date(2023, 9, 29)),
                    ("نقطه کور", 49, date(2023, 10, 6)),
                ],
                2: [
                    ("بازگشت", 52, date(2024, 5, 3)),
                    ("شب طولانی", 50, date(2024, 5, 10)),
                ],
            },
        )

        anime = self.create_media(
            slug="sample-anime-sky-garden",
            title="Sky Garden",
            persian_title="باغ آسمان",
            original_title="Sora no Niwa",
            media_type=MediaType.ANIME,
            status=MediaStatus.ENDED,
            overview="انیمه‌ای فانتزی درباره نوجوانی که باید راز باغی شناور را کشف کند.",
            release_date=date(2022, 4, 8),
            runtime=24,
            imdb_rating=Decimal("8.6"),
            genres=[genres["fantasy"], genres["animation"]],
            actors=[actors["mina"], actors["navid"]],
            directors=[directors["kenji"]],
            countries=[countries["jp"]],
        )
        self.create_episodes(
            anime,
            {
                1: [
                    ("دروازه ابرها", 24, date(2022, 4, 8)),
                    ("بذر نور", 24, date(2022, 4, 15)),
                    ("باد شمالی", 24, date(2022, 4, 22)),
                ],
            },
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Sample data ready: {movie}, {series}, {anime}"
            )
        )

    def create_genres(self):
        rows = [
            ("drama", "درام"),
            ("mystery", "معمایی"),
            ("crime", "جنایی"),
            ("fantasy", "فانتزی"),
            ("animation", "انیمیشن"),
        ]

        genres = {}

        for slug, name in rows:
            genre, _ = Genre.objects.update_or_create(
                name=name,
                defaults={
                    "slug": slug,
                },
            )

            genres[slug] = genre

        return genres

    def create_actors(self):
        names = {
            "navid": "نوید محمدزاده",
            "sara": "سارا بهرامی",
            "peyman": "پیمان معادی",
            "mina": "مینا ساداتی",
        }
        return {
            key: Actor.objects.update_or_create(
                full_name=name,
                defaults={},
            )[0]
            for key, name in names.items()
        }

    def create_directors(self):
        names = {
            "asghar": "اصغر فرهادی",
            "narges": "نرگس آبیار",
            "kenji": "کنجی ناکامورا",
        }
        return {
            key: Director.objects.update_or_create(
                full_name=name,
                defaults={},
            )[0]
            for key, name in names.items()
        }

    def create_countries(self):
        rows = {
            "ir": ("ایران", "IR"),
            "jp": ("ژاپن", "JP"),
            "us": ("آمریکا", "US"),
        }
        return {
            key: Country.objects.update_or_create(
                code=code,
                defaults={"name": name},
            )[0]
            for key, (name, code) in rows.items()
        }

    def create_media(
        self,
        slug,
        title,
        persian_title,
        original_title,
        media_type,
        status,
        overview,
        release_date,
        runtime,
        imdb_rating,
        genres,
        actors,
        directors,
        countries,
        is_featured=False,
    ):
        media, _ = Media.objects.update_or_create(
            slug=slug,
            defaults={
                "title": title,
                "persian_title": persian_title,
                "original_title": original_title,
                "media_type": media_type,
                "status": status,
                "overview": overview,
                "release_date": release_date,
                "runtime": runtime,
                "imdb_rating": imdb_rating,
                "is_featured": is_featured,
            },
        )
        media.genres.set(genres)
        media.actors.set(actors)
        media.directors.set(directors)
        media.countries.set(countries)
        return media

    def create_episodes(self, media, seasons):
        for season_number, episodes in seasons.items():
            season, _ = Season.objects.update_or_create(
                media=media,
                season_number=season_number,
                defaults={},
            )
            for episode_number, (title, runtime, release_date) in enumerate(episodes, start=1):
                Episode.objects.update_or_create(
                    season=season,
                    episode_number=episode_number,
                    defaults={
                        "title": title,
                        "runtime": runtime,
                        "release_date": release_date,
                    },
                )
