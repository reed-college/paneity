from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("List courses here.")

def admin(request):
    return HttpResponse("This be the admin page.")

def tutors(request):
    return HttpResponse("You're looking at online and offline tutors.")

def startstop(request):
    return HttpResponse("This be the page to start and stop a tutor's session.")