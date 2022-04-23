
from distutils.log import info
from rest_framework import status
from omdb_adapter.models import Mapper
from omdb_adapter import constants as c
import requests
import logging
logger = logging.getLogger('adapter_omdb')


class ConnectionService:

    def __init__(self, **kargs):

        if kargs.get('auth'):
            self.auth = kargs.get('auth')
        else:
            self.auth = self._get_mappers(c.AUTH_SETTINGS)

        if kargs.get('urls'):
            self.urls = kargs.get('urls')
        else:
            self.urls = self._get_mappers(c.URLS)



    def _get_data_from_response(self, response):
        """Return if the response is 200 OK the data from the json response or set a new token in case of response = 401"""


        if response.status_code == status.HTTP_200_OK:
            return response.json()

        elif response.status_code == status.HTTP_401_UNAUTHORIZED or response.status_code == status.HTTP_403_FORBIDDEN:
            ### If API was using OUTH shoud refresh token and repeat the same request ###
            return False


    def _make_get_request(self, url, token=None):
        """Must return a response from a GET request"""

        headers = {}
        return requests.get(url, headers=headers)

    def _get_mappers(self, mapper=None):
        """get auth mapper"""

        if mapper is None:
            return False

        try:
            return Mapper.objects.get(name=mapper).mapper
        except Exception as e:
            logger.error("Not possible to find the adapter %s" % (mapper))
            return False

    def get_episodes_by_season(self, imdb_id, season):
        """
            Must fetch all episodes from a given movie / season and set on movie payload
        """

        movie_url = self.urls.get('movie') % (imdb_id, self.auth.get('token')) + "&season=%s" % (season,)
        data = self._get_data_from_response(self._make_get_request(movie_url))

        full_episodes_details = []
        for episodes in data.get('Episodes'):
            episode_url = self.urls.get('season') % (episodes.get('imdbID'), self.auth.get('token'))
            full_episodes_details.append(
                self._get_data_from_response(self._make_get_request(episode_url))
            )

        return full_episodes_details


    def get_movies(self, movie_name=''):
        """
            Must return a movie or a list from movies on omdb API service
        """

        movie_url = self.urls.get('movie') % (movie_name, self.auth.get('token'))
        response = self._make_get_request(movie_url)
        data = self._get_data_from_response(response)

        if not data or type(data) != dict:
            return False

        data['Episodes'] = []
        for season in range(0, int(data.get('totalSeasons'))):
            data['Episodes'] += self.get_episodes_by_season(data.get('imdbID'), season + 1)

        return data
