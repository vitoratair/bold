
import logging

import requests
import simplejson as json
from core import constants as c
from core.models import Subscriber
from omdb_adapter.serializers import \
    MovieCreateSerializer as OMDBMovieCreateSerializer
from omdb_adapter.serializers import \
    MovieEpisodeCreateSerializer as OMDBMovieEpisodeCreateSerializer
from rest_framework import status

logger = logging.getLogger('core_logger')

class Helper:
    """Generics methods to handle client ids, tenants managements and URLs."""

    def get_client_id(self, auth):
        if auth is None:
            return None

        return auth.application.client_id

    def get_subscriber(self, auth, resource):
        try:
            subscriber = Subscriber.objects.filter(
                resource=resource,
                client=auth.application.client_id,
                name=auth.application.name
            ).get()
        except Exception:
            return None

        result = {}
        result['client_id'] = auth.application.client_id
        result['tenant'] = auth.application.name
        result['subscriber'] = subscriber
        return result

    def make_post_core(self, url, token, data):
        headers = {'Authorization': 'Bearer %s' % (token), 'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(data, use_decimal=True), headers=headers, verify=False)

        if response.status_code == status.HTTP_201_CREATED:
            return True

        if response.status_code == status.HTTP_401_UNAUTHORIZED or response.status_code == status.HTTP_403_FORBIDDEN:
            ### Logic to refresh tokens and handle errors ###
            pass
        else:
            logger.error(response.status_code)
            logger.error(response.text)

        return False

class AdaptersHelper:
    """
        Adapter subscribers Helper
    """


    def get_serializer_by_subscriber(self, resource, subscriber, data, request=None, episodes=False):
        """Select the serializer (adapter) based on the subscriber."""

        if resource == c.MOVIE_RESOURCE:
            if subscriber.name == c.OMDB_ADAPTER:
                if not episodes:
                    data['subscriber'] = subscriber.id
                    return OMDBMovieCreateSerializer(data=data)
                else:
                    return OMDBMovieEpisodeCreateSerializer(data=data, many=True)

        return None
