from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import CreateView

from interactions.models import Favorite, Rating, Review, Watchlist

from .forms import LoginForm, RegisterForm


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


class UserRegisterView(CreateView):
    form_class = RegisterForm
    template_name = "accounts/register.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

    def get_success_url(self):
        return "/"
    
class UserLogoutView(LogoutView):
    next_page = "/"


@login_required
def profile_view(request):
    favorites = list(
        Favorite.objects
        .filter(user=request.user)
        .select_related("media")[:12]
    )
    watchlist_items = list(
        Watchlist.objects
        .filter(user=request.user)
        .select_related("media")[:12]
    )
    ratings = list(
        Rating.objects
        .filter(user=request.user)
        .select_related("media")[:12]
    )
    reviews = list(
        Review.objects
        .filter(user=request.user)
        .select_related("media")[:8]
    )

    context = {
        "favorites": favorites,
        "watchlist_items": watchlist_items,
        "ratings": ratings,
        "reviews": reviews,
        "favorite_count": request.user.favorites.count(),
        "watchlist_count": request.user.watchlist.count(),
        "rating_count": request.user.ratings.count(),
        "review_count": request.user.reviews.count(),
    }

    return render(request, "pages/profile.html", context)
