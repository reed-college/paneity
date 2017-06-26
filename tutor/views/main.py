from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.contrib.auth.decorators import login_required
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
    # course.tutors has the info of all of the users who are marked
    # as tutors for this course
    tutors = course.tutors.all().annotate(null_login=Count('user__last_login')
                                          ).order_by('-null_login', '-user__last_login')
    context = {
        "tutors": tutors,
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


def dropin(request):
    return render(request, 'tutor/dropin.html')


@login_required
def tutorchat(request):
    """
    Page for tutors to get messaged
    """
    # you need to be a tutor to access this page
    if not getattr(request.user, 'student', False):
        return render(request, 'error/403.html', status=403)
    if not request.user.student.tutor:
        return render(request, 'error/403.html', status=403)
    return render(request, 'tutor/tutorchat.html')
