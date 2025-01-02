
from django_init import django_init
django_init()

if True:
    from h5media.models import MediaFile, Profile


def main():
    profile = Profile.objects.get(user__username='john')
    profile.queue = [
        {
            'pk': -1,
            'title': 'Beautiful World',
            'type': MediaFile.TYPE_ALBUM_TRACK,
        },
        {
            'pk': -2,
            'title': 'Django',
            'type': MediaFile.TYPE_PODCAST_EPISODE,
        },
        {
            'pk': -3,
            'title': 'Chapter1',
            'type': MediaFile.TYPE_AUDIOBOOK_CHAPTER,
        }
    ]
    profile.save()




if __name__ == '__main__':
    main()
