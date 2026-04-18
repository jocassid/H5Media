
from django.contrib.auth.forms import AuthenticationForm
from django.forms import (
    CharField,
    ChoiceField,
    PasswordInput,
    TextInput,
)

class BulmaAuthenticationForm(AuthenticationForm):
    username = CharField(
        widget=TextInput(
            attrs={"class": "input", "placeholder": "Username"},
        )
    )

    password = CharField(
        widget=PasswordInput(
            attrs={"class": "input", "placeholder": "Password"},
        )
    )

    mode = ChoiceField(
        label="Mode",
        choices=(
            ('', 'Select Mode'),
            ('desktop', 'Desktop'),
            ('mobile', 'Mobile'),
        )
    )
