from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render

from interactions.forms import RatingForm, ReviewForm
from interactions.models import Favorite, Rating, Review, Watchlist
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
    approved_reviews_queryset = Review.objects.filter(
        is_approved=True
    ).select_related("user")

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
            Prefetch("reviews", queryset=approved_reviews_queryset),
        ),
        slug=slug,
    )

    is_favorite = False
    is_in_watchlist = False
    user_rating = None
    user_review = None

    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(
            user=request.user,
            media=media,
        ).exists()
        is_in_watchlist = Watchlist.objects.filter(
            user=request.user,
            media=media,
        ).exists()
        user_rating = Rating.objects.filter(
            user=request.user,
            media=media,
        ).first()
        user_review = Review.objects.filter(
            user=request.user,
            media=media,
        ).first()

    context = {
        "media": media,
        "seasons": media.seasons.all(),
        "reviews": media.reviews.all()[:6],
        "is_series": media.media_type == "series",
        "is_favorite": is_favorite,
        "is_in_watchlist": is_in_watchlist,
        "user_rating": user_rating,
        "user_review": user_review,
        "rating_form": RatingForm(
            initial={"score": user_rating.score if user_rating else None}
        ),
        "review_form": ReviewForm(instance=user_review),
    }

    return render(request, "pages/media-detail.html", context)
