
import logging
import threading
import timeit

from core import constants as c
from core.commons.helper import AdaptersHelper
from core.commons.helper import Helper as CoreHelper
from core.movies.helper import Helper as MovieHelper
from core.movies.models import Episode, Movie
from core.movies.serializers import EpisodeListSerializer, MovieSerializer
from rest_framework import generics, status
from rest_framework.response import Response

logger = logging.getLogger('api_movie')


class MovieResourceAPIView(generics.GenericAPIView, MovieHelper, AdaptersHelper, CoreHelper):

    permission_classes = []
    queryset = Episode.objects.select_related('movie').all()
    serializer_class = EpisodeListSerializer

    def post(self, request, format=None):

        logger.info("MovieResource - POST received")

        subscriber = self.get_subscriber(request.auth, c.MOVIE_RESOURCE)
        if subscriber is None:
            return Response({'error':True, 'error':"Targeted subscriber was not found."}, status=status.HTTP_404_NOT_FOUND)

        threading.Thread(target=self._create_resource, args=(request, subscriber)).start()

        return Response({}, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """
            Simple filter using query_params from api request.
            For more complex projects, a solution with models managers and django filters could be used, for example.
        """

        queryset = Episode.objects.select_related('movie').all()

        title = self.request.query_params.get('title', c.GOT)
        season = self.request.query_params.get('season')
        episode = self.request.query_params.get('episode')
        episode_id = self.request.query_params.get('episode_id')
        rating = self.request.query_params.get('rating')

        if episode_id:
            queryset = queryset.filter(id=episode_id)

        elif episode:
            queryset = queryset.filter(movie__title=title, season=season, episode_number=episode)

        elif season:
            queryset = queryset.filter(movie__title=title, season=season)

        elif title:
            queryset = queryset.filter(movie__title=title)

        else:
            queryset = queryset.none()

        if rating:
            queryset = queryset.filter(rating__gte=rating)

        return queryset


    def get(self, request):
        logger.info("MovieResourceAPIView - GET received")

        queryset = self.get_queryset()

        serializer_episodes = EpisodeListSerializer(data=queryset, many=True)
        serializer_episodes.is_valid()

        if not serializer_episodes.data:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        serializer_movie = MovieSerializer(
            data=Movie.objects.filter(
                pk=queryset.first().movie.id).all(), many=True
        )

        serializer_movie.is_valid()
        data = list(serializer_movie.data)[0]
        data['episodes'] = serializer_episodes.data

        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """
            Clean all movies from database
            For now here, later should be moved to adapter endpoint
        """

        threading.Thread(target=self._truncate_table_resource, args=(Movie,)).start()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
