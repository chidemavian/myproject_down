
from django.conf.urls.defaults import patterns, url

from myproject.lesson.views import *

urlpatterns = patterns('myproject.lesson.views',
    # Examples:
    url(r'^wel/$', 'wel'),
  #*********set up topic******************
    url(r'^set_up/$', 'settopic'),
    url(r'^set_up/topic=&?/$', 'settopic'),
    url(r'^set_up/gettopajax/$', 'topajax'),
    url(r'^set_up/delete/(\d+)/$', 'deletetopiccode'),
    
    #*********set up content******************
    url(r'^setup_sub/$', 'setsub'),
    url(r'^setup_sub/subtopicajaxxxxxx/$', 'filsubtop'),
    url(r'^setup_sub/entercont/$', 'entercont'),
    url(r'^setup_sub/entercontent/(\d+)/$', 'cont'),
    url(r'^setup_sub/delete/(\d+)/$', 'deletecon'),


    #*********set up objectives******************    
    url(r'^set_up/obj/$', 'setobj'),
    url(r'^set_up/obj/subobjajax/$', 'filobj'),
    url(r'^set_up/obj/objajax/$','obj'),
    url(r'^set_up/obj/objajax/(\d+)/$', 'enterobj'),
    url(r'^set_up/obj/delete/(\d+)/$', 'deleteobj'),


#*********set up instructional resources*****************
    url(r'^set_up/resources/$', 'setresource'),
    url(r'^set_up/resources/resajax/$', 'resajax'),
    url(r'^set_up/resources/enterir/$','enterir'),
    url(r'^set_up/resources/enterir/(\d+)/$','irajax'),
    url(r'^set_up/resources/delete/(\d+)/$','deleteir'),

    
 #*********set up teacher activities*****************   
    url(r'^set_up/teacher_activities/$', 'tactivities'),
    url(r'^set_up/teacher_activities/tajax/$', 'tajax'),
    url(r'^set_up/teacher_activities/enajax/$', 'entajax'),
    url(r'^set_up/teacher_activities/enajax/(\d+)/$', 'saveta'),
    url(r'^set_up/teacher_activities/delete/(\d+)/$', 'deleteta'),
#*********set up students activities*****************
    url(r'^set_up/students_activities/$', 'sactivities'),
    url(r'^set_up/students_activities/sajax/$', 'sajax'),
    url(r'^set_up/students_activities/ensajax/$', 'ensajax'),
    url(r'^set_up/students_activities/ensajax/(\d+)/$', 'savesa'),
    url(r'^set_up/students_activities/delete/(\d+)/$', 'deletesa'),
#*********EVALUATION*****************
    url(r'^set_up/evaluation/$', 'seteva'),
    url(r'^set_up/evajax/$', 'fileva'),
    url(r'^set_up/eva/evajax/$','eva'),
    url(r'^set_up/eva/evajjax/(\d+)/$', 'entereva'),
    url(r'^set_up/evaluation/delete/(\d+)/$', 'deleteva'),
   #*********lesson count*****************
    url(r'^set_up/lesson_count/$','lesscount'),
    url(r'^set_up/lesson_count/getwa/$','wajax'),
    url(r'^set_up/lesson_count/entwa/$', 'enterwa'),
    url(r'^set_up/lesson_count/entwa/(\d+)/$', 'editwa'),
  #********Lesson Note***********************
    url(r'^note/$', 'setupmynote'),
    url(r'^note/getnote/$','notajax'),
    url(r'^note/upload/(\d+)/$','uploadnote'),
    url(r'^note/view/(\d+)/$','viewnote'),
    url(r'^note/edit/(\d+)/$','reviewnote'),
    #********Questions Bank ***********************
    url(r'^ExamQuest/$','examquests'),
    url(r'^ExamQuest/getquest/$', 'getexamquest'),
    url(r'^ExamQuest/view/(\d+)/$','downquest'),
    url(r'^ExamQuest/upload/(\d+)/$','upquest'),
    url(r'^ExamQuest/newupload/(w+)/(w+)/(w+)/(w+)/$','upquestnew'),
#**************Lesson Plan***************
    url(r'^plan/$', 'setupmyplan'),

#**************Admin***************
    # url(r'^admin/$', 'admins'),

 )
