from core.models import Subscriber
from django.db import models
from django.utils import timezone
from django.db.models import Avg
from auditlog.registry import auditlog

class Movie(models.Model):
    """
    Stores a single movie entry
    """

    ### In case of the aplication grow big and multiples adapters needed to be used ###
    subscriber = models.ForeignKey(Subscriber, related_name="subscriber_movie", on_delete=models.CASCADE)
    subscriber_movie_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    title = models.CharField(max_length=255)
    total_seasons = models.IntegerField()
    year = models.CharField(max_length=9)
    released = models.DateField()
    runtime = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    writer = models.CharField(max_length=255)
    actors = models.TextField()
    plot = models.TextField()
    language = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    awards = models.CharField(max_length=255)
    poster_url = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    votes = models.IntegerField()
    type = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % (self.title)


    def total_episodes(self):
        """
            Must return the count of all episodes associated with the movie instance
        """

        return Episode.objects.filter(movie_id=self.id).count()

    def rating_average(self):
        """
            Must return the rating avg of all episodes associated with the movie instance
        """
        queryset = Episode.objects.filter(
            movie_id=self.id
        ).aggregate(
            Avg('rating')
        )
        if queryset.get('rating__avg') is None:
            return 'N/A'

        return '{0:.2f}'.format(queryset.get('rating__avg'))


class Episode(models.Model):
    """
    Stores a single episode entry
    Related to :model:`core.Movie`
    """

    movie = models.ForeignKey('Movie', related_name="episodes", on_delete=models.CASCADE)
    subscriber_movie_episode_id = models.CharField(max_length=255)

    ### Required fields ###
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=9)
    released = models.DateField()
    episode_number = models.IntegerField()
    season = models.IntegerField()
    runtime = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    writer = models.CharField(max_length=255)
    actors = models.TextField()
    plot = models.TextField()
    language = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    awards = models.CharField(max_length=255)
    poster_url = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    votes = models.IntegerField()

    def __str__(self):
        return "%s - Season %s | %s" % (self.movie.title, self.season, self.title)

class Comment(models.Model):
    """
    Stores a single comment entry
    Related to :model:`core.Episode`
    """
    episode = models.ForeignKey('Episode', related_name="comment", on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "%s | %s" % (self.episode.title, self.comment[0:100])


auditlog.register(Movie)
auditlog.register(Episode)
auditlog.register(Comment)