import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    """The function checks that the year of creation of the title
    can not be in the future."""
    current_year = dt.datetime.now().year
    if value > current_year:
        raise ValidationError(
            "Ошибка: Год произведения не может быть в будущем"
        )
