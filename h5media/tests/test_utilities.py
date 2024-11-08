
from django.contrib.auth.models import User

from faker import Faker

faker = Faker()


def create_user(first_name: str = '') -> User:
    first_name = first_name or faker.first_name()
    last_name = faker.last_name()
    username = f"{first_name}.{last_name}@{faker.domain_name()}"
    return User.objects.create_user(
        username,
        email=username,
        password='password123',
        first_name=first_name,
        last_name=last_name,
    )
