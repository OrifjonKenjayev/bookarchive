from django import template
import os

register = template.Library()

@register.filter
def ext(file_field):
    """
    Return the lowercase extension of a FileField or string path.
    Usage: {{ book.file|ext }} -> "pdf" or "epub" etc.
    """
    if not file_field:
        return ''
    # file_field may be a FieldFile or a string
    try:
        name = file_field.url if hasattr(file_field, 'url') else str(file_field)
    except Exception:
        name = str(file_field)
    _, extension = os.path.splitext(name)
    return extension.lower().lstrip('.')
