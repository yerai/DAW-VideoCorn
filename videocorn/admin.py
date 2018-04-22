from django.contrib import admin
from .models import Genre, Year, Score, Actor, Movie

admin.site.register(Genre)
admin.site.register(Year)
admin.site.register(Score)
admin.site.register(Actor)
admin.site.register(Movie)
