from django.contrib import admin
from core.movies.models import Movie, Episode

class EpisodeAdmin(admin.ModelAdmin):
    list_filter = ('season',)

admin.site.register(Movie)
admin.site.register(Episode, EpisodeAdmin)

