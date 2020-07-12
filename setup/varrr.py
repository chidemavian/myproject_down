from django.shortcuts import render_to_response, get_object_or_404
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from django.core.serializers.json import json
from myproject.assessment.forms import *
from myproject.academics.models import *
from myproject.sysadmin.models import *
from myproject.setup.models import *
from myproject.assessment.getordinal import *
from myproject.assessment.utils import *
from myproject.assessment.bsheet import *
from myproject.utilities.views import *
from django.db.models import Max,Sum
import datetime
from datetime import date
import locale
locale.setlocale(locale.LC_ALL,'')
import xlwt

currse = currentsession.objects.get(id = 1)

def sublists(varuser,session,klass):
    data = subjectteacher.objects.filter(teachername = varuser,session=session,klass = klass)
    for j in data:
        j = j.subject
        s = {j:j}
        sdic.update(s)
    kb = sdic.values()
    return kb
