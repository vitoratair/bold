import logging

from core.movies.models import Movie, Episode, Comment
from rest_framework import serializers

logger = logging.getLogger('api_movie')

class EpisodeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Episode
        exclude = (
            'subscriber_movie_episode_id',
        )

class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        exclude = (
            'subscriber_movie_id',
            'created_at',
            'subscriber'
        )

class EpisodeCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
