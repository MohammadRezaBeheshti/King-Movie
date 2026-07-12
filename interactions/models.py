from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from media_library.models import Media


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="کاربر",
    )
    media = models.ForeignKey(
        Media,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="رسانه",
    )
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)

    class Meta:
        verbose_name = "علاقه‌مندی"
        verbose_name_plural = "علاقه‌مندی‌ها"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "media"],
                name="unique_favorite_per_user_media",
            ),
        ]

    def __str__(self):
        return f"{self.user} - {self.media}"


class Watchlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="watchlist",
        verbose_name="کاربر",
    )
    media = models.ForeignKey(
        Media,
        on_delete=models.CASCADE,
        related_name="watchlist",
        verbose_name="رسانه",
    )
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)

    class Meta:
        verbose_name = "لیست تماشا"
        verbose_name_plural = "لیست‌های تماشا"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "media"],
                name="unique_watchlist_per_user_media",
            ),
        ]

    def __str__(self):
        return f"{self.user} - {self.media}"


class Rating(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ratings",
        verbose_name="کاربر",
    )
    media = models.ForeignKey(
        Media,
        on_delete=models.CASCADE,
        related_name="ratings",
        verbose_name="رسانه",
    )
    score = models.PositiveSmallIntegerField(
        "امتیاز",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
    )
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField("تاریخ ویرایش", auto_now=True)

    class Meta:
        verbose_name = "امتیاز"
        verbose_name_plural = "امتیازها"
        ordering = ["-updated_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "media"],
                name="unique_rating_per_user_media",
            ),
            models.CheckConstraint(
                condition=models.Q(score__gte=1) & models.Q(score__lte=10),
                name="rating_score_between_1_and_10",
            ),
        ]

    def __str__(self):
        return f"{self.user} - {self.media}: {self.score}"


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="کاربر",
    )
    media = models.ForeignKey(
        Media,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="رسانه",
    )
    content = models.TextField("متن نظر")
    is_approved = models.BooleanField("تایید شده", default=True)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField("تاریخ ویرایش", auto_now=True)

    class Meta:
        verbose_name = "نقد و نظر"
        verbose_name_plural = "نقد و نظرها"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "media"],
                name="unique_review_per_user_media",
            ),
        ]

    def __str__(self):
        return f"{self.user} - {self.media}"
