from django.core.exceptions import ValidationError
from django.utils import timezone


def validator(value):
    if value < 868 or value > timezone.now().year:
        raise ValidationError("Год указан неверно!",
                              params={'value': value},)
