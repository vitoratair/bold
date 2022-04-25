from core.movies.views import *
from core.movies.views import MovieResourceAPIView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('comment', CommentEpisodeResource)


movies_urlpatterns = [
    path('movie/', MovieResourceAPIView.as_view(), name="movie_resource"),
    path(r'', include(router.urls))
]
