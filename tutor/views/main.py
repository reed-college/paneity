from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
import tutor.models as models


def index(request):
    return render(
        request,
        'tutor/index.html',
        {"Subjects": list(models.Subject.objects.all())})


def tutors(request, course_id):
    """
    View for the tutors page
    It gets the course based on the course id put in the address bar.
    Then, if the course exists, it renders the tutors.html page and passes
    the list of tutors on that course to the page.
    """
    course = get_object_or_404(models.Course, pk=course_id)
    # course.tutors has the info of all of the users who are marked as tutors
    # for this course
    context = {
        "tutors": course.tutors.all().order_by('-user__last_login'),
        "course_name": course,
        "day": timedelta(days=1),
        "week": timedelta(days=7),
        "dnow": timezone.now(),
    }

    return render(
        request,
        'tutor/tutors.html',
        context
    )


def startstop(request):
    return render(request, 'tutor/startstop.html')
