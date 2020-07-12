
from django.contrib import admin
from myproject.sysadmin.models import *

admin.site.register([ClassTeacher, tblrpin, tblexpress,subjectteacher, userprofile,currentsession,Principal])
