
from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView, TemplateView
from myproject.student import models

urlpatterns = patterns('myproject.sysadmin.views',
    # Examples:
    #url(r'^$', 'index'),
    url(r'^createuser/$', 'creatuser'),
    url(r'^user_ajax/$','usersearchajax'),
    url(r'^users_ajax/$','usersearchajax1'),
    url(r'^backup-db/$', 'backup'),
    url(r'^setdeadlines/$', 'setdl'),
    url(r'^cf/deadlines/$', 'cfsetdl'),
    url(r'^rst/dl/$', 'rsetr'),
    url(r'^subclass/$', 'getsubclass'), 
    url(r'^comauto/$', 'comauto'),
    url(r'^comauto/range/$','ajaxrange'),
    url(r'^getusermain/$', 'getuseraccountmain'),
    url(r'^edituser/(\d+)/$', 'editusermain'),
    url(r'^getacademic/$', 'getstudentacademic'),
    url(r'^edituseraca/(\d+)/$', 'edituseraca'),
    url(r'^edithomescreen/(\d+)/$','editmyhome'),
    url(r'^getadmin/$', 'getadmin'),
    url(r'^homeview/$', 'homeview'),
    url(r'^edituseradmin/(\d+)/$', 'edituseradmin'),
    url(r'^unauto/$', 'adminunautomain'),
    url(r'^resetuser/$', 'resetusermain'),
    url(r'^duration/$', 'duration'),
    url(r'^date/$', 'date'),
    url(r'^classteacher/$', 'classteachermain'),


    url(r'^subject_group/$', 'subjectgroupmain'),


    url(r'^getteacher/$', 'getclassteacher'), 
    url(r'^getcommm/$', 'getautocom'), 
    url(r'^editautocomment/(\d+)/$', 'editautocomment'),
    url(r'^deleteclassteacher/(\d+)/$', 'deleteclassteacher'),
    url(r'^deleteduration/(\d+)/$', 'deleteduration'),


    url(r'^deletedate/(\d+)/$', 'deletedate'),


    url(r'^userviews/$','userviews'),


    url(r'^getuser/$', 'autocomplete'),

    url(r'^getname/$', 'autocompletes'),

    url(r'^subjectteacher/$', 'subjectteachermain'),
    url(r'^getsubjectteacher/$', 'getsubjectteacher'),

    url(r'^getgrpteacher/$', 'getgrpteacher'),


    url(r'^deletesubjectteacher/(\d+)/$', 'deletesubjectteacher'),
    url(r'^deletegrpteacher/(\d+)/$', 'deletegrpteacher'),


    url(r'^principal/$', 'principalmain'),
    url(r'^getprincipal/$', 'getprin'),
    url(r'^deleteprincipal/(\d+)/$', 'deleteprincipal'),
    url(r'^page-expire/(\d+)/$', "expire"),
    url(r'^paybill/$',"paybill"),
    url(r'^term-status/$',"termenable"),
    url(r'^reportsheet/$',"reportable"),
    url(r'^student-promotion/$',"student_promotion"),
    url(r'^update-calendar/$',"calendar_update"),
    url(r'^online-result/$',"online_result"),
    url(r'^online-statement/$',"online_statement"),
    url(r'^subject-report/$','subject_report'),
    url(r'^subject-reportajax/$', 'subrepajax'),
    url(r'^coco/$','codi'),
    url(r'^autorun/$','autorun'),
    url(r'^getcodi/$','getcodi'),
    url(r'^deletecoco/(\d+)/$', 'deletecoco'),



)
