

import logging

from core import constants as c

logger = logging.getLogger('api_movie')

class Helper:

    def set_movie_id_episodes(self, movie, episodes):
        """Set the movie id in each episode"""

        for episode in episodes:
            episode['movie'] = movie

        return episodes


    def _truncate_table_resource(self, model):

        try:
            count = model.objects.count()
            model.objects.all().delete()
            logger.info("%s movies were delete" % (count))
        except Exception as e:
            logger.exception(e)
            logger.info("Handle error...")


    def _create_resource(self, request, subscriber):
        """Must create on django models teh movie resource based on payload from request.data"""

        serializer = self.get_serializer_by_subscriber(c.MOVIE_RESOURCE, subscriber['subscriber'], request.data)
        if not serializer.is_valid():
            serializer.is_valid(raise_exception=True)

        serializer.save()

        data_episodes = self.set_movie_id_episodes(serializer.data.get('id'), request.data.pop("Episodes"))
        serializer_episodes = self.get_serializer_by_subscriber(
            c.MOVIE_RESOURCE,
            subscriber['subscriber'],
            data_episodes,
            request.data,
            True
        )

        if not serializer_episodes.is_valid():
            serializer_episodes.is_valid(raise_exception=True)

        serializer_episodes.save()

        logger.info("Threading concluded")
