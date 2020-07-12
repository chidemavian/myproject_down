from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView, TemplateView
from myproject.student import models

urlpatterns = patterns('myproject.student.views',
    # Examples:
    url(r'^$', 'index'),
    url(r'^register/$', 'register'),
    url(r'^admno/$', 'getadmno'),
    url(r'^wel/$', 'wel'),
    url(r'^subclass/$', 'getsubclass'),
    url(r'^findstudent/$', 'autocomplete'),
   # url(r'^edit/$', 'edit_registration'),
   # url(r'^withdraw/$', 'withdraw_student'),
   # url(r'^return/$', 'return_withdrawn_student'),
    url(r'^ajaxlga/$', 'getlocal'),
    url(r'^editregistration/$', 'editreg'),
    url(r'^studentinfo/$', 'getstuinfo'),
    url(r'^autopost/$', 'getstuinfoauto'),
    url(r'^studentreport/$', 'studentreport'),
    #url(r'^studentreportpdf/$', 'studentreppdf'),
    url(r'^withdraw_student/$', 'withdrawstudent'),
    url(r'^withdrawajax/$', 'withdrawajax'),
    url(r'^student_return/$', 'returngonestudent'),
    url(r'^studentinfogone/$', 'getstuinfogone'),
    url(r'^returnajax/$', 'returnajax'),
    url(r'^withdrawn_report/$', 'withdrawnreport'),
    url(r'^success/$', 'studentsuccessful'),
    url(r'^search/(\d+)/$', 'searchstudent'),
    url(r'^profile/$', 'searchprofile'),
    url(r'^search_ajax/$', 'studentsearchajax'),
    url(r'^search_ajax1/$', 'studentsearchajax1'),



   # url(r'^report/student/$', TemplateView.as_view(template_name='student/student_report.html')),
    #url(r'^report/student/list/$', 'get_report'),
    #url(r'^report/student/(?P<pk>\d+)/$', DetailView.as_view(template_name='student/student_detail.html', model=models.Student)),
    #url(r'^report/withdrawn/$', TemplateView.as_view(template_name='student/withdrawn_report.html')),
    #url(r'^report/withdrawn/list/$', 'get_report', {'type': 'withdrawn'}),

    #url(r'^find/$', 'autocomplete'),
    #url(r'^find/gone/$', 'autocomplete', {'gone': True}),
    #url(r'^getlga/(?P<state>\w+)/$', 'get_lga_as_list'),

    #url(r'^getform/$', 'edit_registration', {'is_ajax': True}),
    #url(r'^getform/return/$', 'return_withdrawn_student', {'is_ajax': True}),
    #url(r'^getform/withdraw/$', 'withdraw_student', {'is_ajax': True}),

    #url(r'success/$', TemplateView.as_view(template_name='student/success.html')),
)
