
from django.test import TestCase

from h5media.actions.podcast_actions import AddEpisodeToQueueAction
from h5media.models import Podcast, PodcastEpisode, Profile
from h5media.serializers import PodcastEpisodeSerializer
from h5media.tests.test_utilities import create_user


class AddEpisodeToQueueActionTest(TestCase):

    def test_run(self):
        podcast = Podcast.objects.create(
            title="Even Truer Crime"
        )
        episode = PodcastEpisode.objects.create(
            podcast=podcast,
            title="Murderizing in Memphis",
        )
        profile = Profile.objects.create(
            user=create_user(),
        )
        self.assertEqual(profile.queue, [])

        AddEpisodeToQueueAction().run(episode, profile)

        profile.refresh_from_db()
        self.assertEqual(
            profile.queue,
            [
                PodcastEpisodeSerializer(episode).data
            ],
        )





class RssHandlerTest(TestCase):

    def test_stack_ends_with(self):
        self.fail()


