from django.utils import timezone
from django.core.exceptions import ValidationError


def validator(value):
    if value < 868 or value > timezone.now().year:
        raise ValidationError("Год указан неверно!",
                              params={'value': value},)
