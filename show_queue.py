
from django_init import django_init
django_init()

if True:
    from json import dumps

    from h5media.models import Profile


def main():
    profile = Profile.objects.get(user__username='john')
    formatted_json = dumps(profile.queue, indent=2)
    print(formatted_json)


if __name__ == '__main__':
    main()
