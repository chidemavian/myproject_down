from django.conf.urls.defaults import *
from myproject.signals import *
from django.conf import settings
from myproject.sysadmin.views import *
from myproject.setup.views import *
from myproject.utilities.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', index),studentlogin
    # url(r'^login/$', index),


    url(r'^$', studentlogin),
    url(r'^login/$', studentlogin),

    url(r'^login/admin/$', index),

    url(r'^header/$', header),
    url(r'^welcome/$', welcomecode),
    url(r'^online/$', online_result),
    url(r'^subject_report/$', subject_report),
    url(r'^student_search/$', search_student),
    url(r'^logout/$', logoutuser),
    url(r'^unauthorised/$', unatho),
    url(r'^uploadlga/$',uploadlocal ),
    url(r'^uploadsubgroup/$',uploadaccsubgrp),
    url(r'^uploadacc/$',uploadacc),
    url(r'^home_dashboard/$',dashboard),
    url(r'^uploadtransaction/$',uploadtransaction),
    url(r'^pass_change/$', change_password),
    url(r'^getchangepassword/$', getchangepassword),
    url(r'^uploadstudent/$',uploadstudent),
    url(r'^uploadbill/$',uploadbill),#to upload bill setup
    url(r'^uploadbillname/$',uploadbillname),#to upload bill name
    url(r'^uploadadditionalbill/$',uploadadditionalbill),#to upload  additional bills
    url(r'^uploadpostedbill/$',uploadpostedbill),#to upload posted bill

    url(r'^changepassword/$', changepassword),
    url(r'^setup/', include('myproject.setup.urls')),
    url(r'^student/', include('myproject.student.urls')),
    url(r'^bill/', include('myproject.bill.urls')),
    url(r'^cbt/', include('myproject.CBT.urls')),
    url(r'^sysadmin/', include('myproject.sysadmin.urls')),
    url(r'^controllers/', include('myproject.sysadmin.urls')),
    url(r'^assessment/', include('myproject.assessment.urls')),

    url(r'^lesson/', include('myproject.lesson.urls')),
    url(r'^authen/', include('myproject.authen.urls')),

    url(r'^assignment/', include('myproject.assignment.urls')),
   # url(r'^transport/', include('myproject.transport.urls')),
    url(r'^utils/', include('myproject.utilities.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
   # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),

    #url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
