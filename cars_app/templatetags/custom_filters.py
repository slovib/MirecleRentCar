from django import template

register = template.Library()

@register.filter
def to_millions(value):
    """Фильтр для преобразования цены в миллионы, убирает ненужные нули после запятой."""
    try:
        # Делим цену на 1 миллион и форматируем, убирая лишние нули после запятой
        return f"{value / 1_000_000:.1f}".rstrip('0').rstrip('.')
    except (TypeError, ValueError):
        return value  # Возвращаем исходное значение, если возникла ошибка
