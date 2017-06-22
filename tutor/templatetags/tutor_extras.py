from django import template

register = template.Library()


@register.filter
def datetime_ge(dt1, dt2):
    """
    Returns true if dt1 is greater than or equal to dt2 because the
    django templating language is too incomptetent to compare
    datetimes itself
    """
    return dt1 >= dt2
