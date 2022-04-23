
import logging
from datetime import datetime

from core.movies.models import Episode, Movie
from rest_framework import serializers

logger = logging.getLogger('adapter_omdb')


class OmdbMoviesListSerializer(serializers.BaseSerializer):
    """
        Only used this kind of Serializer to represent the Django feature to override and make all kind of logic that we may need on the future.
    """

    def to_representation(self, instance):
        """
            Must represent the same payload instance of the OMDB result API.
            - Only for demostrate that we can handle the data as we needed, before save or do anything in the aplication.
        """

        return {
            "Title": instance.get('Title'),
            "Year": instance.get('Year'),
            "Released": instance.get('Released'),
            "Runtime": instance.get('Runtime'),
            "Genre": instance.get('Genre'),
            "Director": instance.get('Director'),
            "Writer": instance.get('Writer'),
            "Actors": instance.get('Actors'),
            "Plot": instance.get('Plot'),
            "Language": instance.get('Language'),
            "Country": instance.get('Country'),
            "Awards": instance.get('Awards'),
            "Poster": instance.get('Poster'),
            "Ratings": instance.get('Ratings'),
            "Metascore": instance.get('Metascore'),
            "imdbRating": instance.get('imdbRating'),
            "imdbVotes": instance.get('imdbVotes'),
            "imdbID": instance.get('imdbID'),
            "Type": instance.get('Type'),
            "totalSeasons": instance.get('totalSeasons'),
            "Response": instance.get('Response'),
            "MovieId": instance.get('imdbID'),
            "Episodes": instance.get("Episodes")
        }

    def to_internal_value(self, data):
        return data


class MovieCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'

    def to_internal_value(self, data):
        """Mapper data comming from OMDB service to CORE movie models."""

        mapper = {}

        # CORE Controllers
        mapper.update({'subscriber_id': data.get('subscriber')})
        mapper.update({'subscriber_movie_id': data.get('MovieId')})

        ### Movies fields ###
        mapper.update({'title': data.get('Title')})
        mapper.update({'total_seasons': data.get('totalSeasons')})
        mapper.update({'year': data.get('Year')})
        mapper.update({'released': datetime.strptime(data.get('Released'), '%d %b %Y').date()})
        mapper.update({'runtime': data.get('Runtime')})
        mapper.update({'genre': data.get('Genre')})
        mapper.update({'director': data.get('Director')})
        mapper.update({'writer': data.get('Writer')})
        mapper.update({'actors': data.get('Actors')})
        mapper.update({'plot': data.get('Plot')})
        mapper.update({'language': data.get('Language')})
        mapper.update({'country': data.get('Country')})
        mapper.update({'awards': data.get('Awards')})
        mapper.update({'poster_url': data.get('Poster')})
        mapper.update({'rating': data.get('imdbRating')})
        mapper.update({'votes': data.get('imdbVotes').replace(",", "")})
        mapper.update({'type': data.get('Type')})
        return mapper


class MovieEpisodeCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Episode
        fields = '__all__'


    def to_internal_value(self, data):
        """Mapper data comming from OMDB service to CORE movie models."""

        mapper = {}
        mapper.update({'subscriber_movie_episode_id': data.get('imdbID')})
        mapper.update({'movie_id': data.get('movie')})
        mapper.update({'title': data.get('Title')})
        mapper.update({'year': data.get('Year')})
        mapper.update({'runtime': data.get('Runtime')})
        mapper.update({'genre': data.get('Genre')})
        mapper.update({'director': data.get('Director')})
        mapper.update({'writer': data.get('Writer')})
        mapper.update({'actors': data.get('Actors')})
        mapper.update({'plot': data.get('Plot')})
        mapper.update({'language': data.get('Language')})
        mapper.update({'country': data.get('Country')})
        mapper.update({'awards': data.get('Awards')})
        mapper.update({'poster_url': data.get('Poster')})
        mapper.update({'votes': data.get('imdbVotes').replace(",", "")})
        mapper.update({'episode_number': data.get('Episode')})
        mapper.update({'released': datetime.strptime(data.get('Released'), '%d %b %Y').date()})
        mapper.update({'season': data.get('Season')})
        mapper.update({'rating': 0 if data.get('imdbRating') == 'N/A' else data.get('imdbRating')})
        return mapper
