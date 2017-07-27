from django.apps import AppConfig


class TutorConfig(AppConfig):
    name = 'tutor'
    verbose_name = 'Courses'

    def ready(self):
        """
        This imports signals.py
        """
        from tutor import signals
