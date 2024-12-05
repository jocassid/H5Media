
from django_init import django_init
django_init()

if True:
    from django.contrib.auth.models import User
    from django.db.models import BooleanField, Count, Q
    from django.db.models.functions import Cast

    from h5media.models import Podcast

"""
SELECT
    "h5media_podcast"."id",
    "h5media_podcast"."title",
    "h5media_podcast"."website",
    "h5media_podcast"."rss",
    "h5media_podcast"."description",
    CAST(
        COUNT("h5media_podcast_subscribers"."user_id") 
        FILTER (WHERE "h5media_podcast_subscribers"."user_id" = 1) 
        AS bool
    ) AS "subscribed"
FROM "h5media_podcast"
LEFT OUTER JOIN "h5media_podcast_subscribers"
    ON ("h5media_podcast"."id" = "h5media_podcast_subscribers"."podcast_id")
GROUP BY 
    "h5media_podcast"."id",
    "h5media_podcast"."title",
    "h5media_podcast"."website",
    "h5media_podcast"."rss",
    "h5media_podcast"."description";

"""

def main():
    user = User.objects.get(username='john')
    podcasts = Podcast.objects.annotate(
        subscribed=Cast(
            Count(
                'subscribers',
                filter=Q(subscribers=user.id)
            ),
            output_field=BooleanField(),
        )
    )
    print(f"{podcasts.query}\n")
    for podcast in podcasts:
        print(f"{podcast.subscribed}  {podcast.title}")


if __name__ == '__main__':
    main()
