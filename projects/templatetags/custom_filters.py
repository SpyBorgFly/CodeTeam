from django import template

register = template.Library()

from django import template

register = template.Library()

@register.filter(name='groupby')
def groupby(value, arg):
    """Groups a list of objects by a specified attribute."""
    grouped = {}
    for item in value:
        key = getattr(item, arg)
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(item)
    return grouped

@register.filter(name='get_attr')
def get_attr(obj, attr_name):
    """Returns the attribute value of an object."""
    try:
        return getattr(obj, attr_name)
    except AttributeError:
        return None
    
@register.filter(name='contains')
def contains(value, arg):
    return arg in value

