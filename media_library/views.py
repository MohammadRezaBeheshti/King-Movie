from django.core.paginator import Paginator
from django.db.models import Prefetch, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from interactions.forms import RatingForm, ReviewForm
from interactions.models import Favorite, Rating, Review, Watchlist
from media_library.forms import SearchForm
from media_library.models import Actor, Country, Director, Episode, Genre, Media, MediaStatus, MediaType, Season


SEARCH_SORT_CHOICES = [
    ("-release_date", "جدیدترین"),
    ("release_date", "قدیمی‌ترین"),
    ("-imdb_rating", "بالاترین امتیاز IMDb"),
    ("persian_title", "عنوان فارسی"),
]


def get_search_filter_choices():
    return {
        "media_types": [("", "همه نوع‌ها"), *MediaType.choices],
        "genres": [("", "همه ژانرها"), *[(genre.slug, genre.name) for genre in Genre.objects.all()]],
        "countries": [("", "همه کشورها"), *[(country.code, country.name) for country in Country.objects.all()]],
        "statuses": [("", "همه وضعیت‌ها"), *MediaStatus.choices],
        "directors": [("", "همه کارگردان‌ها"), *[(str(director.id), director.full_name) for director in Director.objects.all()]],
        "actors": [("", "همه بازیگران"), *[(str(actor.id), actor.full_name) for actor in Actor.objects.all()]],
        "sorts": SEARCH_SORT_CHOICES,
    }


def get_optimized_media_queryset():
    return Media.objects.select_related().prefetch_related(
        "genres",
        "actors",
        "directors",
        "countries",
    )


def get_media_archive_queryset():
    return Media.objects.select_related().prefetch_related(
        "genres",
    ).order_by("-release_date", "persian_title", "title")


def enrich_media_items(media_items):
    for media in media_items:
        genres = list(media.genres.all())
        media.primary_genre = genres[0] if genres else None
    return media_items


def render_media_archive(request, media_type, title, eyebrow, empty_message):
    media_items = enrich_media_items(
        list(get_media_archive_queryset().filter(media_type=media_type))
    )
    context = {
        "page_title": title,
        "page_eyebrow": eyebrow,
        "media_items": media_items,
        "empty_message": empty_message,
    }
    return render(request, "pages/archive/media-list.html", context)


def apply_media_search_filters(queryset, form):
    if not form.is_valid():
        return queryset.none()

    data = form.cleaned_data
    query = data.get("q")

    if query:
        queryset = queryset.filter(
            Q(persian_title__icontains=query)
            | Q(original_title__icontains=query)
            | Q(title__icontains=query)
        )

    if data.get("type"):
        queryset = queryset.filter(media_type=data["type"])

    if data.get("genre"):
        queryset = queryset.filter(genres__slug=data["genre"])

    if data.get("country"):
        queryset = queryset.filter(countries__code=data["country"])

    if data.get("year_from"):
        queryset = queryset.filter(release_date__year__gte=data["year_from"])

    if data.get("year_to"):
        queryset = queryset.filter(release_date__year__lte=data["year_to"])

    if data.get("rating"):
        queryset = queryset.filter(imdb_rating__gte=data["rating"])

    if data.get("status"):
        queryset = queryset.filter(status=data["status"])

    if data.get("director"):
        queryset = queryset.filter(directors__id=data["director"])

    if data.get("actor"):
        queryset = queryset.filter(actors__id=data["actor"])

    sort = data.get("sort") or "-release_date"
    allowed_sorts = {value for value, _ in SEARCH_SORT_CHOICES}
    if sort not in allowed_sorts:
        sort = "-release_date"

    return queryset.distinct().order_by(sort)


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

    featured_media = list(
        Media.objects.filter(is_featured=True)
        .prefetch_related("genres")
        .order_by("-release_date", "-updated_at")[:6]
    )

    if not featured_media:
        fallback_item = (
            Media.objects
            .prefetch_related("genres")
            .order_by("-release_date", "-updated_at")
            .first()
        )
        if fallback_item is not None:
            featured_media = [fallback_item]

    top_rated = Media.objects.filter(imdb_rating__isnull=False).order_by("-imdb_rating")[:8]

    context = {
        "latest_movies": latest_movies,
        "latest_series": latest_series,
        "latest_anime": latest_anime,
        "featured_media": featured_media,
        "top_rated": top_rated,
        "search_form": SearchForm(filter_choices=get_search_filter_choices()),
    }

    return render(request, "pages/home.html", context)


def movies_archive(request):
    return render_media_archive(
        request=request,
        media_type=MediaType.MOVIE,
        title="آرشیو فیلم‌ها",
        eyebrow="Movies",
        empty_message="فیلمی برای نمایش وجود ندارد.",
    )


def series_archive(request):
    return render_media_archive(
        request=request,
        media_type=MediaType.SERIES,
        title="آرشیو سریال‌ها",
        eyebrow="Series",
        empty_message="سریالی برای نمایش وجود ندارد.",
    )


def anime_archive(request):
    return render_media_archive(
        request=request,
        media_type=MediaType.ANIME,
        title="آرشیو انیمه",
        eyebrow="Anime",
        empty_message="انیمه‌ای برای نمایش وجود ندارد.",
    )


def animation_archive(request):
    return render_media_archive(
        request=request,
        media_type=MediaType.ANIMATION,
        title="آرشیو انیمیشن‌ها",
        eyebrow="Animations",
        empty_message="انیمیشنی برای نمایش وجود ندارد.",
    )


def genre_detail(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    media_items = enrich_media_items(
        list(get_media_archive_queryset().filter(genres__slug=slug).distinct())
    )
    context = {
        "genre": genre,
        "page_title": f"ژانر {genre.name}",
        "page_eyebrow": "Genre",
        "media_items": media_items,
        "empty_message": f"موردی برای ژانر «{genre.name}» پیدا نشد.",
    }
    return render(request, "pages/archive/genre-detail.html", context)


def search_suggestions(request):
    query = request.GET.get("q", "").strip()

    if len(query) < 2:
        return JsonResponse({"results": []})

    results = (
        get_optimized_media_queryset()
        .filter(
            Q(persian_title__icontains=query)
            | Q(original_title__icontains=query)
            | Q(title__icontains=query)
        )
        .order_by("-release_date")[:8]
    )

    payload = []
    for media in results:
        payload.append({
            "title": media.persian_title or media.title,
            "original_title": media.original_title,
            "year": media.release_date.year if media.release_date else "",
            "type": media.get_media_type_display(),
            "rating": str(media.imdb_rating) if media.imdb_rating else "",
            "poster": media.poster.url if media.poster else "",
            "url": f"/media/{media.slug}/",
        })

    return JsonResponse({"results": payload})


def search(request):
    filter_choices = get_search_filter_choices()
    form = SearchForm(request.GET, filter_choices=filter_choices)
    queryset = apply_media_search_filters(get_optimized_media_queryset(), form)

    paginator = Paginator(queryset, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    query_params = request.GET.copy()
    query_params.pop("page", None)

    applied_filters = []
    if form.is_valid():
        for field_name, label in [
            ("q", "جستجو"),
            ("type", "نوع"),
            ("genre", "ژانر"),
            ("country", "کشور"),
            ("year_from", "از سال"),
            ("year_to", "تا سال"),
            ("rating", "حداقل امتیاز"),
            ("status", "وضعیت"),
            ("director", "کارگردان"),
            ("actor", "بازیگر"),
            ("sort", "مرتب‌سازی"),
        ]:
            value = form.cleaned_data.get(field_name)
            if value:
                display_value = dict(form.fields[field_name].choices).get(value, value) if hasattr(form.fields[field_name], "choices") else value
                applied_filters.append({"label": label, "value": display_value})

    context = {
        "search_form": form,
        "page_obj": page_obj,
        "results": page_obj.object_list,
        "applied_filters": applied_filters,
        "total_results": paginator.count,
        "pagination_query": query_params.urlencode(),
    }

    return render(request, "pages/search.html", context)


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
