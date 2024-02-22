from django.core.exceptions import ValidationError
from rest_framework import status


def not_equal_me_username_validator(value):
    """
    Custom username validator, which ckeck 'year' field and
    rise error when year value is greater than the current one.
    """

    if value.lower() == 'me':
        raise ValidationError(
        'Недопустимое имя пользователя "me".',
        code=status.HTTP_400_BAD_REQUEST
    )
