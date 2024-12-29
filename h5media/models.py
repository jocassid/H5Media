
from collections.abc import Iterable
from typing import Optional, Tuple

from django.contrib.auth.models import User
from django.core.exceptions import (
    MultipleObjectsReturned,
    ObjectDoesNotExist,
)
from django.db.models import (
    Model,
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    IntegerField,
    JSONField,
    ManyToManyField,
    Max,
    OneToOneField,
    TextField,
    URLField,
)
from django.db.transaction import atomic


class DatabaseError(RuntimeError):
    pass


class BaseModel(Model):

    update_fields = tuple()

    class Meta:
        abstract = True

    def fetch(self) -> Optional[Model]:
        return None

    def update(
            self,
            instance: Model,
            copy_nulls: bool = False,
            defer_save: bool = False,
    ):
        for field in self.update_fields:
            rhs_value = getattr(instance, field)
            if rhs_value or copy_nulls:
                setattr(self, field, rhs_value)
        if defer_save:
            return
        self.save()


class Profile(BaseModel):
    user = OneToOneField(
        User,
        on_delete=CASCADE,
        related_name='profile',
    )

    def __str__(self):
        return self.user.username


class MediaFile(BaseModel):
    """Audio or visual file"""
    title = CharField(max_length=250)
    file_path = CharField(max_length=250)
    owner = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='media_files',
    )

    TYPE_PODCAST_EPISODE = 'e'
    TYPE_AUDIOBOOK_CHAPTER = 'c'
    TYPE_ALBUM_TRACK = 't'
    TYPE_MEDIA_FILE = 'm'

    TYPE_CHOICES = (
        (TYPE_PODCAST_EPISODE, 'Podcast Episode'),
        (TYPE_AUDIOBOOK_CHAPTER, 'Audiobook Chapter'),
        (TYPE_ALBUM_TRACK, 'Album Track'),
        (TYPE_MEDIA_FILE, 'Media File')
    )

    type = CharField(
        max_length=1,
        null=False,
        blank=False,
        default=TYPE_MEDIA_FILE,
        choices=TYPE_CHOICES,
    )


class PlayList(BaseModel):
    owner = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='playlists',
    )
    name = CharField(max_length=200)


class Podcast(BaseModel):

    update_fields = ('title', 'website', 'rss', 'description')

    title = CharField(max_length=200, unique=True)

    website = URLField(max_length=500, default='')
    
    rss = URLField(max_length=500, default='', unique=True)

    description = TextField(default='')

    subscribers = ManyToManyField(
        User,
        blank=True,
        related_name='podcasts_subscribed_to',
    )

    def __str__(self):
        return self.title

    def fetch(self) -> Optional[Model]:
        try:
            podcast = Podcast.objects.get(rss__iexact=self.rss)
        except ObjectDoesNotExist:
            return None
        else:
            return podcast


class PodcastEpisode(MediaFile):

    update_fields = (
        'podcast', 'title', 'url',
        'pub_date', 'description',
    )

    podcast = ForeignKey(
        Podcast,
        related_name='episodes',
        on_delete=CASCADE
    )

    url = URLField(max_length=500, default='', unique=True)

    pub_date = DateTimeField(
        null=True,
        blank=True,
    )

    description = TextField(default='')

    def __str__(self):
        return self.title

    def fetch(self) -> Optional[Model]:
        try:
            episode = PodcastEpisode.objects.get(url__iexact=self.url)
        except ObjectDoesNotExist:
            return None
        else:
            return episode
















