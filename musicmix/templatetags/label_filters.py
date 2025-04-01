from . import register
from ..models import Label


@register.filter(name='label_type')
def label_type(value: list[Label], t: str) -> list[Label]:
    return list(filter(lambda label: label.label_type == t, value))
