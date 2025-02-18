# In curlyhair/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary by key."""
    try:
        return dictionary.get(key)
    except AttributeError:
        return None
