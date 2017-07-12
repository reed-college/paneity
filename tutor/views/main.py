from django.shortcuts import render
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Max
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

def about(request):
    return render(request, 'tutor/about.html')

@login_required
def tutorchat(request):
    """
    Page for tutors to get messaged
    """
    # you need to be a tutor to access this page
    if request.user.is_superuser:
        pass
    elif not getattr(request.user, 'student', False):
        return render(request, 'error/403.html', status=403)
    elif not request.user.student.tutor:
        return render(request, 'error/403.html', status=403)

    # Get websocket server
    context = {}
    context['ws_server_path'] = 'ws://{}:{}/'.format(
        settings.CHAT_WS_SERVER_HOST,
        settings.CHAT_WS_SERVER_PORT,
    )

    # I am getting all of the conversations the tutor is
    # involved in.
    # This is gonna get weird because the tutor may be the
    # 'owner' of a conversation or the 'opponent' of a
    # conversation.

    # These are the dialogs that the user owns
    ownerds = request.user.selfDialogs.annotate(
        lastm=Max("messages__modified"), null_m=Count("messages__dialog_id", distinct=True))
    # These are the dialogs that the user is in but does not own
    opponentds = request.user.dialog_set.annotate(
        lastm=Max("messages__modified"), null_m=Count("messages__dialog_id", distinct=True))
    # Note how the operations are the same for both of the above
    # querysets. 'lastm' will be returns the timestamp of the
    # most recent message in the conversation
    # 'null_m' will be how many distinct dialog_ids each message has
    # (Which will be either 0 or 1 since we are only looking at the
    #  messages from one dialog). This will be used to tell if the
    # dialog has messages or not

    dialogs = ownerds.union(opponentds).order_by("-null_m", "-lastm")
    # The above line combines the two querysets and orders them
    # first by whether or not they have messages and then by their
    # most recent message

    context['dialogs'] = dialogs

    return render(request, 'tutor/tutorchat.html', context)
