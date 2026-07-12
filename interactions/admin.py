from django.contrib import admin

from .models import Favorite, Rating, Review, Watchlist


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "media", "created_at")
    search_fields = ("user__username", "media__title", "media__persian_title")
    list_filter = ("created_at", "media__media_type")
    ordering = ("-created_at",)
    autocomplete_fields = ("user", "media")


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("user", "media", "created_at")
    search_fields = ("user__username", "media__title", "media__persian_title")
    list_filter = ("created_at", "media__media_type")
    ordering = ("-created_at",)
    autocomplete_fields = ("user", "media")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("user", "media", "score", "created_at", "updated_at")
    search_fields = ("user__username", "media__title", "media__persian_title")
    list_filter = ("score", "created_at", "updated_at", "media__media_type")
    ordering = ("-updated_at",)
    autocomplete_fields = ("user", "media")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "media", "is_approved", "created_at", "updated_at")
    search_fields = ("user__username", "media__title", "media__persian_title", "content")
    list_filter = ("is_approved", "created_at", "updated_at", "media__media_type")
    ordering = ("-created_at",)
    autocomplete_fields = ("user", "media")
    list_editable = ("is_approved",)
