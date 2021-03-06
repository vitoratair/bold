import logging
import threading

from core import constants as c
from core.commons.helper import Helper as CoreHelper
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_condition import Or
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from omdb_adapter.connection_service import ConnectionService
from omdb_adapter.serializers import OmdbMoviesListSerializer
from drf_yasg.utils import  swagger_auto_schema

logger = logging.getLogger('adapter_omdb')


class OmdbSyncAPIView(generics.GenericAPIView, CoreHelper):
    """
    ## Overview:

    Receive a GET request to sync movies from OMDB API to **bold** local database.
    Fetch info from API, serializer the data and send to bold **/api/movie/** API endpoint to be processed and saved\f

    ## Available subscribers

    Each subscriber has a specific payload, the documentation about it can be found on the link below.
    - <a target="_blank" href="https://www.omdbapi.com/">OMDB</a>
    \f
    """
    permission_classes = [Or(permissions.IsAdminUser, permissions.IsAuthenticated, TokenHasReadWriteScope)]
    serializer_class = OmdbMoviesListSerializer

    def _process_on_thread(self, request):
        """Must process the request payload on a thread to prevent timeout errors."""

        service = ConnectionService()

        movies = service.get_movies(c.GOT)

        if not movies:
            logger.error("Not possible to find any movie with the name requested")
            return

        data_serialized = OmdbMoviesListSerializer(data=movies)
        if not data_serialized.is_valid():
            logger.error(data_serialized.errors)
            return

        #### Adapter will send a POST request with all movies to the CORE application ####
        url = "http://localhost:8000/api/movie/" ### DEV ONLY
        self.make_post_core(url, request.auth, data_serialized.data)

    @swagger_auto_schema(
        operation_id='omdb_sync',
        operation_summary="OMDB - Sync movies",
        responses = {
            200: '',
            404: ' Targeted subscriber was not found.'
        }
    )
    def get(self, request):
        logger.info("OmdbSyncAPIView - GET received")

        subscriber = self.get_subscriber(request.auth, c.MOVIE_RESOURCE)
        if subscriber is None:
            return Response({'error':True, 'error':"Targeted subscriber was not found."}, status=status.HTTP_404_NOT_FOUND)

        threading.Thread(target=self._process_on_thread, args=(request,)).start()

        return Response({}, status=status.HTTP_200_OK)
