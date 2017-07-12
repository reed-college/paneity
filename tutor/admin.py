from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError

import tutor.models as models


class StudentInline(admin.StackedInline):
    """
    Inline field for the student
    """
    model = models.Student
    can_delete = False
    verbose_name = "Student Information"
    verbose_name_plural = "Student Information"
    filter_horizontal = ['tutoring_classes', 'enrolled_classes']


class StudentChangeForm(UserChangeForm):
    def clean_first_name(self):
        if self.cleaned_data["first_name"].strip() == '':
            raise ValidationError("First name is required.")
        return self.cleaned_data["first_name"]

    def clean_last_name(self):
        if self.cleaned_data["last_name"].strip() == '':
            raise ValidationError("Last name is required.")
        return self.cleaned_data["last_name"]


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    form = StudentChangeForm
    inlines = (StudentInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register the rest of the fields
admin.site.register(models.Subject)
admin.site.register(models.Course)
