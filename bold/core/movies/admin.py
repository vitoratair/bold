from django.contrib import admin
from core.movies.models import Movie, Episode


class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'total_seasons', 'awards', 'total_episodes', 'rating_average')

class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie', 'title', 'season', 'rating')
    list_filter = ('season',)

admin.site.register(Movie, MovieAdmin)
admin.site.register(Episode, EpisodeAdmin)

