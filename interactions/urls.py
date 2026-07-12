from django.urls import path

from . import views

app_name = "interactions"

urlpatterns = [
    path("media/<slug:slug>/favorite/", views.toggle_favorite, name="favorite"),
    path("media/<slug:slug>/watchlist/", views.toggle_watchlist, name="watchlist"),
    path("media/<slug:slug>/rating/", views.submit_rating, name="rating"),
    path("media/<slug:slug>/review/", views.manage_review, name="review"),
]
