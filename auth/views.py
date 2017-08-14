from django.shortcuts import redirect
from django.contrib.auth import logout as logout_func


def logout(request):
    logout_func(request)
    return redirect("https://weblogin.reed.edu/cgi-bin/logout.cgi")
