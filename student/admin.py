

from django.contrib import admin
from myproject.student.models import Student, WithdrawnStudent


admin.site.register([Student, WithdrawnStudent])
