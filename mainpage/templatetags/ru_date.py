from django import template
import babel.dates


register = template.Library()

@register.filter
def ru_date(value, format="d MMM"):
    """
    Форматирует дату в русской локали.
    Пример: 22 фев / пн
    """
    if not value:
        return ""
    if isinstance(value, str):
        return value
    return babel.dates.format_date(value, format=format, locale='ru')

@register.filter
def ru_date_full(value, format="d MMMM yyyy"):
    """
    Форматирует дату в русской локали.
    Пример: 22 февраля 2025
    """
    if not value:
        return ""
    if isinstance(value, str):
        return value
    return babel.dates.format_date(value, format=format, locale='ru')