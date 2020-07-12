
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('myproject.assessment.views',
    # Examples:
    url(r'^enterca/$', 'enterca'),#Continueous Assessment for Secondary School
    url(r'^ca_comments/$','commentca'),
    url(r'^getclass/$', 'getclass'),
    url(r'^stucacom/$','stucom'),
    url(r'^student/my_subjects/$','mysubjects'),
    url(r'^student/my_subject_page/$','mysubjectpage'),
    url(r'^student/my_results/$','my_results'),
    url(r'^student/my_results_page/$','my_results_page'),
    url(r'^student/myassess/$', 'myassess'),
    url(r'^sn/class_notes/$', 'stunotes'),
    url(r'^sn/pq/$', 'pq'),
    url(r'^student/mybills/$', 'mybills'),
    # url(r'^lib/choose/$', 'options'),
    url(r'^student/printmybills/$', 'printmybill'),
    url(r'^student/mystudykit/$', 'mystudykit'),
    url(r'^student/mycomm/$', 'mycomm'),
    url(r'^student/ca_student/$', 'castudent'),
    url(r'^wel/$', 'wel'),
  

    url(r'^class_list/$', 'classlist'),
    url(r'^half_term/$', 'halfterm'),

    url(r'^getmycourse/$', 'hgkvkuu'),
    url(r'^stucourseform/$', 'stucourseform'),               

    url(r'^getarm/$', 'getarm'),
    url(r'^getarmgrp/$', 'getarmgroup'),
    url(r'^getterm/$', 'getterm'),
    url(r'^getsubject/$', 'getsubject'),
    url(r'^getstusubject/$', 'getstusubject'),
    url(r'^getsubjectless/$', 'getsubjectlesson'),
    url(r'^getstudent/$', 'getstudent'),
    url(r'^getassign/$', 'getassign'),
    url(r'^editca/(\d+)/$', 'editca'),
    
    url(r'^editcas2/(\d+)/$', 'editcas2'),  #End term magana***************

    url(r'^editcas1/(\d+)/$', 'editcas1'),   #mid term magana***************
   
    url(r'^teacherrport/$', 'teacher_report'),
    url(r'^editcap/(\d+)/$', 'editcapry'),
    url(r'^getsubjectscore/$', 'getsubjectscore'),
    url(r'^getsubjectscore1/$', 'getsubjectscore1'),
    url(r'^getsubjectscore2/$', 'getsubjectscore2'),
    url(r'^getsubjectscorep/$', 'getsubjectscorep'),
    url(r'^getclassaff/$', 'getclassaff'),
    url(r'^getarmaff/$', 'getarmaff'),    
    url(r'^affective/$', 'affectivedomain'),
    url(r'^courseform/(\d+)/$', 'studentcourseform'),
    url(r'^getstudentaff/$', 'getstudentaff'),
    url(r'^classlist/$', 'getstudentlist'),
    url(r'^getcomment/$', 'getcomment'),
    url(r'^comment/$', 'getcomm'),
    url(r'^getmycomment/$', 'comment'),
    url(r'^getstucomment/$', 'getcomment'),
    url(r'^getstucommentca/$', 'getcommentca'),
    url(r'^getaffective/$', 'getaffective'),
    url(r'^getpsyco/$', 'getpsyco'),
    url(r'^getsubgroup/$', 'changesubgrp'),
    url(r'^editgrp/(\d+)/$', 'editsubgrp'),


    url(r'^editcomment/(\d+)/$', 'editcomment'),
    url(r'^editcommentca1/(\d+)/$','editcommentca1'),
    url(r'^editcommentca2/(\d+)/$','editcommentca2'),
    url(r'^editpsyco/(\d+)/$', 'editpsyco'),
    url(r'^editaffective/(\d+)/$', 'editaffective'),
    url(r'^addsubject/$', 'addsubject'),
    url(r'^getstudentsubject/$', 'getstudentsubject'),
    url(r'^getsubject4student/$', 'getsubject4student'),
    url(r'^getmoresubject/$', 'getmoresubject'),
    url(r'^getmorestudentsubject/$', 'getmorestudentsubject'),
    url(r'^addmoresubject/$', 'addmoresubject'),
    url(r'^deletemoresubject/$', 'deletemoresubject'),
    url(r'^confirmdeletemoresubject/(\d+)/$', 'confirmdeletemoresubject'),
    url(r'^principalcomment/$', 'principalcomment'),
    url(r'^getstudentprinicipalcomment/$', 'getstudentprincipalcomment'),
    url(r'^getprinicipalcomment/$', 'getprincipalcomment'),
    url(r'^editcommentprin/(\d+)/$', 'editcommentprin'),
    url(r'^getstudentacademic/$', 'getstudentacademic'),
    url(r'^entercapry/$', 'addsubject4pry'),#Continueous Assessment for Primary School
    url(r'^primary_assessment/(\w+)/(\w+)/(\w+)/(\w+)/(\w+)/$', 'primary_url'),#primary school redirecting
    
    # url(r'^secondary_assessment/(\w+)/(\w+)/(\w+)/(\w+)/(\w+)/$', 'secondary_url'),#secondary school redirecting

    url(r'^secondary_assessment/(\w+)/(\w+)/(\w+)/(\w+)/(\w+)/(\w+)/(\w+)/$', 'secondary_url'),#secondary school redirecting

    url(r'^secondary_print_assessment/(\w+)/(\w+)/(\w+)/(\w+)/(\w+)/(\w+)/$', 'secondary_teacher_report'),#secondary school redirecting

    url(r'^secondary_cf/(\w+)/(\w+)/(\w+)/$', 'secondary_cf'),# cf redirecting for secondary

    url(r'^getsubject4studentpry/$', 'getsubject4studentpry'),
    url(r'^getclassaffpry/$', 'getclassaffpry'),
    url(r'^reportsheet/$', 'reportsheet'),
    url(r'^reportopt/$', 'reportopt'),
    url(r'^indreport/$', 'indreport'),
    url(r'^mid-term-report/$', 'reportsheetmidterm'),
    url(r'^broadsheet/$', 'broadsheet'),
    url(r'^mid-term-broadsheet/$', 'mid_term_broadsheet'),
    url(r'^access-denied/$', 'unautho'),

    
)