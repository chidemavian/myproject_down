from django.conf.urls.defaults import *
from django.views.generic import TemplateView
#from django.views.decorators.csrf import ensure_csrf_cookie

urlpatterns = patterns('myproject.setup.views',
    # Examples:
    url(r'^class/$','classarm', name = 'class and arm'),
    url(r'^arm/$','addarm',name= 'Arm'),
    url(r'^welcome/$','welcome'),                       
    url(r'^class/delete/(\d+)/$', 'deleteclasscode', name='deleteclass'),
    url(r'^arm/delete/(\d+)/$', 'deletearmcode', name='deletearm'),
    url(r'^getsubject/$', 'getsubject', name='getsubject'),
    url(r'^subject_group/$','subjectgroup'),
    url(r'^subjectgroup/delete/(\d+)/$', 'deletesubjectgroupcode'),
    url(r'^editsubject/(\d+)/$', 'editsubject', name='editsubject'),
    url(r'^house/delete/(\d+)/$', 'deletehousecode', name='deletehouse'),
    url(r'^subject/$', 'subject',name= 'Subject'),
    # departments & roles
    url(r'^departmentsandroles/$','department',name='department'),
    # houses
    url(r'^schoolhouse/$','house',name='house'),

    url(r'^lga/$','uploadlocalgovt',name ='uploadlocalgovt'),

)
