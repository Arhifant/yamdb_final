from django.core.exceptions import ValidationError


def me_username_validator(value):
    if value.lower() == "me":
        raise ValidationError("Username <me> is prohibited.")
