from django.core.exceptions import ValidationError
from rest_framework import status


def not_equal_me_username_validator(value):
    """
    Custom username validator, which ckeck 'username' field is
    not equal 'me' string.
    """

    if value.lower() == 'me':
        raise ValidationError(
        'Недопустимое имя пользователя "me".',
        code=status.HTTP_400_BAD_REQUEST
    )
