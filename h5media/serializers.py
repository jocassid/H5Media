
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)


from h5media.models import PodcastEpisode


COMMON_MEDIA_FILE_FIELDS = (
    'pk',
    'title',
    'type',
)


class PodcastEpisodeSerializer(ModelSerializer):

    podcast_title = SerializerMethodField()

    class Meta:
        model = PodcastEpisode
        fields = COMMON_MEDIA_FILE_FIELDS + (
            'podcast_title',
        )

    @staticmethod
    def get_podcast_title(obj):
        podcast = obj.podcast
        if not podcast:
            return ''
        return podcast.title
            

