from django.conf import settings


def login_logout(request):
    """
    Adds LOGIN_URL and LOGOUT_URL from the settings to the context
    """
    return {"LOGIN_URL": settings.LOGIN_URL, "LOGOUT_URL": settings.LOGOUT_URL}
