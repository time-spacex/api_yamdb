from django.core.exceptions import ValidationError
from rest_framework import status


class NotEqualMeUsernameValidator:
    """
    Custom username validator, which ckeck 'username' field is
    not equal 'me' string.
    """

    def __call__(self, value):
        if value.lower() == 'me':
            raise ValidationError(
            'Недопустимое имя пользователя "me".',
            code=status.HTTP_400_BAD_REQUEST
        )