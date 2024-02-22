from datetime import datetime

from django.core.exceptions import ValidationError
from rest_framework import status


def custom_year_validator(value):
    """
    Custom username validator, which ckeck 'username' field is
    not equal 'me' string.
    """

    if value > datetime.now().year:
        raise ValidationError(
            'Значение года не может быть больше текущего.',
            code=status.HTTP_400_BAD_REQUEST
        )
