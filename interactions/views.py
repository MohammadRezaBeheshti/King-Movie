from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from media_library.models import Media

from .forms import RatingForm, ReviewForm
from .models import Favorite, Rating, Review, Watchlist


def _get_media(slug):
    return get_object_or_404(Media, slug=slug)


@login_required
@require_POST
def toggle_favorite(request, slug):
    media = _get_media(slug)
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        media=media,
    )

    if created:
        messages.success(request, "به علاقه‌مندی‌ها اضافه شد.")
    else:
        favorite.delete()
        messages.info(request, "از علاقه‌مندی‌ها حذف شد.")

    return redirect("media_detail", slug=media.slug)


@login_required
@require_POST
def toggle_watchlist(request, slug):
    media = _get_media(slug)
    watchlist_item, created = Watchlist.objects.get_or_create(
        user=request.user,
        media=media,
    )

    if created:
        messages.success(request, "به لیست تماشا اضافه شد.")
    else:
        watchlist_item.delete()
        messages.info(request, "از لیست تماشا حذف شد.")

    return redirect("media_detail", slug=media.slug)


@login_required
@require_POST
def submit_rating(request, slug):
    media = _get_media(slug)
    form = RatingForm(request.POST)

    if form.is_valid():
        Rating.objects.update_or_create(
            user=request.user,
            media=media,
            defaults={"score": form.cleaned_data["score"]},
        )
        messages.success(request, "امتیاز شما ثبت شد.")
    else:
        messages.error(request, "امتیاز باید عددی بین ۱ تا ۱۰ باشد.")

    return redirect("media_detail", slug=media.slug)


@login_required
@require_POST
def manage_review(request, slug):
    media = _get_media(slug)
    action = request.POST.get("action", "save")

    if action == "delete":
        deleted_count, _ = Review.objects.filter(
            user=request.user,
            media=media,
        ).delete()

        if deleted_count:
            messages.info(request, "نظر شما حذف شد.")
        else:
            messages.warning(request, "نظری برای حذف پیدا نشد.")

        return redirect("media_detail", slug=media.slug)

    form = ReviewForm(request.POST)

    if form.is_valid():
        Review.objects.update_or_create(
            user=request.user,
            media=media,
            defaults={
                "content": form.cleaned_data["content"],
                "is_approved": True,
            },
        )
        messages.success(request, "نظر شما ثبت شد.")
    else:
        messages.error(request, "متن نظر نمی‌تواند خالی باشد.")

    return redirect("media_detail", slug=media.slug)
