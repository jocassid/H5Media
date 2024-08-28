
from django.test import TestCase

from h5media.models import MediaFile, Profile
from h5media.tests.test_utilities import create_user



class ProfileTest(TestCase):

    def test_add(self):

        user = create_user()
        profile = Profile.objects.create(user=user)

        media_file = MediaFile.objects.create(
            title='episode1',
            file_path='/mnt/bulk/media/episode1.mp3',
            owner=user,
        )
        media_file.add_to_queue(profile)

        profile.refresh_from_db()
        self.assertEqual(
            [],
            profile.queue,
        )

        media_file2 = MediaFile.objects.create(
            title='episode2',
            file_path='/mnt/bulk/media/episode2.mp3',
            owner=user,
        )
        media_file2.add_to_queue(profile)

        self.assertEqual(
            [],
            profile.queue,
        )




