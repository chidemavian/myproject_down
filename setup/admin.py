from django.contrib import admin
from myproject.setup.models import  *

admin.site.register([Subject, Class, Role, Department, Arm, LGA,School,subclass,gradingsys,appused])
