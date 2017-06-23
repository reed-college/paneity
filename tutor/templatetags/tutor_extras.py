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


@register.filter
def get_vc_link(username1, username2):
    """
    This returns a link to a videochat room that is (most likely)
    unique to those two usernames. It returns the same link
    regardless of the order of the usernames
    """

    # I decided to hardcode this value here because if we change
    # our videochat provider, we will most likely need to change
    # this function
    VC_LINK_BASE = "https://meet.jit.si/"

    h1 = hash(username1)
    h2 = hash(username2)
    # This returns a string where the lower hash is first
    if h1 < h2:
        return "{}{}-{}".format(VC_LINK_BASE, h1, h2)
    return "{}{}-{}".format(VC_LINK_BASE, h2, h1)
