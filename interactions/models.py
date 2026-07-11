from django.conf import settings
from django.db import models

from media_library.models import Media


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites",
    )

    media = models.ForeignKey(
        Media,
        on_delete=models.CASCADE,
        related_name="favorites",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "media")

    def __str__(self):
        return f"{self.user} - {self.media}"
    
class Watchlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="watchlist",
    )

    media = models.ForeignKey(
        Media,
        on_delete=models.CASCADE,
        related_name="watchlist",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "media")

    def __str__(self):
        return f"{self.user} - {self.media}"
    
class Rating(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    media = models.ForeignKey(
        Media,
        on_delete=models.CASCADE,
        related_name="ratings",
    )

    score = models.PositiveSmallIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "media")

    def __str__(self):
        return str(self.score)
    
class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    media = models.ForeignKey(
        Media,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.user.username