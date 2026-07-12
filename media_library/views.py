from django.shortcuts import render

from media_library.models import Media


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