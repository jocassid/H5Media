
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


class TitledObjectMixin(Model):
    title = CharField(
        max_length=250,
        null=False,
        blank=False,
        default='',
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class BaseModel(Model):

    update_fields = tuple()

    class Meta:
        abstract = True

    def fetch(self) -> Optional[Model]:
        """When this method is invoked on an unsaved instance of BaseModel,
        an attempt will be made to find a matching record in the database.
        If a matching record is found, the record is returned otherwise None
        is returned.  Subclasses will override this method to match on
        whatever fields are appropriate for that Model"""
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


def profile_queue_default():
    return []


class Profile(BaseModel):
    user = OneToOneField(
        User,
        on_delete=CASCADE,
        related_name='profile',
    )

    queue = JSONField(
        null=False,
        blank=False,
        default=profile_queue_default
    )

    def __str__(self):
        return self.user.username


class MediaFile(TitledObjectMixin, BaseModel):
    """Audio or visual file"""
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


def playlist_contents_default():
    return []


class PlayList(TitledObjectMixin, BaseModel):
    owner = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='playlists',
    )

    contents = JSONField(
        null=False,
        blank=False,
        default=playlist_contents_default
    )


class Podcast(BaseModel):

    update_fields = ('title', 'website', 'rss', 'description')

    # This class doesn't inherit from TitledObjectMixin because of the
    # unique constraint on this field.
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

    def fetch(self) -> Optional[Model]:
        try:
            episode = PodcastEpisode.objects.get(url__iexact=self.url)
        except ObjectDoesNotExist:
            return None
        else:
            return episode


class Audiobook(TitledObjectMixin, BaseModel):
    pass


class AudiobookChapter(MediaFile):
    audiobook = ForeignKey(
        Audiobook,
        related_name='chapters',
        on_delete=CASCADE
    )

    chapter = IntegerField(
        null=False,
        blank=False,
        default=0,
    )

    class Meta:
        unique_together = [[
            'audiobook',
            'chapter'
        ]]


class Album(TitledObjectMixin, BaseModel):
    pass


class AlbumTrack(MediaFile):

    album = ForeignKey(
        Album,
        null=True,
        blank=True,
        related_name='tracks',
        on_delete=CASCADE,
    )














