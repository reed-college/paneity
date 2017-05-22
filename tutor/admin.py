from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

import tutor.models as models


class StudentInline(admin.StackedInline):
    """
    Inline field for the student
    """
    model = models.Student
    can_delete = False
    verbose_name = "Student Information"
    verbose_name_plural = "Student Information"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (StudentInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register the rest of the fields
admin.site.register(models.Subject)
admin.site.register(models.Course)
