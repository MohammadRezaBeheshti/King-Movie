from django.contrib import admin

from .models import Favorite, Rating, Review, Watchlist

admin.site.register(Favorite)
admin.site.register(Watchlist)
admin.site.register(Rating)
admin.site.register(Review)