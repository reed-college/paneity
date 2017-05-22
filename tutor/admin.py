from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from tutor.models import Student


class StudentInline(admin.StackedInline):
    """
    Inline field for the student
    """
    model = Student
    can_delete = False
    verbose_name_plural = 'student'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (StudentInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
