
import logging
import threading
import timeit

from core import constants as c
from core.commons.helper import AdaptersHelper
from core.commons.helper import Helper as CoreHelper
from core.movies.helper import Helper as MovieHelper
from core.movies.models import Episode, Movie, Comment
from core.movies.serializers import EpisodeListSerializer, MovieSerializer, EpisodeCommentSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from drf_yasg.utils import  swagger_auto_schema
from rest_framework.viewsets import ModelViewSet

logger = logging.getLogger('api_movie')


class MovieResourceAPIView(generics.GenericAPIView, MovieHelper, AdaptersHelper, CoreHelper):

    permission_classes = []
    queryset = Episode.objects.select_related('movie').all()
    serializer_class = EpisodeListSerializer

    @swagger_auto_schema(
        responses = {
            201: '',
            404: ' Targeted subscriber was not found.'
        }
    )
    def post(self, request, format=None):
        """
            - Save movies on database (only by subscribers)

            Endpoint only used by the aplication internal subscribers.

            In order to not change this enpoint or de models database if movies from diferents APIS are added later,
            all the particularity from the payload will be handle on the adapter serializer.
        """

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

        title = self.request.query_params.get('title')
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

        if rating:
            queryset = queryset.filter(rating__gte=rating)

        return queryset


    def get(self, request):
        """
            - List movies saved on database

        List movies saved on database
        ## Filters:
        - title
        - season
        - episode
        - episode_id
        """

        logger.info("MovieResourceAPIView - GET received")

        queryset = self.get_queryset()

        serializer_episodes = EpisodeListSerializer(data=queryset, many=True)
        serializer_episodes.is_valid()

        if not serializer_episodes.data:
            return Response([], status=status.HTTP_200_OK)

        payload_result = []
        for movie_id in list(set([item.get('movie') for item in serializer_episodes.data])):
            serializer_movie = MovieSerializer(data=Movie.objects.filter(pk=movie_id).all(), many=True)
            serializer_movie.is_valid()
            data = list(serializer_movie.data)[0]
            data['episodes'] = [item for item in serializer_episodes.data if item.get('movie') == movie_id]
            payload_result.append(data)

        return Response(payload_result, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """
            - Wipe clean all movies

            Wipe clean all movies
            With multiples subscribers should have a subscriber param
        """

        threading.Thread(target=self._truncate_table_resource, args=(Movie,)).start()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class CommentEpisodeResource(ModelViewSet):
    """
    Episode comments

    **GET**
    List all comments from an specific episode id
        **Filters**
            _/api/comments/**?episode**={episode_id}_

    **POST**
    Create a single coment

    **Delete**
    Delete a single comment

    """

    permission_classes = []
    serializer_class = EpisodeCommentSerializer
    queryset = Comment.objects.select_related('episode').all()
    http_method_names = ['get', 'post', 'delete']


    def get_queryset(self):
        """
            Simple filter using query_params from api request.
            For more complex projects, a solution with models managers and django filters could be used, for example.
        """

        episode = self.request.query_params.get('episode')

        queryset = Comment.objects.select_related('episode').all()
        if episode:
            queryset = queryset.filter(episode_id=episode)

        return queryset
