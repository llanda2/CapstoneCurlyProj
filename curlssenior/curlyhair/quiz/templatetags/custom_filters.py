from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """Returns the value for a given key from a dictionary."""
    return dictionary.get(key)
