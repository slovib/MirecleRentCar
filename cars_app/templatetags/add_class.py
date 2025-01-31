from django import template

register = template.Library()

@register.filter
def to_millions(value):
    """Фильтр для преобразования цены в миллионы."""
    try:
        return round(value / 1_000_000, 1)  # Делим на миллион и округляем до 1 знака
    except (TypeError, ValueError):
        return value  # Возвращаем исходное значение, если возникла ошибка
