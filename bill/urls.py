
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('myproject.bill.views',
    # Examples:
    url(r'^billname/$', 'addexpensesname'),
    url(r'^wel/$', 'wel'),
    url(r'^deleteexpense/(\d+)/$', 'deleteexpensesname'),
    url(r'^billsetup/$', 'billsetup'),
    url(r'^setupajax/$', 'billsetupajax'),
    url(r'^deletebillajax/(\d+)/$', 'deletebillajax'),
    url(r'^additionalbill/$', 'additionalbill'),
    url(r'^findstudent/$', 'autocomplete'),
    url(r'^addajax/$', 'billaddsetupajax'),
    url(r'^deleteaddbill/(\d+)/$', 'deleteaddbillajax'),
    url(r'^printbill/$', 'printbill'),
    url(r'^getstudent/$', 'getstuinfoajax'),
    url(r'^billschedule/$', 'printbillschdule'),
    url(r'^findacc/$', 'autocompletenameacc'),
    url(r'^printoldbill/$', 'printoldbill'),
    url(r'^getbill/$', 'genbill'),
    url(r'^update_calendar/$', 'bill_calendar_update'),
    url(r'^repoint-account/$', 'repoint_account'),#to convert our liabilities account to Income Account

    )
