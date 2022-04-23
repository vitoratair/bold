from core.movies.views import MovieResourceAPIView
from django.urls import path

movies_urlpatterns = [
    path('api/movie/', MovieResourceAPIView.as_view(), name="movie_resource")
]
