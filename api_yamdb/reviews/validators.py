from django.core.exceptions import ValidationError


def validate_score(value):
    """
    Validates the score is
    between 1 and 10 inclusive.
    """
    if value in range(1, 11):
        return value
    raise ValidationError(
        'Оценка должна быть от 1 до 10.'
    )
