
import logging
import threading
import timeit

from core import constants as c
from core.movies.helper import Helper as MovieHelper
from core.movies.models import Episode
from core.movies.serializers import EpisodeListSerializer
from rest_framework import generics, status
from rest_framework.response import Response

logger = logging.getLogger('api_movie')


class MovieResourceAPIView(generics.GenericAPIView, MovieHelper):

    permission_classes = []
    queryset = Episode.objects.select_related('movie').all()
    serializer_class = EpisodeListSerializer

    def post(self, request, format=None):

        logger.info("MovieResource - POST received")

        return Response({}, status=status.HTTP_201_CREATED)

    def get(self, request):
        """."""
        logger.info("MovieResource - GET received")

        return Response({}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """."""
        logger.info("MovieResource - DELETE received")
        return Response({}, status=status.HTTP_204_NO_CONTENT)
