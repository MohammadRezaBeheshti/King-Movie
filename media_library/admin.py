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

admin.site.register(Genre)
admin.site.register(Country)
admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Media)
admin.site.register(Season)
admin.site.register(Episode)