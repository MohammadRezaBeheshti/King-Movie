from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html

from .models import (
    Actor,
    Country,
    Director,
    Episode,
    Genre,
    Media,
    MediaSource,
    MediaType,
    Season,
)


def image_preview(image, width=56, height=78):
    if not image:
        return "-"

    return format_html(
        '<img src="{}" width="{}" height="{}" style="object-fit: cover; border-radius: 6px;" />',
        image.url,
        width,
        height,
    )


class RelatedMediaCountMixin:
    media_count_label = "تعداد آثار"

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            media_count=Count("media", distinct=True),
        )

    @admin.display(description=media_count_label, ordering="media_count")
    def media_count(self, obj):
        return obj.media_count


class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 1
    fields = ("episode_number", "title", "runtime", "release_date")
    ordering = ("episode_number",)


class SeasonInline(admin.TabularInline):
    model = Season
    extra = 1
    fields = ("season_number", "episode_count", "episodes_link")
    readonly_fields = ("episode_count", "episodes_link")
    show_change_link = True
    ordering = ("season_number",)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            episode_count_value=Count("episodes", distinct=True),
        )

    @admin.display(description="تعداد قسمت‌ها", ordering="episode_count_value")
    def episode_count(self, obj):
        return getattr(obj, "episode_count_value", 0)

    @admin.display(description="مدیریت قسمت‌ها")
    def episodes_link(self, obj):
        if not obj.pk:
            return "پس از ذخیره فصل فعال می‌شود"

        url = reverse("admin:media_library_season_change", args=[obj.pk])
        return format_html('<a href="{}">ویرایش فصل و قسمت‌ها</a>', url)


class MediaSourceInline(admin.TabularInline):
    model = MediaSource
    extra = 1
    fields = (
        "title",
        "quality",
        "language",
        "subtitle_language",
        "source_type",
        "url",
        "file_size",
        "is_active",
        "ordering",
    )
    ordering = ("ordering", "quality")


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = (
        "poster_preview",
        "display_title",
        "original_title",
        "media_type",
        "status",
        "release_date",
        "imdb_rating",
        "genre_list",
        "season_count",
        "is_featured",
    )
    list_display_links = ("poster_preview", "display_title")
    list_filter = (
        "media_type",
        "status",
        "release_date",
        "genres",
    )
    search_fields = (
        "persian_title",
        "title",
        "original_title",
        "slug",
        "actors__full_name",
    )
    ordering = ("-release_date", "persian_title", "title")
    readonly_fields = ("poster_large_preview", "backdrop_large_preview")
    filter_horizontal = (
        "genres",
        "actors",
        "directors",
        "countries",
    )
    list_per_page = 25
    save_on_top = True
    inlines = (SeasonInline,)
    fieldsets = (
        (
            "اطلاعات اصلی",
            {
                "fields": (
                    "title",
                    "persian_title",
                    "original_title",
                    "slug",
                    "media_type",
                    "status",
                    "is_featured",
                )
            },
        ),
        (
            "جزئیات انتشار",
            {
                "fields": (
                    "overview",
                    "release_date",
                    "runtime",
                    "imdb_rating",
                    "trailer",
                )
            },
        ),
        (
            "تصاویر",
            {
                "fields": (
                    "poster",
                    "poster_large_preview",
                    "backdrop",
                    "backdrop_large_preview",
                )
            },
        ),
        (
            "دسته‌بندی و عوامل",
            {
                "fields": (
                    "genres",
                    "actors",
                    "directors",
                    "countries",
                )
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            "genres",
            "actors",
            "directors",
            "countries",
        ).annotate(
            season_count_value=Count("seasons", distinct=True),
        )

    def get_inline_instances(self, request, obj=None):
        inlines = []
        if obj:
            if obj.media_type in {MediaType.SERIES, MediaType.ANIME}:
                inlines.append(SeasonInline)
            else:
                inlines.append(MediaSourceInline)
        return [inline(self.model, self.admin_site) for inline in inlines]

    @admin.display(description="عنوان")
    def display_title(self, obj):
        return obj.persian_title or obj.title

    @admin.display(description="پوستر")
    def poster_preview(self, obj):
        return image_preview(obj.poster, width=46, height=68)

    @admin.display(description="پیش‌نمایش پوستر")
    def poster_large_preview(self, obj):
        return image_preview(obj.poster, width=140, height=210)

    @admin.display(description="پیش‌نمایش بک‌دراپ")
    def backdrop_large_preview(self, obj):
        return image_preview(obj.backdrop, width=260, height=146)

    @admin.display(description="ژانرها")
    def genre_list(self, obj):
        genres = [genre.name for genre in obj.genres.all()[:3]]
        if not genres:
            return "-"

        suffix = " ..." if obj.genres.count() > 3 else ""
        return f"{'، '.join(genres)}{suffix}"

    @admin.display(description="فصل‌ها", ordering="season_count_value")
    def season_count(self, obj):
        return obj.season_count_value


@admin.register(Genre)
class GenreAdmin(RelatedMediaCountMixin, admin.ModelAdmin):
    list_display = ("name", "slug", "media_count")
    search_fields = ("name", "slug")
    list_filter = ("media__media_type",)
    ordering = ("name",)


@admin.register(Country)
class CountryAdmin(RelatedMediaCountMixin, admin.ModelAdmin):
    list_display = ("name", "code", "media_count")
    search_fields = ("name", "code")
    list_filter = ("code", "media__media_type")
    ordering = ("name",)


@admin.register(Actor)
class ActorAdmin(RelatedMediaCountMixin, admin.ModelAdmin):
    list_display = ("image_thumb", "full_name", "media_count")
    list_display_links = ("image_thumb", "full_name")
    search_fields = ("full_name", "media__persian_title", "media__original_title", "media__title")
    list_filter = ("media__media_type",)
    ordering = ("full_name",)

    @admin.display(description="تصویر")
    def image_thumb(self, obj):
        return image_preview(obj.image, width=46, height=46)


@admin.register(Director)
class DirectorAdmin(RelatedMediaCountMixin, admin.ModelAdmin):
    list_display = ("image_thumb", "full_name", "media_count")
    list_display_links = ("image_thumb", "full_name")
    search_fields = ("full_name", "media__persian_title", "media__original_title", "media__title")
    list_filter = ("media__media_type",)
    ordering = ("full_name",)

    @admin.display(description="تصویر")
    def image_thumb(self, obj):
        return image_preview(obj.image, width=46, height=46)


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ("media", "season_number", "episode_count")
    list_filter = ("media__media_type", "media")
    search_fields = (
        "media__persian_title",
        "media__title",
        "media__original_title",
    )
    ordering = ("media__persian_title", "season_number")
    inlines = (EpisodeInline,)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("media").annotate(
            episode_count_value=Count("episodes", distinct=True),
        )

    @admin.display(description="تعداد قسمت‌ها", ordering="episode_count_value")
    def episode_count(self, obj):
        return obj.episode_count_value


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    inlines = (MediaSourceInline,)
    list_display = (
        "title",
        "media_title",
        "season_number",
        "episode_number",
        "runtime",
        "release_date",
    )
    list_filter = ("season__media__media_type", "season__media", "release_date")
    search_fields = (
        "title",
        "season__media__persian_title",
        "season__media__title",
        "season__media__original_title",
    )
    ordering = (
        "season__media__persian_title",
        "season__season_number",
        "episode_number",
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("season", "season__media")

    @admin.display(description="رسانه", ordering="season__media__persian_title")
    def media_title(self, obj):
        return obj.season.media

    @admin.display(description="فصل", ordering="season__season_number")
    def season_number(self, obj):
        return obj.season.season_number


@admin.register(MediaSource)
class MediaSourceAdmin(admin.ModelAdmin):
    list_display = (
        "media_title",
        "episode_info",
        "title",
        "quality",
        "language",
        "source_type",
        "is_active",
        "ordering",
    )
    list_editable = ("is_active", "ordering")
    list_filter = (
        "source_type",
        "quality",
        "language",
        "is_active",
        "media__media_type",
    )
    search_fields = (
        "title",
        "media__persian_title",
        "media__title",
        "episode__title",
        "url",
    )
    ordering = ("media", "episode", "ordering")
    raw_id_fields = ("media", "episode")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("media", "episode")

    @admin.display(description="رسانه", ordering="media__persian_title")
    def media_title(self, obj):
        return obj.media.persian_title or obj.media.title

    @admin.display(description="فصل / قسمت", ordering="episode__episode_number")
    def episode_info(self, obj):
        if obj.episode:
            return f"فصل {obj.episode.season.season_number} | قسمت {obj.episode.episode_number}"
        return "فیلم / انیمیشن"
