from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render

from media_library.models import Episode, Media, Season


def home(request):
    latest_movies = Media.objects.filter(
        media_type="movie"
    ).order_by("-release_date")[:8]

    latest_series = Media.objects.filter(
        media_type="series"
    ).order_by("-release_date")[:8]

    latest_anime = Media.objects.filter(
        media_type="anime"
    ).order_by("-release_date")[:8]

    hero_item = (
        Media.objects
        .filter(is_featured=True)
        .first()
    )

    if hero_item is None:
        hero_item = (
            Media.objects
            .order_by("-release_date")
            .first()
        )

    context = {
        "latest_movies": latest_movies,
        "latest_series": latest_series,
        "latest_anime": latest_anime,
        "hero_item": hero_item,
    }

    return render(request, "pages/home.html", context)


def media_detail(request, slug):
    seasons_queryset = Season.objects.prefetch_related(
        Prefetch(
            "episodes",
            queryset=Episode.objects.order_by("episode_number"),
        )
    ).order_by("season_number")

    media = get_object_or_404(
        Media.objects
        .select_related()
        .prefetch_related(
            "genres",
            "actors",
            "directors",
            "countries",
            Prefetch("seasons", queryset=seasons_queryset),
            "reviews__user",
        ),
        slug=slug,
    )

    context = {
        "media": media,
        "seasons": media.seasons.all(),
        "reviews": media.reviews.all()[:6],
        "is_series": media.media_type == "series",
    }

    return render(request, "pages/media-detail.html", context)
