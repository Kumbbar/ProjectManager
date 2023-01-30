from django.template.defaulttags import register
from datetime import datetime, date
from django.template.defaultfilters import stringfilter
import markdown
from markdown.extensions import codehilite, fenced_code


@register.filter
def format_date(value) -> str:
    if isinstance(value, datetime):
        return value.strftime('%Y.%m.%d %H:%M')
    if isinstance(value, date):
        return value.strftime('%Y.%m.%d')
    return value


@register.filter
def check_none(value) -> str:
    if value is None:
        return 'Нет'
    return value
    

@register.filter
@stringfilter
def convert_markdown(value) -> str:
    return markdown.markdown(value, extensions=['fenced_code', 'codehilite'])