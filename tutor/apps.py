from django.apps import AppConfig


class TutorConfig(AppConfig):
    name = 'tutor'
    verbose_name = 'Courses'

    def ready(self):
        from tutor import signals
