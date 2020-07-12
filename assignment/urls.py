
from django.conf.urls.defaults import patterns, url



urlpatterns = patterns('myproject.assignment.views',
    # Examples:
    url(r'^assignment/$', 'choose'),
    url(r'^t/pa/$', 'assignment'),
    url(r'^s/pj/$', 'studassign'),

    )
