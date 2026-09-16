"""
URL configuration for config project.
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
from django.views.static import serve

from accounts.views import profile_view
from media_library.views import (
    anime_archive,
    animation_archive,
    genre_detail,
    home,
    media_detail,
    movies_archive,
    search,
    search_suggestions,
    series_archive,
    watch_view,
)

urlpatterns = [
    path("", home, name="home"),
    path("", include("interactions.urls")),
    path("movies/", movies_archive, name="movies_archive"),
    path("series/", series_archive, name="series_archive"),
    path("anime/", anime_archive, name="anime_archive"),
    path("animations/", animation_archive, name="animation_archive"),
    path("genre/<slug:slug>/", genre_detail, name="genre_detail"),
    path("search/", search, name="search"),
    path("search/suggestions/", search_suggestions, name="search_suggestions"),
    path("profile/", profile_view, name="profile"),
    path("media/<slug:slug>/", media_detail, name="media_detail"),
    path("watch/<slug:slug>/", watch_view, name="watch_view"),
    path("accounts/", include("accounts.urls")),
    path("admin/", admin.site.urls),
]

urlpatterns += [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
