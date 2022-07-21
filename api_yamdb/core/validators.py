from datetime import date

from rest_framework.exceptions import ValidationError


def validate_date(year):
    current_year = int(date.today().year)
    if year > current_year or year <= 0:
        raise ValidationError('Ошибка! Введен неверный год!')
