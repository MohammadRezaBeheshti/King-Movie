from django.contrib import admin

from .models import (
    Actor,
    Country,
    Director,
    Episode,
    Genre,
    Media,
    Season,
)


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = (
        "persian_title",
        "media_type",
        "status",
        "imdb_rating",
        "release_date",
    )

    search_fields = (
        "persian_title",
        "title",
        "original_title",
        "slug",
    )

    list_filter = (
        "media_type",
        "status",
        "genres",
        "release_date",
    )

    ordering = ("-release_date",)

    filter_horizontal = (
        "genres",
        "actors",
        "directors",
        "countries",
    )


admin.site.register(Genre)
admin.site.register(Country)
admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Season)
admin.site.register(Episode)