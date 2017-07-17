from django import template
from django.contrib.auth.models import User
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


@register.filter
def other_username(dialog, username):
    """
    This takes a django-private-chat dialog and a username and
    returns the username of the memeber of this dialog that doesnt
    match the variable, 'username'
    """
    if dialog.opponent.username == username:
        return dialog.owner.username
    elif dialog.owner.username == username:
        return dialog.opponent.username
    else:
        errortext = "Username {} not present in dialog".format(username)
        raise RuntimeError(errortext)


@register.filter
def get_name(user_name):
    """
    This takes a user's username and django-private-chat dialog as input and returns their first and last name.
    This is mainly for the django chat.
    """
    user = User.objects.get(username=user_name)
    return str(user.first_name) + " " + str(user.last_name)


@register.filter
def get_user(user_name):
    """
    Takes a username and returns a user
    """
    return User.objects.get(username=user_name)


@register.filter
def most_recent_message(dialog):
    """
    Takes a dialog and returns the most recent message in that
    dialog
    """
    return dialog.messages.order_by("-created").first()
