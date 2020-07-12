# Create your views here.
from django.core.serializers.json import json
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from myproject.setup.models import *
from myproject.student.models import *
from myproject.student.forms import *
from myproject.student.utils import render_to_pdf, render_to_xls
from myproject.sysadmin.admin import *
from myproject.academics.models import *
import datetime
from datetime import date
import xlwt

currse = currentsession.objects.get(id = 1)


def autocomplete(request):
    term = request.GET.get('term')
    #p =  request.GET.get('query')
    #print p
    qset = Student.objects.filter(fullname__contains=term,admitted_session = sessi,gone = False)[:10]

    suggestions = []
    for i in qset:
        suggestions.append({'label': '%s :%s :%s :%s ' % (i.admissionno, i.fullname,i.admitted_class,i.admitted_arm), 'admno': i.admissionno,'name':i.fullname,'klass':i.admitted_class,'arm':i.admitted_arm})
    return suggestions


def index(request):
    return render_to_response('student/base.html', {})

def wel(request):
    if  "userid" in request.session:
        varuser=request.session['userid']
        return render_to_response('student/wel.html',{'varuser':varuser})
    else:
        return HttpResponseRedirect('/login/')

def register(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.studentregistration
        if uenter == False :
            return HttpResponseRedirect('/unauthorised/')
        varerr =''
        form = StudentRegistrationForm()
        if request.method == 'POST':
           form = StudentRegistrationForm(request.POST, request.FILES)
           if form.is_valid():
               birth_date= form.cleaned_data['birth_date']
               admitted_session = form.cleaned_data['admitted_session']
               firstname1 = form.cleaned_data['firstname']
               surname1 = form.cleaned_data['surname']
               othername1 =  form.cleaned_data['othername']
               address = form.cleaned_data['address']
               sex = form.cleaned_data['sex']
               birth_place = form.cleaned_data['birth_place']
               state_of_origin = form.cleaned_data['state_of_origin']
               lga = form.cleaned_data['lga']
               fathername = form.cleaned_data['fathername']
               fatheraddress = form.cleaned_data['fatheraddress']
               fathernumber =  form.cleaned_data['fathernumber']
               fatheroccupation = form.cleaned_data['fatheroccupation']
               fatheremail = form.cleaned_data['fatheremail']
               prev_school =  form.cleaned_data['prev_school']
               prev_class =  form.cleaned_data['prev_class']
               admitted_class = form.cleaned_data['admitted_class']
               admitted_arm = form.cleaned_data['admitted_arm']
               admissionno1 = form.cleaned_data['admissionno']
               house = form.cleaned_data['house']
               dayboarding = form.cleaned_data['dayboarding']
               subclass = form.cleaned_data['subclass']
               rfile = form.cleaned_data['studentpicture']
               getf = str(firstname1)
               getf1 = str(surname1)
               getf2 = str(othername1)
               getf3 = str(admissionno1)
               firstname = getf.replace(':','')
               surname = getf1.replace(':','')
               othername = getf2.replace(':','')
               admissionno = getf3.replace(':','')
               admissionno = admissionno.upper()
               adm = admissionno
               spadm = admitted_session
               j,k = spadm.split("/")
               js = int(k)
               js += 1
               newsession = k + '/' + str(js)
               if rfile is None:
                   studentpicture = 'studentpix/user.png'
               else:
                   studentpicture = request.FILES['studentpicture']
               if Student.objects.filter(admissionno = admissionno).count() == 0:
                   pass
               else:
                   varerr = "Admission No IN EXISTENCE"
                   return render_to_response('student/register.html',{'varerr':varerr,'form':form},context_instance = RequestContext(request))

               import datetime
               today = datetime.datetime.now()
               tm = today.month

               if tm == 9 or tm == 10 or tm == 11 or tm == 12:
                   submit = Student(birth_date= birth_date,admitted_session = admitted_session,first_term = True, second_term = True, third_term = True,firstname = firstname,surname = surname,othername = othername,address = address,sex = sex,birth_place = birth_place,state_of_origin =state_of_origin,lga = lga,fathername =fathername,fatheraddress = fatheraddress,fathernumber = fathernumber,fatheroccupation =fatheroccupation,fatheremail = fatheremail,prev_school =prev_school,prev_class = prev_class,admitted_class = admitted_class,admitted_arm = admitted_arm,admissionno = admissionno,house = house,dayboarding = dayboarding,subclass = subclass,userid = varuser,studentpicture = studentpicture)
                   submit.save()
               if tm == 1 or tm == 2 or tm == 3 or tm == 4:
                   submit = Student(birth_date= birth_date,admitted_session = admitted_session,first_term = False, second_term = True, third_term = True,firstname = firstname,surname = surname,othername = othername,address = address,sex = sex,birth_place = birth_place,state_of_origin =state_of_origin,lga = lga,fathername =fathername,fatheraddress = fatheraddress,fathernumber = fathernumber,fatheroccupation =fatheroccupation,fatheremail = fatheremail,prev_school =prev_school,prev_class = prev_class,admitted_class = admitted_class,admitted_arm = admitted_arm,admissionno = admissionno,house = house,dayboarding = dayboarding,subclass = subclass,userid = varuser,studentpicture = studentpicture)
                   submit.save()
               if tm == 5 or tm == 6 or tm == 7 or tm == 8:
                   submit = Student(birth_date= birth_date,admitted_session = admitted_session,first_term = False, second_term = False, third_term = True,firstname = firstname,surname = surname,othername = othername,address = address,sex = sex,birth_place = birth_place,state_of_origin =state_of_origin,lga = lga,fathername =fathername,fatheraddress = fatheraddress,fathernumber = fathernumber,fatheroccupation =fatheroccupation,fatheremail = fatheremail,prev_school =prev_school,prev_class = prev_class,admitted_class = admitted_class,admitted_arm = admitted_arm,admissionno = admissionno,house = house,dayboarding = dayboarding,subclass = subclass,userid = varuser,studentpicture = studentpicture)
                   submit.save()

               #********************************************************
               #submit1 = Student(birth_date= birth_date,admitted_session = newsession,firstname = firstname,surname = surname,othername = othername,address = address,sex = sex,birth_place = birth_place,state_of_origin =state_of_origin,lga = lga,fathername =fathername,fatheraddress = fatheraddress,fathernumber = fathernumber,fatheroccupation =fatheroccupation,fatheremail = fatheremail,prev_school =prev_school,prev_class = prev_class,admitted_class = admitted_class,admitted_arm = admitted_arm,admissionno = admissionno,house = house,dayboarding = dayboarding,subclass = subclass,userid = varuser,studentpicture =  studentpicture)
               #submit1.save()
               fullname = str(surname) + ' ' + str(firstname) + ' '+ str(othername)

#             ******************* ADD COMPULSORY SUBJECT*********************************
               try:
                   from setup.models import Subject
                   from academics.models import *
                   import datetime
               except:
                    pass
               today = datetime.datetime.now()
               tm = today.month
               akrec = Student.objects.get(admissionno = admissionno, admitted_session = admitted_session)

               if tm == 9 or tm == 10 or tm == 11 or tm == 12 and admitted_session == admitted_session:
                   terrm = ['First', 'Second', 'Third']
                   for term in terrm:
                       akademics = StudentAcademicRecord(student=akrec, klass= akrec.admitted_class,arm= akrec.admitted_arm, term=term, session=akrec.admitted_session)
                       akademics.save()
                       AffectiveSkill(academic_rec=akademics).save()
                       PsychomotorSkill(academic_rec=akademics).save()
                       co = StudentAcademicRecord.objects.get(student=akrec, term = term)
                       #counts no of subjects
                       P = Subject.objects.filter(category = akrec.subclass).count()
                       P = P+1
                       for n in range (1,P):
                           sub = Subject.objects.get(category = akrec.subclass, num = n)
                           if sub.category2 == 'Compulsory':
                               SubjectScore(academic_rec = co, subject = sub.subject, num = n, klass = admitted_class, session = admitted_session, arm = admitted_arm, term = term).save()

               if tm == 1 or tm == 2 or tm == 3 or tm == 4 :#and session == admitted_session:
                   terrm2 = ['Second','Third']
                   for term in terrm2:
                       akademics = StudentAcademicRecord(student=akrec, klass= akrec.admitted_class,arm= akrec.admitted_arm, term=term, session=akrec.admitted_session)
                       akademics.save()
                       AffectiveSkill(academic_rec=akademics).save()
                       PsychomotorSkill(academic_rec=akademics).save()
                       co = StudentAcademicRecord.objects.get(student=akrec, term = term)
                       P = Subject.objects.filter(category =akrec.subclass ).count()
                       P = P+1
                       for n in range (1,P):
                           sub = Subject.objects.get(category = akrec.subclass, num = n)
                           if sub.category2 == 'Compulsory':
                               SubjectScore(academic_rec = co, subject = sub.subject, num = n, klass = admitted_class, session = admitted_session, arm = admitted_arm, term = term).save()
               if tm == 5 or tm == 6 or tm == 7 or tm == 8 and session == admitted_session:
                   terrm3 = ['Third']
                   for term in terrm3:
                       akademics = StudentAcademicRecord(student=akrec, klass= akrec.admitted_class,arm= akrec.admitted_arm, term=term, session=akrec.admitted_session)
                       akademics.save()
                       AffectiveSkill(academic_rec=akademics).save()
                       PsychomotorSkill(academic_rec=akademics).save()
                       co = StudentAcademicRecord.objects.get(student=akrec, term = term)
                       P = Subject.objects.filter(category=akrec.subclass).count()
                       P = P+1
                       for n in range (1,P):
                           sub = Subject.objects.get(category = akrec.subclass, num = n)
                           if sub.category2 == 'Compulsory':
                               SubjectScore(academic_rec = co, subject = sub.subject, num = n, klass = admitted_class, session = admitted_session, arm = admitted_arm, term = term).save()

              ####################ACCOUNT OPENING ###################################

               try:
                   from myproject.ruffwal.rsetup.models import tblaccount
                   used = tblaccount(groupname = "CURRENT ASSETS",groupcode = "30000",subgroupname = "RECEIVABLES",subgroupcode="30200",datecreated = datetime.datetime.today(),userid =varuser,accname = fullname.upper(),acccode = admissionno,accbal= 0,accstatus ="ACTIVE",recreport ="STUDENTS" )
                   used.save()
               except :
                   pass
               if dayboarding == 'Boarding':
                   try:
                       from myproject.ruffwal.rsetup.models import tblaccount
                       #used = tblaccount(groupname = "CURRENT ASSETS",groupcode = "30000",subgroupname = "RECEIVABLES",subgroupcode="30200",datecreated = datetime.datetime.today(),userid =varuser,accname = fullname.upper(),acccode = admissionno,accbal= 0,accstatus ="ACTIVE",recreport ="STUDENTS" )
                       #used.save()
                       used = tblaccount(groupname = "CURRENT LIABILITIES",groupcode = "40000",subgroupname = "STUDENT ACC",subgroupcode="41200",datecreated = datetime.datetime.today(),userid =varuser,accname = fullname.upper(),acccode = 'L' + admissionno,accbal= 0,accstatus ="ACTIVE",recreport ="POCKET" )
                       used.save()
                       used = tblaccount(groupname = "CURRENT LIABILITIES",groupcode = "40000",subgroupname = "STUDENT ACC",subgroupcode="41200",datecreated = datetime.datetime.today(),userid =varuser,accname = fullname.upper(),acccode = 'C' + admissionno,accbal= 0,accstatus ="ACTIVE",recreport ="POCKET" )
                       used.save()
                   except :
                       return HttpResponseRedirect('/student/success/')
               else:
                   return HttpResponseRedirect('/student/success/')
           else:
               varerr = "All Fields Are Required"
           return render_to_response('student/register.html', {'varuser':varuser,'varerr':varerr,'form': form}, RequestContext(request))
        else:
            return render_to_response('student/register.html', {'varuser':varuser,'varerr':varerr,'form': form}, RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')




def register(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.studentregistration
        if uenter == False :
            return HttpResponseRedirect('/unauthorised/')
        varerr =''
        form = StudentRegistrationForm()
        if request.method == 'POST':
           form = StudentRegistrationForm(request.POST, request.FILES)
           if form.is_valid():
               birth_date= form.cleaned_data['birth_date']
               admitted_session = form.cleaned_data['admitted_session']
               firstname1 = form.cleaned_data['firstname']
               surname1 = form.cleaned_data['surname']
               othername1 =  form.cleaned_data['othername']
               address = form.cleaned_data['address']
               sex = form.cleaned_data['sex']
               birth_place = form.cleaned_data['birth_place']
               state_of_origin = form.cleaned_data['state_of_origin']
               lga = form.cleaned_data['lga']
               fathername = form.cleaned_data['fathername']
               fatheraddress = form.cleaned_data['fatheraddress']
               fathernumber =  form.cleaned_data['fathernumber']
               fatheroccupation = form.cleaned_data['fatheroccupation']
               fatheremail = form.cleaned_data['fatheremail']
               prev_school =  form.cleaned_data['prev_school']
               prev_class =  form.cleaned_data['prev_class']
               admitted_class = form.cleaned_data['admitted_class']
               admitted_arm = form.cleaned_data['admitted_arm']
               admissionno1 = form.cleaned_data['admissionno']
               house = form.cleaned_data['house']
               dayboarding = form.cleaned_data['dayboarding']
               subclass = form.cleaned_data['subclass']
               rfile = form.cleaned_data['studentpicture']
               getf = str(firstname1)
               getf1 = str(surname1)
               getf2 = str(othername1)
               getf3 = str(admissionno1)
               firstname = getf.replace(':','')
               surname = getf1.replace(':','')
               othername = getf2.replace(':','')
               admissionno = getf3.replace(':','')
               admissionno = admissionno.upper()
               adm = admissionno
               spadm = admitted_session
               j,k = spadm.split("/")
               js = int(k)
               js += 1
               newsession = k + '/' + str(js)
               if rfile is None:
                   studentpicture = 'studentpix/user.png'
               else:
                   studentpicture = request.FILES['studentpicture']
               if Student.objects.filter(admissionno = admissionno).count() == 0:
                   pass
               else:
                   varerr = "Admission No IN EXISTENCE"
                   return render_to_response('student/register.html',{'varerr':varerr,'form':form},context_instance = RequestContext(request))

               import datetime
               today = datetime.datetime.now()
               tm = today.month

               if tm == 9 or tm == 10 or tm == 11 or tm == 12:
                   submit = Student(birth_date= birth_date,admitted_session = admitted_session,first_term = True, second_term = True, third_term = True,firstname = firstname,surname = surname,othername = othername,address = address,sex = sex,birth_place = birth_place,state_of_origin =state_of_origin,lga = lga,fathername =fathername,fatheraddress = fatheraddress,fathernumber = fathernumber,fatheroccupation =fatheroccupation,fatheremail = fatheremail,prev_school =prev_school,prev_class = prev_class,admitted_class = admitted_class,admitted_arm = admitted_arm,admissionno = admissionno,house = house,dayboarding = dayboarding,subclass = subclass,userid = varuser,studentpicture = studentpicture)
                   submit.save()
               if tm == 1 or tm == 2 or tm == 3 or tm == 4:
                   submit = Student(birth_date= birth_date,admitted_session = admitted_session,first_term = False, second_term = True, third_term = True,firstname = firstname,surname = surname,othername = othername,address = address,sex = sex,birth_place = birth_place,state_of_origin =state_of_origin,lga = lga,fathername =fathername,fatheraddress = fatheraddress,fathernumber = fathernumber,fatheroccupation =fatheroccupation,fatheremail = fatheremail,prev_school =prev_school,prev_class = prev_class,admitted_class = admitted_class,admitted_arm = admitted_arm,admissionno = admissionno,house = house,dayboarding = dayboarding,subclass = subclass,userid = varuser,studentpicture = studentpicture)
                   submit.save()
               if tm == 5 or tm == 6 or tm == 7 or tm == 8:
                   submit = Student(birth_date= birth_date,admitted_session = admitted_session,first_term = False, second_term = False, third_term = True,firstname = firstname,surname = surname,othername = othername,address = address,sex = sex,birth_place = birth_place,state_of_origin =state_of_origin,lga = lga,fathername =fathername,fatheraddress = fatheraddress,fathernumber = fathernumber,fatheroccupation =fatheroccupation,fatheremail = fatheremail,prev_school =prev_school,prev_class = prev_class,admitted_class = admitted_class,admitted_arm = admitted_arm,admissionno = admissionno,house = house,dayboarding = dayboarding,subclass = subclass,userid = varuser,studentpicture = studentpicture)
                   submit.save()

               #********************************************************
               #submit1 = Student(birth_date= birth_date,admitted_session = newsession,firstname = firstname,surname = surname,othername = othername,address = address,sex = sex,birth_place = birth_place,state_of_origin =state_of_origin,lga = lga,fathername =fathername,fatheraddress = fatheraddress,fathernumber = fathernumber,fatheroccupation =fatheroccupation,fatheremail = fatheremail,prev_school =prev_school,prev_class = prev_class,admitted_class = admitted_class,admitted_arm = admitted_arm,admissionno = admissionno,house = house,dayboarding = dayboarding,subclass = subclass,userid = varuser,studentpicture =  studentpicture)
               #submit1.save()
               fullname = str(surname) + ' ' + str(firstname) + ' '+ str(othername)

#             ******************* ADD COMPULSORY SUBJECT*********************************
               try:
                   from setup.models import Subject
                   from academics.models import *
                   import datetime
               except:
                    pass
               today = datetime.datetime.now()
               tm = today.month
               akrec = Student.objects.get(admissionno = admissionno, admitted_session = admitted_session)

               if tm == 9 or tm == 10 or tm == 11 or tm == 12 and admitted_session == admitted_session:
                   terrm = ['First', 'Second', 'Third']
                   for term in terrm:
                       akademics = StudentAcademicRecord(student=akrec, klass= akrec.admitted_class,arm= akrec.admitted_arm, term=term, session=akrec.admitted_session)
                       akademics.save()
                       AffectiveSkill(academic_rec=akademics).save()
                       PsychomotorSkill(academic_rec=akademics).save()
                       co = StudentAcademicRecord.objects.get(student=akrec, term = term)
                       #counts no of subjects
                       P = Subject.objects.filter(category = akrec.subclass).count()
                       P = P+1
                       for n in range (1,P):
                           sub = Subject.objects.get(category = akrec.subclass, num = n)
                           if sub.category2 == 'Compulsory':
                               SubjectScore(academic_rec = co, subject = sub.subject, num = n, klass = admitted_class, session = admitted_session, arm = admitted_arm, term = term).save()

               if tm == 1 or tm == 2 or tm == 3 or tm == 4 :#and session == admitted_session:
                   terrm2 = ['Second','Third']
                   for term in terrm2:
                       akademics = StudentAcademicRecord(student=akrec, klass= akrec.admitted_class,arm= akrec.admitted_arm, term=term, session=akrec.admitted_session)
                       akademics.save()
                       AffectiveSkill(academic_rec=akademics).save()
                       PsychomotorSkill(academic_rec=akademics).save()
                       co = StudentAcademicRecord.objects.get(student=akrec, term = term)
                       P = Subject.objects.filter(category =akrec.subclass ).count()
                       P = P+1
                       for n in range (1,P):
                           sub = Subject.objects.get(category = akrec.subclass, num = n)
                           if sub.category2 == 'Compulsory':
                               SubjectScore(academic_rec = co, subject = sub.subject, num = n, klass = admitted_class, session = admitted_session, arm = admitted_arm, term = term).save()
               if tm == 5 or tm == 6 or tm == 7 or tm == 8 and admitted_session == admitted_session:
                   terrm3 = ['Third']
                   for term in terrm3:
                       akademics = StudentAcademicRecord(student=akrec, klass= akrec.admitted_class,arm= akrec.admitted_arm, term=term, session=akrec.admitted_session)
                       akademics.save()
                       AffectiveSkill(academic_rec=akademics).save()
                       PsychomotorSkill(academic_rec=akademics).save()
                       co = StudentAcademicRecord.objects.get(student=akrec, term = term)
                       P = Subject.objects.filter(category=akrec.subclass).count()
                       P = P+1
                       for n in range (1,P):
                           sub = Subject.objects.get(category = akrec.subclass, num = n)
                           if sub.category2 == 'Compulsory':
                               SubjectScore(academic_rec = co, subject = sub.subject, num = n, klass = admitted_class, session = admitted_session, arm = admitted_arm, term = term).save()

              ####################ACCOUNT OPENING ###################################

               try:
                   from myproject.ruffwal.rsetup.models import tblaccount
                   used = tblaccount(groupname = "CURRENT ASSETS",groupcode = "30000",subgroupname = "RECEIVABLES",subgroupcode="30200",datecreated = datetime.datetime.today(),userid =varuser,accname = fullname.upper(),acccode = admissionno,accbal= 0,accstatus ="ACTIVE",recreport ="STUDENTS" )
                   used.save()
               except :
                   pass
               if dayboarding == 'Boarding':
                   try:
                       from myproject.ruffwal.rsetup.models import tblaccount
                       #used = tblaccount(groupname = "CURRENT ASSETS",groupcode = "30000",subgroupname = "RECEIVABLES",subgroupcode="30200",datecreated = datetime.datetime.today(),userid =varuser,accname = fullname.upper(),acccode = admissionno,accbal= 0,accstatus ="ACTIVE",recreport ="STUDENTS" )
                       #used.save()
                       used = tblaccount(groupname = "CURRENT LIABILITIES",groupcode = "40000",subgroupname = "STUDENT ACC",subgroupcode="41200",datecreated = datetime.datetime.today(),userid =varuser,accname = fullname.upper(),acccode = 'L' + admissionno,accbal= 0,accstatus ="ACTIVE",recreport ="POCKET" )
                       used.save()
                       used = tblaccount(groupname = "CURRENT LIABILITIES",groupcode = "40000",subgroupname = "STUDENT ACC",subgroupcode="41200",datecreated = datetime.datetime.today(),userid =varuser,accname = fullname.upper(),acccode = 'C' + admissionno,accbal= 0,accstatus ="ACTIVE",recreport ="POCKET" )
                       used.save()
                   except :
                       return HttpResponseRedirect('/student/success/')
               else:
                   return HttpResponseRedirect('/student/success/')
           else:
               varerr = "All Fields Are Required"
           return render_to_response('student/register.html', {'varuser':varuser,'varerr':varerr,'form': form}, RequestContext(request))
        else:
            return render_to_response('student/register.html', {'varuser':varuser,'varerr':varerr,'form': form}, RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')

def getlocal(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                # print acccode
                state = acccode
                #print nation,state
                kk = [] #empty dictionary
                data = LGA.objects.filter(state = state).order_by('lga')
                for p in data:
                    kk.append(p.lga)

                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')
"""
#def getadmno(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                # print acccode
                state = acccode
                #print 'the post :',state
                currr = state.split('/')[0]
                dd = []
                if Student.objects.filter().count() == 0 :
                    stno = 0
                else:
                    sdata = Student.objects.filter(admitted_session = state)
                    for j in sdata:
                        sno = j.admissionno
                        curr = sno.split('/')[1]
                        currb= int(curr)
                        dd.append(currb)
                    dd.sort(reverse= True)
                    stno = dd[0]
                stnno = int(stno)
                stnno1 = stnno + 1
                tday = datetime.date.today()
                ty = tday.year
                typ = str(ty)
                tyy = typ[2:]
                #kk = 'SCS/%s/%.4d'%(tyy, stnno1)
                #data = Student.objects.filter(admitted_session = state).count()
                #data +=  1
                #kk = 'SCS/%s/%.4d'%(currr[2:], stnno1) For Skylink
            #    kk = 'LC/%.4d'%stnno1
                kk = 'AC/SEC/%.4d/%s'%(stnno1, tyy)
                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')
"""

def getadmno(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                # print acccode
                state = acccode
                #print 'the post :',state
                currr = state.split('/')[0]
                dd = []
                if Student.objects.filter(admitted_session=currse).count() == 0 :
                    stdno = 0
                else:
                    sdata = Student.objects.filter(admitted_session = state)
                    for j in sdata:
                        sno = j.admissionno
                        curr = sno.split('/')[1]
                        currb= int(curr)
                        dd.append(currb)
                    dd.sort(reverse= True)
                    stdno = dd[0]
                stnno = int(stdno)
                stnno1 = stnno + 1
                tday = datetime.date.today()
                ty = tday.year
                typ = str(ty)
                tyy = typ[2:]
                #kk = 'SCS/%s/%.4d'%(tyy, stnno1)
                #data = Student.objects.filter(admitted_session = state).count()
                #data +=  1
                if Student.objects.filter(admitted_session=currse).count() == 0 :
                    data = 1
                else:
                    data = Student.objects.filter(admitted_session = state).count()
                    data +=  1
                reg = 'BFC/%s/%.4d'%(currr[2:], data)
                #kk = 'AC/%s/%.4d'%(currr[2:], stnno1) #For Skylink
                #kk = 'AC/%.4d'%stnno1
                return HttpResponse(json.dumps(reg), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def getsubclass(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state = acccode
                data = []
                kk = []
                if subclass.objects.filter(subcode = state):
                  data1 = subclass.objects.filter(subcode = state)
                  for j in data1:
                      data.append(j.classsub)
                else:
                    data.append('Nil')

                for p in data:
                    kk.append(p)
                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')



def getstuinfoauto(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                klass,arm,stuname,admno = acccode.split(':')
                lgaorigin = LGA.objects.all()
                getclass = Class.objects.all()
                getarm = Arm.objects.all()
                gethouse = House.objects.all()
                data = Student.objects.get(admitted_class = klass,admitted_arm = arm,admitted_session = currse,fullname = stuname,admissionno = admno)
                return render_to_response('student/regform.html',{'data':data,'lgaorigin':lgaorigin,'getclass':getclass,'getarm':getarm,'gethouse':gethouse,'session':currse})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('student/regform.html',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getstuinfo(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                # print acccode
                klass,arm = acccode.split('-') #split must be same as whats in html
                kk = []
                data = Student.objects.filter(admitted_class = klass,admitted_arm = arm,admitted_session = currse,gone = False).order_by('fullname')
                for p in data:
                    jn = p.fullname+':'+p.admissionno
                    kk.append(jn)
                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def editreg(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.editregistration
        if uenter == False :
            return HttpResponseRedirect('/unauthorised/')
        varerr =''
        if request.method == 'POST':
                birth_date= request.POST['birth_date']
                admitted_session = request.POST['admitted_session']
                firstname1 = request.POST['firstname']
                surname1 = request.POST['surname']
                othername1 =  request.POST['othername']
                address = request.POST['address']
                sex = request.POST['sex']
                birth_place = request.POST['birth_place']
                state_of_origin = request.POST['state_of_origin']
                lga = request.POST['lga']
                fathername = request.POST['fathername']
                fatheraddress = request.POST['fatheraddress']
                fathernumber =  request.POST['fathernumber']
                fatheroccupation = request.POST['fatheroccupation']
                fatheremail = request.POST['fatheremail']
                prev_school =  request.POST['prev_school']
                prev_class =  request.POST['prev_class']
                admitted_class = request.POST['admitted_class']
                admitted_arm = request.POST['admitted_arm']
                admissionno1 = request.POST['admissionno']
                house = request.POST['house']
                dayboarding = request.POST['dayboarding']
                subclass = request.POST['subclass']
                admissionnoold = request.POST['admissionnoold']
                oldclass = request.POST['oldclass']
                oldarm = request.POST['oldarm']
                oldname = request.POST['oldname']
                getf = str(firstname1)
                getf1 = str(surname1)
                getf2 = str(othername1)
                getf3 = str(admissionno1)
                firstname = getf.replace(':','')
                surname = getf1.replace(':','')
                othername = getf2.replace(':','')
                admissionno = getf3.replace(':','')
                admissionno = admissionno.upper()
                if 'studentpicture' in request.FILES:
                    photo_file = request.FILES['studentpicture']
                    k1 = str(photo_file.name)
                    j = k1.split('.')[1]
                     #print k,j
                    if not (j.lower() in ['jpeg','jpg','png','bmp']):
                       varerr = "%s is not a required picture" % k1
                       getdetails = Student.objects.get(admissionno = admissionnoold,admitted_session = currse)
                       return render_to_response('student/edit_reg.html',{'varerr':varerr,'form': form,'searchform': searchform})
                    else:
                       pass
                else:
                    gda =  Student.objects.get(admissionno = admissionnoold,admitted_session = currse)
                    # print gda.picture
                    photo_file = gda.studentpicture

                if Student.objects.filter(admissionno = admissionno).exclude(admissionno = admissionnoold).count() == 0:
                    pass
                else:
                    varerr = "Error in your request !! - Another Student with Admission No  %s IN EXISTENCE" %admissionno
                    return render_to_response('student/edit_reg.html',{'varerr':varerr,'form': form,'searchform': searchform},context_instance = RequestContext(request))
                if  birth_date == "" or admitted_session == "" or firstname == "" or surname == "" or address == "" or birth_place == "" or fathername == "" or fatheraddress == "" or fatheroccupation == "" or   admissionno == "" :
                    varerr = "ALL FIELDS ARE REQUIRED"
                    return render_to_response('student/edit_reg.html',{'varerr':varerr,'form': form,'searchform': searchform},context_instance = RequestContext(request))
                #getting the old student details
                #oldrecord = Student.objects.get(admitted_session = currse,admitted_class= oldclass,admitted_arm = oldarm,fullname = oldname)
                # getting class for the new class
                seldata = Student.objects.get(admitted_session = currse,admitted_class= oldclass,admitted_arm = oldarm,fullname = oldname)
                oldrec = seldata
                seldata. birth_date= birth_date
                seldata.address = address
                seldata.firstname = firstname
                seldata.surname = surname
                seldata.othername = othername
                seldata.address = address
                seldata.sex = sex
                seldata.birth_place = birth_place
                seldata.state_of_origin = state_of_origin
                seldata.lga = lga
                seldata.fathername =fathername
                seldata.fatheraddress= fatheraddress
                seldata.fathernumber = fathernumber
                seldata.fatheroccupation = fatheroccupation
                seldata.fatheremail = fatheremail
                seldata.prev_school = prev_school
                seldata.prev_class = prev_class
                seldata.admitted_class = admitted_class
                seldata.admitted_arm = admitted_arm
                seldata.admissionno = admissionno
                seldata.house = house
                seldata.dayboarding = dayboarding
                seldata.subclass = subclass
                seldata.userid = varuser
                seldata.studentpicture = photo_file #*******why pic doesnt update
                seldata.save()
                #*************************************
                spadm = admitted_session
                j,k = spadm.split("/")
                js = int(k)
                js += 1
                #here i need to update the academic records
                stacarec = StudentAcademicRecord.objects.filter(student = oldrec)
                StudentAcademicRecord.objects.filter(student = oldrec).update(arm = admitted_arm,klass = admitted_class)
                for k in stacarec:
                   SubjectScore.objects.filter(academic_rec = k).update(klass = admitted_class,arm = admitted_arm)
                # here i need to update the account table
                fullname =  str(surname) +' '+ str(firstname) + ' '+ str(othername)
                if tblaccount.objects.filter(acccode = admissionno):
                    getacc = tblaccount.objects.get(acccode = admissionno)
                    #getacc.acccode = admissionno
                    getacc.accname = fullname.upper()
                    getacc.save()
                    #update transaction table
                    tbltransaction.objects.filter(acccode = admissionnoold).update(acccode = admissionno,accname = fullname.upper())
                else:
                    used = tblaccount(groupname = "CURRENT ASSETS",groupcode = "30000",subgroupname = "RECEIVABLES",subgroupcode="30200",datecreated = datetime.datetime.today(),userid =varuser,accname = fullname.upper(),acccode = admissionno,accbal= 0,accstatus ="ACTIVE",recreport ="STUDENTS" )
                    used.save()
                #updating the liabilities
                if tblaccount.objects.filter(acccode = 'L'+str(admissionno)):
                    getacc = tblaccount.objects.get(acccode = 'L'+str(admissionno))
                    #getacc.acccode = 'L'+str(admissionno)
                    getacc.accname = fullname.upper()
                    getacc.save()
                    #update transaction table
                    tbltransaction.objects.filter(acccode = 'L'+str(admissionnoold)).update(acccode = 'L'+str(admissionno),accname = fullname.upper())
                else:
                    used = tblaccount(groupname = "CURRENT LIABILITIES",groupcode = "40000",subgroupname = "STUDENT ACC",subgroupcode="41200",datecreated = datetime.datetime.today(),userid =varuser,accname = fullname.upper(),acccode = 'L' + admissionno,accbal= 0,accstatus ="ACTIVE",recreport ="POCKET" )
                    #used.save()
                #treating other liabilities
                if tblaccount.objects.filter(acccode = 'C'+str(admissionno)):
                    getacc = tblaccount.objects.get(acccode = 'C'+str(admissionno))
                    #getacc.acccode = 'C'+str(admissionno)
                    getacc.accname = fullname.upper()
                    getacc.save()
                    #update transaction table
                    tbltransaction.objects.filter(acccode = 'C'+str(admissionnoold)).update(acccode = 'C'+str(admissionno),accname = fullname.upper())
                else:
                    used = tblaccount(groupname = "CURRENT LIABILITIES",groupcode = "40000",subgroupname = "STUDENT ACC",subgroupcode="41200",datecreated = datetime.datetime.today(),userid =varuser,accname = fullname.upper(),acccode = 'C' + admissionno,accbal= 0,accstatus ="ACTIVE",recreport ="POCKET" )
                   # used.save()
                return HttpResponseRedirect('/student/success/')
        else:
            form = StudentRegistrationForm
            searchform = StudentSearchForm()
            return render_to_response('student/edit_reg.html', {'varuser':varuser,'form': form,'searchform': searchform}, RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

def studentreport(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.studentreport
        if uenter == False :
            return HttpResponseRedirect('/unauthorised/')
        varerr =''
        form = studentreportform()
        school = get_object_or_404(School, pk=1)
        student =''
        if request.method == 'POST':
            form = studentreportform(request.POST, request.FILES)
            if form.is_valid():
                session= form.cleaned_data['session']
                klass= form.cleaned_data['klass']
                arm = form.cleaned_data['arm']
                dayboarding = form.cleaned_data['dayboarding']
                filtermethod = form.cleaned_data['filtermethod']
                disclass =''
                disarm = ''
                #excelfile
                if filtermethod == 'Class':
                   student = Student.objects.filter(admitted_class = klass,admitted_session = session,gone = False).order_by('admitted_arm','-sex')
                   disclass = klass
                elif filtermethod == 'Classroom':
                    student = Student.objects.filter(admitted_class = klass,admitted_arm = arm,admitted_session = session,gone = False).order_by('-sex','fullname')
                    disclass = klass
                    disarm = arm
                elif filtermethod=='Day/Boarding':
                    student = Student.objects.filter(admitted_class = klass,admitted_arm = arm,admitted_session = session,dayboarding = dayboarding,gone = False).order_by('-sex','fullname')
                    disclass = klass
                # for k in student:
                #   p1,p2=k.fathernumber.split(',')




                if form.cleaned_data['excelfile']:
                    response = HttpResponse(mimetype="application/ms-excel")
                    response['Content-Disposition'] = 'attachment; filename=studentlist.xls'
                    wb = xlwt.Workbook()
                    ws = wb.add_sheet('studentlist')
                    ws.write(0, 4, school.name)
                    ws.write(1, 4, school.address)
                    ws.write(2, 2, '%s %s :: Student List for %s Session' %(disclass,disarm, session) )
                    ws.write(3, 0, 'Name')
                    ws.write(3, 1, 'Sex')
                    ws.write(3, 2, 'Admission No')
                    ws.write(3, 3, 'Class')
                    ws.write(3, 4, 'Arm')
                    ws.write(3, 5, 'House')
                    ws.write(3, 6, 'Day/Boarding')
                    ws.write(3, 7, 'Phone Number')
                    ws.write(3, 8, 'E-Mail')
                    k = 4
                    for jd in student:
                       ws.write(k, 0, jd.fullname)
                       ws.write(k, 1, jd.sex)
                       ws.write(k, 2, jd.admissionno)
                       ws.write(k, 3, jd.admitted_class)
                       ws.write(k, 4, jd.admitted_arm)
                       ws.write(k, 5, jd.house)
                       ws.write(k, 6, jd.dayboarding)
                       ws.write(k, 7, jd.fathernumber)
                       ws.write(k, 8, jd.fatheremail)
                       k += 1
                    wb.save(response)
                    return response
                else:
                    return render_to_response('student/student_list.html', {
                      # 'p1':p1,'p2':p2,
                      'form': form,'school':school,'varuser':varuser,'students_list':student,'session':session,'disclass':disclass,'disarm':disarm}, RequestContext(request))
            else:
                 varerr = 'All Fields Are Required !'
                 return render_to_response('student/student_list.html', {'form': form,'school':school,'varerr':varerr}, RequestContext(request))
        else:
            form = studentreportform()
            return render_to_response('student/student_list.html', {'varuser':varuser,'form': form,'school':school}, RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

def withdrawajax(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                # print acccode
                klass,arm,stuname,admno = acccode.split(':')
                lgaorigin = LGA.objects.all()
                # stateoforigin = LGA.objects.all().distinct('state').order_by('state')
                #for j in stateoforigin:
                #   print j
                getclass = Class.objects.all()
                getarm = Arm.objects.all()
                gethouse = House.objects.all()
                data = Student.objects.get(admitted_class = klass,admitted_arm = arm,admitted_session = currse,fullname = stuname,admissionno = admno)
                return render_to_response('student/regform1.html',{'data':data,'lgaorigin':lgaorigin,'getclass':getclass,'getarm':getarm,'gethouse':gethouse,'session':currse})
            else:
                gdata = ""
                return render_to_response('student/regform1.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('student/regform1.html',{'gdata':gdata})


##**********WITHDRAW STUDENT BUTTON***************###########
def withdrawstudent(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.withdraw
        if uenter == False :
            return HttpResponseRedirect('/unauthorised/')
        varerr =''
        form = StudentRegistrationForm
        searchform = StudentSearchForm()

        if request.method == 'POST':
            admissionnoold = request.POST['admissionnoold']
            reason = request.POST['reason']
            datewithdrawal = request.POST['datewithdrawal']
            if reason =='' or datewithdrawal =='':
                varerr = "It is required you state both the reason and date of withdrawal date"
                return render_to_response('student/withdraw.html',{'varerr':varerr,'form': form,'searchform': searchform},context_instance = RequestContext(request))
            stuinfo = Student.objects.get(admissionno = admissionnoold,admitted_session = currse)
            submit = WithdrawnStudent(student = stuinfo.fullname,klass = stuinfo.admitted_class,arm = stuinfo.admitted_arm,admissionno = stuinfo.admissionno,reason = reason,date_withdrawn = datewithdrawal,userid = varuser,admitted_session = currse)
            stuinfo.gone = True
            stuinfo.save()
            submit.save()


  #       import datetime
  #          today = datetime.datetime.now()
  #          tm = today.month
  #          if tm == 9 or tm == 10 or tm == 11 or tm == 12: #first term
  #              stuinfo.gone = True
  #              stuinfo.first_term = False
  #              stuinfo.second_term = False
  #              stuinfo.third_term = False
  #              term = 'First'
  #              stuinfo.save()
  #          if tm == 1 or tm == 2 or tm == 3 or tm == 4: #second term
  #              stuinfo.gone = True
  #              stuinfo.second_term = False
  #              stuinfo.third_term = False
  #              term = 'Second'
  #              stuinfo.save()
  #          if tm == 5 or tm == 6 or tm == 7 or tm == 8: #third term
  #              stuinfo.gone = True
  #              stuinfo.first_term = True
  #              stuinfo.second_term = True
  #              stuinfo.third_term = False
  #              term = 'Third'
  #              stuinfo.save()

            #deletig academi records
  #          akademics = StudentAcademicRecord(student=stuinfo, klass= stuinfo.admitted_class,arm= stuinfo.admitted_arm, term=term, session=stuinfo.admitted_session)
  #          akademics.save()
  #          AffectiveSkill(academic_rec=akademics).save()
  #          PsychomotorSkill(academic_rec=akademics).save()
  #          co = StudentAcademicRecord.objects.get(student=akrec, term = term)

            #TREATING THE ACCOUNT


            return HttpResponseRedirect('/student/success/')

        else:
            form = StudentRegistrationForm
            searchform = StudentSearchForm()
            return render_to_response('student/withdraw.html', {'varuser':varuser,'form': form,'searchform': searchform}, RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')


def returngonestudent(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.returngonestudent
        if uenter == False :
            return HttpResponseRedirect('/unauthorised/')
        varerr =''
        form = StudentRegistrationForm
        searchform = StudentSearchForm()

        if request.method == 'POST':
        #form = StudentRegistrationForm(request.POST, request.FILES)
        #if form.is_valid():
            admissiono = request.POST['admissiono']
            reason = request.POST['reason']
            datewithdrawal = request.POST['datewithdrawal']
            if reason =='' or datewithdrawal =='':
                varerr = "Reason for withdrawal/withdrawal date is required"
                return render_to_response('student/returngoneform.html',{'varerr':varerr,'form': form,'searchform': searchform},context_instance = RequestContext(request))
            stuinfo = Student.objects.get(admissionno = admissiono,admitted_session = currse)
            stuinfo.gone = False
            stuinfo.save()
            WithdrawnStudent.objects.get(admissionno = admissiono,admitted_session = currse).delete()
            return HttpResponseRedirect('/student/success/')

        else:

            form = StudentRegistrationForm
            searchform = StudentSearchForm()
            return render_to_response('student/returngoneform.html', {'varuser':varuser,'form': form,'searchform': searchform}, RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

def getstuinfogone(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                # print acccode
                klass,arm = acccode.split('-')
                #print klass,arm

                kk = []
                data = WithdrawnStudent.objects.filter(klass = klass,arm = arm,admitted_session = currse).order_by('student')
                for p in data:
                    jn = p.student+':'+p.admissionno
                    kk.append(jn)
                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def returnajax(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                # print acccode
                klass,arm,stuname,admno = acccode.split(':')
                lgaorigin = LGA.objects.all()
                # stateoforigin = LGA.objects.all().distinct('state').order_by('state')
                #for j in stateoforigin:
                #   print j
                getclass = Class.objects.all()
                getarm = Arm.objects.all()
                gethouse = House.objects.all()
                data = WithdrawnStudent.objects.get(klass = klass,arm = arm,admitted_session = currse,student = stuname,admissionno = admno)
                return render_to_response('student/regform2.html',{'data':data,'lgaorigin':lgaorigin,'getclass':getclass,'getarm':getarm,'gethouse':gethouse,'session':currse})
            else:
                gdata = ""
                return render_to_response('student/regform2.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('student/regform2.html',{'gdata':gdata})

def withdrawnreport(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.withdrawnreport
        if uenter == False :
            return HttpResponseRedirect('/unauthorised/')
        varerr =''
        form = withdrawnreportform()
        school = get_object_or_404(School, pk=1)
        student =''
        if request.method == 'POST':
            form = withdrawnreportform(request.POST, request.FILES)
            if form.is_valid():
                withdrawsession= form.cleaned_data['withdrawsession']
                student_list = []
                jclass = Class.objects.all()
                for klass in jclass:
                    student = WithdrawnStudent.objects.filter(klass = klass,admitted_session = withdrawsession).order_by('admissionno')
                    stdic = {'klass':klass,'student':student}
                    student_list.append(stdic)
                #student = Student.objects.filter(admitted_class = klass,admitted_arm = arm,admitted_session = currse,dayboarding = dayboarding).order_by('sex','fullname')
                #disclass = klass
                #for u in student_list:
                 #   print u['klass']
                if form.cleaned_data['excelfile']:
                    response = HttpResponse(mimetype="application/ms-excel")
                    response['Content-Disposition'] = 'attachment; filename=withdranw_list.xls'
                    wb = xlwt.Workbook()
                    ws = wb.add_sheet('withdrawn_list')
                    ws.write(0, 1, school.name)
                    ws.write(1, 1, school.address)
                    ws.write(2, 2, ' Student  Withdrawn List for %s Session' %withdrawsession )
                    ws.write(3, 0, 'Name')
                    ws.write(3, 1, 'Admission No')
                    ws.write(3, 2, 'Class')
                    ws.write(3, 3, 'Arm')
                    ws.write(3, 4, 'Reason for Withdrawal')
                    ws.write(3, 5, 'Date Withdrawn')
                    k = 4
                    for jk in student_list :
                        ff = jk['klass']
                        #print ff
                        ws.write(k, 0, '%s' %ff)
                        k +=1
                        for jd in jk['student']:
                            ws.write(k, 0, jd.student)
                            ws.write(k, 1, jd.admissionno)
                            ws.write(k, 2, jd.klass)
                            ws.write(k, 3, jd.arm)
                            ws.write(k, 4, jd.reason)
                            ws.write(k, 5, jd.date_withdrawn.strftime("%d-%m-%Y"))
                            k += 1
                    wb.save(response)
                    return response
                else:
                    return render_to_response('student/withdrawn_report.html', {'form': form,'school':school,'students_list':student_list,'session':withdrawsession}, RequestContext(request))

        else:
            form = withdrawnreportform()

            return render_to_response('student/withdrawn_report.html', {'varuser':varuser,'form': form,'school':school}, RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

def searchstudent(request,vid):
    if  "userid" in request.session:
      stuinfo = Student.objects.get(id = vid)
      return render_to_response('student/search.html',{'data':stuinfo})
    else:
        return HttpResponseRedirect('/login/')


def searchprofile(request):
    if  "userid" in request.session:
      user = request.session['userid']
      stuinfo = Student.objects.get(fullname = user,admitted_session=currse)
      return render_to_response('student/profile.html',{'data':stuinfo,'varuser':user})
    else:
        return HttpResponseRedirect('/login/')


def studentsuccessful(request):
    return render_to_response('student/success.html', {}, RequestContext(request))


def get_report(request, type='student'):
    '''gets a report on a given model defined by type. returns html, pdf or xls.
    type can be either student or withdrawn. if type is student the additional filter arg
    defines queryset filter to select. filter keys are klass, arm, dayboarding'''
    format = request.GET.get('format', 'html')
    school = get_object_or_404(School, pk=1)

    if type == 'student':
        filter = {'gone': False}

        if request.GET.get('class'):
            filter.update({'admitted_class': request.GET.get('class')})
        if request.GET.get('arm'):
            filter.update({'admitted_arm': request.GET.get('arm')})
        if request.GET.get('boarding'):
            filter.update({'dayboarding': True})

        queryset = Student.objects.filter(**filter)
        title = 'List of Students'
        template = 'student/student_list.html'

    elif type == 'withdrawn':
        queryset = Student.objects.filter(gone=True)
        title = 'List of Withdrawn Students'
        template = 'student/withdrawn_student_list.html'

    context = {'students_list': queryset, 'report_title': title, 'school': school}

    if format == 'html':
        return render_to_response(template, context)
    elif format == 'pdf':
        render_to_pdf(template, context)
    elif format == 'xls':
        render_to_xls(context)
    else: return Http404


# Wrapper to make a view handle both normal and api request
def json_view(func):
    def wrap(req, *args, **kwargs):
        resp = func(req, *args, **kwargs)
        if isinstance(resp, HttpResponse):
            return resp
        return HttpResponse(json.dumps(resp), mimetype="application/json")

    return wrap

@json_view
def autocomplete(request, gone=False):
    term = request.GET.get('term')

    qset = Student.objects.filter(fullname__icontains=term, gone=gone)[:15]

    suggestions = []
    for i in qset:
        suggestions.append({'label': '%s %s %s' % (i.fullname, i.admitted_class, i.admitted_arm), 'value': i.pk})
    return suggestions

@json_view
def get_lga_as_list(request, state=None):
    lgas = LGA.objects.filter(state__iexact=state)
    lga_list = []

    for lga in lgas:
        lga_list.append(lga.lga)

    lga_list.sort()
    return lga_list

#************function for student search ****************
def studentsearchajax(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                post = request.POST.copy()
                acccode = post['userid']
                if acccode=='':
                  return render_to_response("namesearch.html")
                else:
                  data = Student.objects.filter(admitted_session = currse,fullname__contains = acccode,gone = False)
                  return render_to_response('student/sear.htm',{'data':data,'session':currse})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('student/sear.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def studentsearchajax1(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                post = request.POST.copy()
                acccode = post['userid']
                data = Student.objects.filter(admitted_session = currse,admissionno__contains = acccode,gone = False)
                return render_to_response('student/sear.htm',{'data':data,'session':currse})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('student/sear.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


