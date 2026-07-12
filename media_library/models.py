from django.db import models

class MediaType(models.TextChoices):
    MOVIE = "movie", "فیلم"
    SERIES = "series", "سریال"
    ANIME = "anime", "انیمه"
    ANIMATION = "animation", "انیمیشن"


class MediaStatus(models.TextChoices):
    RELEASED = "released", "منتشر شده"
    UPCOMING = "upcoming", "به زودی"
    ENDED = "ended", "پایان یافته"
    CANCELED = "canceled", "لغو شده"

class Genre(models.Model):
    name = models.CharField("نام", max_length=100, unique=True)
    slug = models.SlugField("اسلاگ", unique=True)

    class Meta:
        verbose_name = "ژانر"
        verbose_name_plural = "ژانرها"
        ordering = ["name"]

    def __str__(self):
        return self.name
    
class Country(models.Model):
    name = models.CharField("نام", max_length=100)
    code = models.CharField("کد", max_length=3, unique=True)

    class Meta:
        verbose_name = "کشور"
        verbose_name_plural = "کشورها"
        ordering = ["name"]

    def __str__(self):
        return self.name
    
class Actor(models.Model):
    full_name = models.CharField("نام", max_length=255)
    image = models.ImageField("تصویر", upload_to="actors/", blank=True)

    class Meta:
        verbose_name = "بازیگر"
        verbose_name_plural = "بازیگران"
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name
    
class Director(models.Model):
    full_name = models.CharField("نام", max_length=255)
    image = models.ImageField("تصویر", upload_to="directors/", blank=True)

    class Meta:
        verbose_name = "کارگردان"
        verbose_name_plural = "کارگردان‌ها"
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name
    
class Media(models.Model):
    title = models.CharField("عنوان", max_length=255)
    original_title = models.CharField("عنوان اصلی", max_length=255, blank=True)
    persian_title = models.CharField("عنوان فارسی", max_length=255, blank=True)

    slug = models.SlugField(unique=True)

    media_type = models.CharField(
        "نوع",
        max_length=20,
        choices=MediaType.choices,
    )

    is_featured = models.BooleanField(
    "پیشنهاد ویژه",
    default=False,
)

    status = models.CharField(
        "وضعیت",
        max_length=20,
        choices=MediaStatus.choices,
        default=MediaStatus.RELEASED,
    )

    overview = models.TextField("خلاصه", blank=True)

    release_date = models.DateField("تاریخ انتشار", null=True, blank=True)

    runtime = models.PositiveIntegerField(
        "مدت زمان (دقیقه)",
        null=True,
        blank=True,
    )

    imdb_rating = models.DecimalField(
        "امتیاز IMDb",
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
    )

    poster = models.ImageField(
        "پوستر",
        upload_to="media/posters/",
        blank=True,
    )

    backdrop = models.ImageField(
        "بک‌دراپ",
        upload_to="media/backdrops/",
        blank=True,
    )

    trailer = models.URLField(
        "لینک تریلر",
        blank=True,
    )

    genres = models.ManyToManyField(
        Genre,
        verbose_name="ژانرها",
        blank=True,
    )

    actors = models.ManyToManyField(
        Actor,
        verbose_name="بازیگران",
        blank=True,
    )

    directors = models.ManyToManyField(
        Director,
        verbose_name="کارگردان‌ها",
        blank=True,
    )

    countries = models.ManyToManyField(
        Country,
        verbose_name="کشورها",
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.persian_title or self.title

class Season(models.Model):
    media = models.ForeignKey(
        Media,
        on_delete=models.CASCADE,
        related_name="seasons",
        verbose_name="رسانه",
    )

    season_number = models.PositiveIntegerField("شماره فصل")

    class Meta:
        verbose_name = "فصل"
        verbose_name_plural = "فصل‌ها"
        ordering = ["season_number"]
        unique_together = ["media", "season_number"]

    def __str__(self):
        return (
            f"{self.media.persian_title} "
            f"- فصل {self.season_number}"
    )
    
class Episode(models.Model):
    season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        related_name="episodes",
        verbose_name="فصل",
    )

    title = models.CharField("عنوان", max_length=255)

    episode_number = models.PositiveIntegerField("شماره قسمت")

    runtime = models.PositiveIntegerField(
        "مدت زمان (دقیقه)",
        null=True,
        blank=True,
    )

    release_date = models.DateField(
        "تاریخ انتشار",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "قسمت"
        verbose_name_plural = "قسمت‌ها"
        ordering = ["episode_number"]
        unique_together = ["season", "episode_number"]

    def __str__(self):
         return (
            f"{self.season.media.persian_title} | "
            f"فصل {self.season.season_number} | "
            f"قسمت {self.episode_number}"
    )