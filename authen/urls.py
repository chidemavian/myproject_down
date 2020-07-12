
from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView, TemplateView
urlpatterns = patterns('myproject.authen.views',


    ###****questions************
    url(r'^signup/new/$', 'signup'),
    url(r'^enter/image/(\d+)/$', 'cbtimage'),
   url(r'^activate/user/$', 'activate'),
   # url(r'^login/me/$', 'mylogin'),
   url(r'^login/student/$','studentlogin'),
    url(r'^subject/choice/$', 'ssubchoice'),

    )