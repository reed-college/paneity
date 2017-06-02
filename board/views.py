from django.shortcuts import render
from django.http import Http404
from tutor.models import Subject


def list(request, subject_id):
    """
    List of posted questions for a given subject
    """
    try:
        subject = Subject.objects.get(pk=subject_id)
    except Subject.DoesNotExist:
        raise Http404("Course does not exist")

    return render(
        request,
        'board/list.html',
        {"subject": subject})
