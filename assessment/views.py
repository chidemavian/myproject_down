# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from django.core.serializers.json import json
from myproject.assessment.forms import *
from myproject.academics.models import *
from myproject.CBT.models import *
from myproject.sysadmin.models import *
from myproject.setup.models import *
from myproject.bill.utils import *
from myproject.assessment.getordinal import *
from myproject.assessment.utils import *
from myproject.assessment.bsheet import *
from myproject.lesson.models import *
from myproject.utilities.views import *


from django.db.models import Max,Sum
from myproject.assignment.models import *
import datetime
from datetime import date
import locale
locale.setlocale(locale.LC_ALL,'')
import xlwt
import decimal

currse = currentsession.objects.get(id = 1)

sublists=[]

date=datetime.date.today()

exam_type=tblcbtexams.objects.get(status='ACTIVE')
exam_type=exam_type.exam_type
def wel(request):
    if  "userid" in request.session:
        varuser=request.session['userid']
        return render_to_response('assessment/success.html',{'varuser':varuser})
    else:
        return HttpResponseRedirect('/login/')


def mysubjects(request):
    if 'userid' in request.session:
        varuser=request.session['userid']
        if request.method=='POST':
            form = studentform(request.POST)
            return HttpResponseRedirect("/assessment/student/my_subject_page/")

        else:
            form= studentform()
        return render_to_response('assessment/subjectpage.html',{'form':form,'varuser':varuser})
    else:
        return HttpResponseRedirect('/login/')


def mysubjectpage(request):
    if 'userid' in request.session:
        varuser=request.session['userid']
        if request.method=='POST':
            form = stuform(request.POST)
            if form.is_valid():
                session=form.cleaned_data['session']
                term = form.cleaned_data['term']
                try:
                    chk=tblcf.objects.get(session=session,term=term)
                    chkdate = chk.deadline
                except:
                    chkdate = date
                #if date<= chkdate:
                #    return render_to_response('assessment/checkback.html',{'ckk':chkdate})
                data=Student.objects.get(fullname=varuser.upper(),admitted_session=currse,gone=False)
                replist=[]
                if StudentAcademicRecord.objects.get(student=data,term=term):
                    acaderec=StudentAcademicRecord.objects.filter(student=data,term=term)
                    subsco=SubjectScore.objects.filter(academic_rec=acaderec).order_by('subject_teacher')
                    return render_to_response('assessment/mysubjects.html',{'getdetails':subsco,
                        'varuser':varuser,
                        'data':data,
                        'term':term,
                        'stuid':data.id,
                        'ckk':chkdate})
    else:
        return HttpResponseRedirect('/login/')


def my_results_page(request):
    if 'userid' in request.session:
        varuser=request.session['userid']
        if request.method=='POST':
            form = stuform(request.POST)
            if form.is_valid():
                session=form.cleaned_data['session']
                term = form.cleaned_data['term']
                try:
                    chk=tblresult.objects.get(session=session,term=term)
                except:
                    varerr= 'Date not set, contact your home room teacher'
                    return render_to_response('assessment/notset.html',{'varerr':varerr})
                chkdate = chk.deadline
                if date < chkdate:
                    return render_to_response('assessment/checkback.html',{'ckk':chkdate})
                else:
                    data=Student.objects.get(fullname=varuser.upper(),admitted_session=currse,gone=False)
                    varerr =''
                    getdetails =''
                    # school = get_object_or_404(School, pk=1)
                    school=School.objects.get(id =1)

                    try:
                      codi = ClassTeacher.objects.get(klass=data.admitted_class,session=session,teachername='N/A')
                    except:
                      codi = 'NOT AVAILABLE'
                    replist = []
                    varbeg = data.admitted_class[0]
                    getgrading = gradingsys.objects.filter(classsub__startswith = varbeg)
                    classtot = 0
                    totsub = 0
                    totalmarkcount = 0
                    stuno1 = Student.objects.filter(admitted_session = data.admitted_session,
                        first_term = 1, 
                        admitted_class = data.admitted_class,
                        admitted_arm = data.admitted_arm,
                        gone = False).count()
                    acaderec = StudentAcademicRecord.objects.get(student = data.id,term = term)
                    psycho = PsychomotorSkill.objects.get(academic_rec = acaderec)  
                    subsco = SubjectScore.objects.filter(academic_rec = acaderec).order_by('num')
                    totsub = SubjectScore.objects.filter(academic_rec = acaderec).count()

                    totalmark2 = 0
                    totalmark = SubjectScore.objects.filter(academic_rec = acaderec).aggregate(Sum('end_term_score'))
                    totalmark2 = totalmark['end_term_score__sum']
                    rtotal = int(totalmark2) #total of term scores from all subject 

                    jdic = {'studentinfo':data,'codi':codi, 'psyco':psycho,'academic':acaderec,'subject':subsco,'totalmark':rtotal}
                    replist.append(jdic)                            
                return render_to_response('assessment/my_results.html',{'varuser':varuser,'school':school,'date':date, 'varerr':varerr,'replist':replist,'term':term,'stuno1':stuno1,})
    else:
        return HttpResponseRedirect('/login/')



def myassess(request):
    if 'userid' in request.session:
        varuser=request.session['userid']
        form= studentform()
        return render_to_response('assessment/myassess.html',{'form':form,'varuser':varuser})
    else:
        return HttpResponseRedirect('/login/')


def stunotes(request):
    if 'userid' in request.session:
        varuser=request.session['userid']
        varerr='Lesson Notes'
        if request.method=='POST':
            form= myform(request.POST)
            # varerr='varerr'
            if form.is_valid():
                session=form.cleaned_data['session']
                term=form.cleaned_data['term']
                subject= form.cleaned_data['subject']
                data= Student.objects.get(admitted_session=session,fullname= varuser,gone=False)
                klass=data.admitted_class
                sett = tbltopic.objects.filter(klass = data.admitted_class,term = term, subject = subject)
                questions=[]
                for qst in sett:
                    sub=qst.subject
                    topic=qst.topic
                    note=str(qst.lessonnote)
                    note=note.split('/')[-1]
                    sett={'sub':sub,'topic':topic,'note':note}
                    questions.append(sett)
                return render_to_response('assessment/notes.html',{'sett':questions,'varuser':varuser ,'varerr':varerr, 'session':session,'term':term,'klass':klass,'subject':subject})
        else:
            form= myform()
        return render_to_response('assessment/stunotes.html',{'form':form,'varuser':varuser,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')


def getstusubject(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                session,term,varuser= acccode.split(':')
                kk = []
                sdic = {}
                stu = Student.objects.get(admitted_session=session,gone=False,fullname= varuser)
                acadec = StudentAcademicRecord.objects.get(student=stu,term=term)
                data = SubjectScore.objects.filter(academic_rec=acadec).order_by('subject')
                for j in data:
                    j = j.subject
                    s = {j:j}
                    sdic.update(s)
                klist = sdic.values()
                for p in klist:
                   # print 'The Subject :',p
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


def classlist(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        try:
            user = ClassTeacher.objects.get(username = varuser)
        except:
            if ClassTeacher.objects.filter(teachername = varuser).count() == 0 :
                return HttpResponseRedirect('/assessment/access-denied/')
        user = userprofile.objects.get(username = varuser)
        varerr =''
        getdetails =''
        form = caform()
        # term=term
        return render_to_response('assessment/classlist.html',{'varuser':varuser,'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')


def halfterm(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        try:
            user = ClassTeacher.objects.get(teachername = varuser)
        except:
            return HttpResponseRedirect('/assessment/access-denied/')
        varerr =''
        getdetails =''
        school=School.objects.get(id =1)
        if request.method == 'POST':
            form = reportsheetform(request.POST)
            if form.is_valid():
                session = form.cleaned_data['session']
                klass = form.cleaned_data['klass']
                term = form.cleaned_data['term']
                arm = form.cleaned_data['arm']

                if term=='First':
                    stuinfo = Student.objects.filter(first_term=True,admitted_session = session, 
                        admitted_class = klass, admitted_arm = arm, gone = False).order_by('fullname')
                elif term == 'Second':
                    stuinfo = Student.objects.filter(second_term=True,admitted_session = session,
                        admitted_class = klass, admitted_arm = arm, gone = False).order_by('fullname')
                elif term == 'Third':
                    stuinfo = Student.objects.filter(third_term=True,admitted_session = session,
                     admitted_class = klass, admitted_arm = arm, gone = False).order_by('fullname')
                try:
                  codi = ClassTeacher.objects.get(klass=klass,session=session,teachername='N/A')
                except:
                  codi='Not Available'

                replist = []
                varbeg = klass[0]


                for j in stuinfo: #students in a class
                    totsub = 0
                    acaderec = StudentAcademicRecord.objects.get(student = j,term = term)
                    psycho = PsychomotorSkill.objects.get(academic_rec = acaderec)
                    subsco = SubjectScore.objects.filter(academic_rec = acaderec,term=term).order_by('num')
                    totsub = SubjectScore.objects.filter(academic_rec = acaderec).count()
                    msublist = []
                    stustat=[]

                    stave=acaderec.stu_ave1 * 5
                    clave =acaderec.class_ave1 * 5

                    stat={'stave':stave,'clave':clave}
                    stustat.append(stat)

######......................grade each subject...............................
                    for jj in subsco:
                        mymid = jj.mid_term_score * 5
                        if varbeg == 'S':
                            remark = seniorgrade(float(mymid))                                    
                        elif varbeg=='J':
                            remark = juniorgrade(float(mymid))
                        msub = {'subject':jj.subject,
                        'mid_term':mymid,
                        'totalperc':locale.format("%.0f",mymid,grouping=True),
                        'remark':remark['remark'],
                        'grade':remark['grade'],
                        'teacher':jj.subject_teacher}
                        msublist.append(msub)                    

                    #****************all i need in report******************************
                    jdic = {'date':date,
                    'codi':codi,
                    'studentinfo':j,
                    'stat':stustat,
                    'pyscho':psycho,
                    'academic':acaderec,
                    'subject':msublist,
                    'school':school}
                    replist.append(jdic)

                return render_to_response('assessment/midmid.html',{'session':session, 
                    'form':form,
                    'varuser':varuser,
                    'varerr':varerr,
                    'replist':replist,
                    'term':term})

        else:
           form = reportsheetform()
        return render_to_response('assessment/halfterm.html',{'varuser':varuser,'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')


def getstudentlist(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                session,klass,arm,term = acccode.split(':')
                getstu = Student.objects.filter(admitted_class = klass,admitted_arm=arm,admitted_session = session,gone = False).order_by('fullname')
                return render_to_response('assessment/myclasslist.html',{'data':getstu,'term':term})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def stucourseform(request):
    if 'userid' in request.session:
        if request.is_ajax():
            if request.method=='POST':
                varuser=request.session['userid']
                post=request.POST.copy()
                acccode=post['userid']
                adm,term=acccode.split(':')                
                getstu=Student.objects.get(admissionno=adm,admitted_session=currse,gone=False)
                rec=StudentAcademicRecord.objects.get(student=getstu,term=term)
                sub=SubjectScore.objects.filter(academic_rec=rec)
                return render_to_response('assessment/studentcf.html',{'getdetails':sub,'term':term})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')



def studentcourseform(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        getstu = Student.objects.get(id=vid, admitted_session=currse,gone=False)
        teach= ClassTeacher.objects.get(teachername=varuser)
        form= cfform()
        if teach.klass==getstu.admitted_class:                
            term = tblterm.objects.filter(status='ACTIVE')
            tr=[]
            for t in term:
                t=t.term
                tr.append(t)
            if StudentAcademicRecord.objects.filter(student = getstu):#,term = term):
               comm = StudentAcademicRecord.objects.filter(student = getstu)#,term = term)
               getdetails = SubjectScore.objects.filter(session = currse,klass = getstu.admitted_class, arm =getstu.admitted_arm,academic_rec = comm).order_by('num')
            return render_to_response('assessment/subgroup.html',{'form':form,'term':tr,'session':currse,'varuser':varuser,'getdetails':getdetails,'stuid':getstu.id,'getstu':getstu})
        else:
            return HttpResponseRedirect('/assessment/access-denied/')
    
    else:
        return HttpResponseRedirect('/login/')

def hgkvkuu(request,vid):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method=='POST':                
                varuser = request.session['userid']
                varerr =""
                post=request.POST.copy()
                acccode= post['userid']
                vid,term=acccode.split(':')
                getstu = Student.objects.get(id=vid, admitted_session=currse)
                if StudentAcademicRecord.objects.filter(student = getstu,term = term):
                   comm = StudentAcademicRecord.objects.get(student = getstu,term = term)
                   getdetails = SubjectScore.objects.filter(session = currse,klass = getstu.admitted_class, arm = getsu.admitted_arm,term = term,academic_rec = comm).order_by('num')
                   return render_to_response('assessment/studentcf.html',{'varuser':varuser,'data':getdetails,'stuid':getstu.id,'fullname':getstu.fullname})
        else:
            HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')

def pq(request):
    if 'userid' in request.session:
        varuser=request.session['userid']
        varerr='Past Questions'
        if request.method=='POST':   
            form= mypqform(request.POST)
            if form.is_valid():
                session=form.cleaned_data['session']
                term=form.cleaned_data['term']
                subject= form.cleaned_data['subject']
                klass= form.cleaned_data['klass']         
                if Student.objects.get(admitted_session=session,fullname=varuser,gone=False):
                    sett = tblquest.objects.filter(klass = klass,term = term, session=session,subject = subject)
                    questions=[]
                    for qst in sett:
                        sub=qst.subject
                        qst=str(qst.question)
                        qst=qst.split('/')[-1]
                        sett={'sub':sub,'qst':qst}
                        questions.append(sett)
                    return render_to_response('assessment/pq.html',{'sett':questions,'varuser':varuser ,'varerr':varerr, 'session':session,'term':term,'klass':klass,'subject':subject})
        else:

            form= mypqform()
        return render_to_response('assessment/stupq.html',{'form':form,'varuser':varuser,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')


def my_results(request):
    if 'userid' in request.session:
        varuser=request.session['userid']
        form= studentform()
        return render_to_response('assessment/resultpage.html',{'form':form,'varuser':varuser})
    else:
        return HttpResponseRedirect('/login/')


def castudent(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method=='POST':                
                varuser = request.session['userid']
                varerr =''
                getdetails =''
                post= request.POST.copy()
                acccode=post['userid']
                term,session,ca = acccode.split(':')
                school=School.objects.get(id =1)
                stuinfo = Student.objects.get(admitted_session = session,fullname=varuser,gone = False)

                try:
                  codi = ClassTeacher.objects.get(klass=stuinfo.admitted_class,session=session,teachername='N/A')
                except:
                  codi = 'Not Entered'

                if ca == '1st Ca':
                    replist = []
                    varbeg = stuinfo.admitted_class[0]
                    acaderec = StudentAcademicRecord.objects.get(student = stuinfo,term = term)
                    psycho = PsychomotorSkill.objects.get(academic_rec = acaderec)
                    subsco = SubjectScore.objects.filter(academic_rec = acaderec).order_by('num')
                    totsub = SubjectScore.objects.filter(academic_rec = acaderec).count()
                    msublist = []
                    for jj in subsco:
                        fca = jj.first_ca
                        totalperc1 = fca/20
                        totalperc = totalperc1 * 100
                        if varbeg == 'S':
                            remark = seniorgrade(float(totalperc))                                    
                        else:
                            remark = juniorgrade(float(totalperc))

                        msub = {'subject':jj.subject,'first_ca':fca,'totalperc':locale.format("%.1f",totalperc,grouping=True),'remark':remark['remark'],'grade':remark['grade'],'teacher':jj.subject_teacher}
                        msublist.append(msub)
                        #****************all i need in report******************************
                    jdic = {'date':date,'codi':codi,'studentinfo':stuinfo,'academic':acaderec,'pyscho':psycho,'subject':msublist}
                    replist.append(jdic)
                    return render_to_response('assessment/myassessajax.html',{'session':session,'varuser':varuser,'varerr':varerr,'replist':replist,'school':school,'term':term})

                elif ca == '2nd Ca':
                    replist = []
                    varbeg = stuinfo.admitted_class[0]
                    acaderec = StudentAcademicRecord.objects.get(student = stuinfo,term = term)
                    psycho = PsychomotorSkill.objects.get(academic_rec = acaderec)
                    subsco = SubjectScore.objects.filter(academic_rec = acaderec).order_by('num')
                    totsub = SubjectScore.objects.filter(academic_rec = acaderec).count()
                    msublist = []
                    for jj in subsco:
                        sca = jj.second_ca
                        totalperc1 = sca/20
                        totalperc = totalperc1 * 100
                        if varbeg == 'S':
                            remark = seniorgrade(float(totalperc))                                    
                        else:
                            remark = juniorgrade(float(totalperc))

                        msub = {'subject':jj.subject,'second_ca':sca,'totalperc':locale.format("%.1f",totalperc,grouping=True),'remark':remark['remark'],'grade':remark['grade'],'teacher':jj.subject_teacher}
                        msublist.append(msub)
                        #****************all i need in report******************************
                    jdic = {'date':date,'codi':codi,'studentinfo':stuinfo,'academic':acaderec,'pyscho':psycho,'subject':msublist}
                    replist.append(jdic)

                    return render_to_response('assessment/stuassess.html',{'session':session,'varuser':varuser,'varerr':varerr,'replist':replist,'school':school,'term':term})

                else:
                    return render_to_response('index.html')
        else:
            return render_to_response('index.html')
    else:
        return HttpResponseRedirect('/login/')


def mybills(request):
    if 'userid' in request.session:
        varuser=request.session['userid']
        form= studentform()
        return render_to_response('assessment/mybills.html',{'form':form,'varuser':varuser})
    else:
        return HttpResponseRedirect('/login/')

def printmybill(request):
    if 'userid' in request.session:
        varuser = request.session['userid']
        varerr = ''
        getdetails = ''
        school = get_object_or_404(School, pk = 1)
        if request.method == 'POST':
            form = stuform(request.POST)
            if form.is_valid():
                session = form.cleaned_data['session']
                term = form.cleaned_data['term']
                bill_list = []
                # studata = Student.objects.filter(fullname =varuser, admitted_session = session, gone = False)
                studata = Student.objects.get(fullname =varuser, admitted_session = session, gone = False)
                varrid2 = 0
                getaddbill = ''
                billlist = []
                if tblbill.objects.filter(klass = studata.admitted_class, term = term, dayboarding = studata.dayboarding).count() == 0:
                    varrid = 0
                else:
                    getbill = tblbill.objects.filter(klass = studata.admitted_class, term = term, dayboarding = studata.dayboarding)
                    varrid1 = tblbill.objects.filter(klass = studata.admitted_class, term = term, dayboarding = studata.dayboarding).aggregate(Sum('billamount'))
                    varrid = varrid1['billamount__sum']
                    for j in getbill:
                        billdic = {
                            'desc': j.desc,
                            'billamount': locale.format('%.2f', j.billamount, grouping = True) }
                        billlist.append(billdic)

                if tbladditionalbill.objects.filter(session = session, admissionno = studata.admissionno, klass = studata.admitted_class, term = term).count() == 0:
                    varrid2 = 0
                    getaddbill = ''
                else:
                    getaddbill = tbladditionalbill.objects.filter(session = session, admissionno = studata.admissionno, klass = studata.admitted_class, term = term)
                    varrid11 = tbladditionalbill.objects.filter(session = session, admissionno = studata.admissionno, klass = studata.admitted_class, term = term).aggregate(Sum('billamount'))
                    varrid2 = varrid11['billamount__sum']
                    for h in getaddbill:
                        billdic = {
                            'desc': h.desc,
                            'billamount': locale.format('%.2f', h.billamount, grouping = True) }
                        billlist.append(billdic)

                varrid = varrid + varrid2
                billdic = {
                    'student': studata,
                    'bill': billlist,
                    'totalbill': locale.format('%.2f', varrid, grouping = True) }
                bill_list.append(billdic)
                

                return render_to_response('assessment/billreport.html',{'varuser':varuser, 'varerr':varerr,'bill_list':bill_list,'school':school,'session':session,'term':term,'klass':studata.admitted_class})

        # return render_to_response('bill/printbill.html',{'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')


def mystudykit(request):
    if 'userid' in request.session:
        varuser=request.session['userid']
        form= studentform()
        return render_to_response('assessment/mystudykit.html',{'form':form,'varuser':varuser})
    else:
        return HttpResponseRedirect('/login/')

def mycomm(request):
    if 'userid' in request.session:
        varuser=request.session['userid']
        data=Student.objects.get(fullname=varuser,admitted_session=currse,gone=False)
        assignment=tblassignment.objects.filter(session=data.admitted_session,klass=data.admitted_class).order_by('submit_on','id')

        # form= studentform()
        return render_to_response('assignment/assignment.html',{'data':assignment,'varuser':varuser})
    else:
        return HttpResponseRedirect('/login/')


def unautho(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =''
        return render_to_response('assessment/unautorise.htm',{'varerr':varerr,'varuser':str(varuser).upper()})
    else:
        return HttpResponseRedirect('/login/')






def enterca(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        if subjectteacher.objects.filter(teachername = varuser).count() == 0 :
            return HttpResponseRedirect('/assessment/access-denied/')
        varerr =''
        sec = ''
        pry = ''
        for j in appused.objects.all():
            pry = j.primary
            sec = j.secondary
        if sec is True :
            pass
        else:
            return HttpResponseRedirect('/assessment/access-denied/')
        if request.method == 'POST':
            form = caform(request.POST) # A form bound to the POST data
            if form.is_valid():
                session = form.cleaned_data['session']
                klass = form.cleaned_data['klass']
                term = form.cleaned_data['term']
                arm = form.cleaned_data['arm']
                subject = form.cleaned_data['subject']
                reporttype = form.cleaned_data['reporttype']

                return HttpResponseRedirect('/assessment/secondary_print_assessment/%s/%s/%s/%s/%s/%s/'%(str(session).replace('/','j'),str(klass).replace(' ','k'),str(arm).replace(' ','k'),str(subject).replace(' ','k'),str(reporttype).replace(' ','w'),str(term).replace(' ','0')))
        else:
            form = caform()
        return render_to_response('assessment/enterca.html',{'varuser':varuser,'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')



def teacher_report(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        if subjectteacher.objects.filter(teachername = varuser).count() == 0 :
            return HttpResponseRedirect('/assessment/access-denied/')
        varerr =''
        sec = ''
        pry = ''
        school=School.objects.get(id =1)
        for j in appused.objects.all():
            pry = j.primary
            sec = j.secondary
        if sec is True :
            pass
        else:
            return HttpResponseRedirect('/assessment/access-denied/')
        if request.method == 'POST':
            form = caform(request.POST)
            if form.is_valid():
                session = form.cleaned_data['session']
                klass = form.cleaned_data['klass']
                term = form.cleaned_data['term']
                arm = form.cleaned_data['arm']
                subject = form.cleaned_data['subject']
                stu=Student.objects.filter(admitted_session=session,admitted_class=klass,admitted_arm=arm,gone=False)
                replist=[]
                for j in stu:
                        acadec= StudentAcademicRecord.objects.filter(student=j,term=term)
                        for recf in acadec:                          
                            rec=SubjectScore.objects.filter(academic_rec=recf,
                                subject=subject)
                            reca={'rec':rec,'stu':j}
                            replist.append(reca)        
            return render_to_response('assessment/scoresheet.html',{'varuser':varuser,'school':school,'session':session,'term':term, 'date':date,'form':form,'subject':subject,'class':klass,'replist':replist})
        else:
            form = caform()
        return render_to_response('assessment/scoresheet.html',{'varuser':varuser,'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')



def commentca(request):
    if  "userid" in request.session:
        varuser=request.session['userid']
        if ClassTeacher.objects.filter(teachername = varuser).count() == 0 :
            return HttpResponseRedirect('/assessment/access-denied/')
        varerr=''
        form = cacomform()
        return render_to_response('assessment/entcom.html',{'varuser':varuser,'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')


def stucom(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                session,klass,arm,term,ca = acccode.split(':')
                #print klass
                data = []
                getstu = Student.objects.filter(admitted_class = klass,admitted_arm=arm,admitted_session = session,gone = False).order_by('-sex','fullname')
                for p in getstu:
                    if StudentAcademicRecord.objects.filter(student = p,term = term):
                        comm = StudentAcademicRecord.objects.get(student = p,term = term)
                        affec = AffectiveSkill.objects.get(academic_rec = comm)
                        psyco = PsychomotorSkill.objects.get(academic_rec = comm)
                        stdic = {'studentinfo':p,'comment':comm,'affective':affec,'psyco':psyco}
                        data.append(stdic)

                if ca=='Mid term':
                    return render_to_response('assessment/comca.html',{'ca':ca,
                    'klass':klass,'data':data,'session':session,'term':term,'arm':arm
                    })
                elif ca=='End term':
                    return render_to_response('assessment/comment.html',{'ca':ca,
                    'klass':klass,'data':data,'session':session,'term':term,'arm':arm
                    })


            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')









def getclass(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state = acccode
                kk = []
                sdic = {}

                data = subjectteacher.objects.filter(teachername = varuser,status = 'ACTIVE',session = state).order_by('klass')
                for j in data:
                    j = j.klass
                    s = {j:j}
                    sdic.update(s)

                data1= groupteacher.objects.filter(teachername = varuser,status = 'ACTIVE',session = state).order_by('klass')
                for j in data1:
                    j = j.klass
                    s = {j:j}
                    sdic.update(s)

                klist = sdic.values()
                for p in klist:
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








def getarm(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                session,klass = acccode.split(':')
                kk = []
                sdic = {}
                data = subjectteacher.objects.filter(teachername = varuser,status = 'ACTIVE',session = session,klass = klass).order_by('arm')
                for j in data:
                    j = j.arm
                    #print j
                    s = {j:j}
                    sdic.update(s)
                klist = sdic.values()

                for p in klist:
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

def getarmgroup(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                session,klass = acccode.split(':')
                kk = []
                sdic = {}
                data = subjectteacher.objects.filter(teachername = varuser,status = 'ACTIVE',session = session,klass = klass).order_by('arm')
                for j in data:
                    j = j.arm
                    #print j
                    s = {j:j}
                    sdic.update(s)

                data1 = groupteacher.objects.filter(teachername = varuser,status = 'ACTIVE',session = session,klass = klass).order_by('group')
                for j in data1:
                    j = j.group
                    #print j
                    s = {j:j}
                    sdic.update(s)

                klist = sdic.values()

                for p in klist:
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


def getmyterm(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state = acccode
                kk = []
                sdic = {}
                data = subjectteacher.objects.filter(teachername = varuser,status = 'ACTIVE',session = state).order_by('term')
                for j in data:
                    j = j.term
                    #print j
                    s = {j:j}
                    sdic.update(s)
                klist = sdic.values()
                klist.sort()
                for p in klist:
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







def getterm(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state = acccode
                kk = []
                sdic = {}
                term=tblterm.objects.get(status='ACTIVE')
                term=term.term
                data = subjectteacher.objects.filter(teachername = varuser,status = 'ACTIVE',session = state,term=term)
                for j in data:
                    j = j.term
                    #print j
                    s = {j:j}
                    sdic.update(s)
                klist = sdic.values()
                klist.sort()
                for p in klist:
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


def getsubject(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                #state = acccode
                #print acccode
                session,klass,arm,term = acccode.split(':')
                kk = []
                sdic = {}
                data = subjectteacher.objects.filter(teachername = varuser,status = 'ACTIVE',session = session,klass = klass,arm = arm)
                for j in data:
                    j = j.subject
                    #print j
                    s = {j:j}
                    sdic.update(s)

                data1 = groupteacher.objects.filter(teachername = varuser,status = 'ACTIVE',session = session,klass = klass,group = arm)
                for j in data1:
                    j = j.subject
                    #print j
                    s = {j:j}
                    sdic.update(s)


                klist = sdic.values()
                for p in klist:
                   # print 'The Subject :',p
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


def getsubjectlesson(request):
    if "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr = ""
                post = request.POST.copy()
                acccode = post['userid']
               # state = acccode
                session,klass = acccode.split(':')
                kk = []
                sdic = {}
                data = subjectteacher.objects.filter(teachername = varuser,session=session,klass = klass)
                for j in data:
                    j = j.subject
                    s = {j:j}
                    sdic.update(s)
                kk = sdic.values()
                sublists=kk
                #klist = sdic.values()
                #for p in klist:
                #    kk.append(p)
                return HttpResponse(json.dumps(kk),mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def getstudent(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                session,klass,arm,term, subject,reporttype= acccode.split(':')
                stlist = []
                
                if term == 'Third':
                    tday = datetime.date.today()
                    if tday.year < 2212:
                        if tblpin.objects.filter(ydate__year = tday.year):
                           gdate = tblpin.objects.get(ydate__year = tday.year)
                           if tday < gdate.ydate:
                              pass
                           else:
                              gpin = gdate.pin
                              gused = gdate.used
                              k = decrypt1(str(gused))
                              uu = encrypt(k)
                              if str(gpin) == str(uu):
                                 pass
                              else:
                                 return HttpResponseRedirect('/sysadmin/page-expire/%s/'%int(tday.year))
                    else:
                         return HttpResponseRedirect('/sysadmin/page-expire/%s/'%int(tday.year))
                else:
                    pass

                data2 = subjectteacher.objects.filter(teachername = varuser,
                    status = 'ACTIVE',
                    klass=klass,
                    arm=arm,
                    term=term,
                    subject=subject,
                    session = session).count()

                if data2 > 0:

                    try:
                        Arm.objects.get(arm=arm)

                        for j in Student.objects.filter(admitted_session = session,admitted_class = klass,admitted_arm = arm,gone = False):
                            if StudentAcademicRecord.objects.filter(student = j,session = session,term = term):
                                st = StudentAcademicRecord.objects.get(student = j,session = session,term = term)
                                if SubjectScore.objects.filter(academic_rec = st,klass = klass,subject = subject,session = session,arm=arm,term =term):
                                    gs = SubjectScore.objects.get(academic_rec = st,klass = klass,subject = subject,session = session,arm=arm,term =term)
                                    kk = {'id':gs.id,
                                    'admissionno':j.admissionno,
                                    'fullname':j.fullname,
                                    'sex':j.sex,
                                    'subject':gs.subject,
                                    'term':str(term),
                                    'first_ca':gs.first_ca,
                                    'second_ca':gs.second_ca,
                                    'third_ca':gs.third_ca,
                                    'fourth_ca':gs.fourth_ca,
                                    'fifth_ca':gs.fifth_ca,
                                    'sixth_ca':gs.sixth_ca,
                                    'klass':gs.klass,                                    
                                    'arm':gs.arm,
                                    'exam_score':gs.end_term_score}
                                    stlist.append(kk)
                                else:
                                    pass
                    except:
                        for j in Student.objects.filter(admitted_session = session,admitted_class = klass,gone = False):
                            if StudentAcademicRecord.objects.filter(student = j,session = session,term = term):
                                st = StudentAcademicRecord.objects.get(student = j,session = session,term = term)
                                if SubjectScore.objects.filter(academic_rec = st,klass = klass,subject = subject,session = session,subject_group=arm,term =term):
                                    gs = SubjectScore.objects.get(academic_rec = st,klass = klass,subject = subject,session = session,subject_group=arm,term =term)
                                    kk = {'id':gs.id,
                                    'admissionno':j.admissionno,
                                    'fullname':j.fullname,
                                    'sex':j.sex,
                                    'subject':gs.subject,
                                    'term':str(term),
                                    'first_ca':gs.first_ca,
                                    'second_ca':gs.second_ca,
                                    'third_ca':gs.third_ca,
                                    'fourth_ca':gs.fourth_ca,
                                    'fifth_ca':gs.fifth_ca,
                                    'sixth_ca':gs.sixth_ca,
                                    'klass':gs.klass,
                                    'arm':gs.arm,
                                    'exam_score':gs.end_term_score}
                                    stlist.append(kk)
                                else:
                                    pass
                    if reporttype=='Mid term':
                        # if klass=='JS 1' or klass== 'SS 1':
                        return render_to_response('assessment/mid.html',{'data':stlist,'subject':subject,'term':term,'klass':klass,'arm':arm,'report':reporttype})
                        # else:
                        #     return render_to_response('assessment/ca_first.html',{'data':stlist})
                    elif reporttype=='End term':
                        # if klass=='JS 1' or klass== 'SS 1':
                        return render_to_response('assessment/endterm.html',{'data':stlist,'subject':subject,'term':term,'klass':klass,'arm':arm,'report':reporttype})
                        # else:
                        #     return render_to_response('assessment/ca_first.html',{'data':stlist})

                else:
                    varerr='User not asigned'
                    return render_to_response('assessment/notallowed.html',{'varerr':varerr})

            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def getassign(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
                session,klass,arm,term, subject= acccode.split(':')
                myassign=tblassignment.objects.filter(teacher=varuser,session=session,term=term,klass=klass,arm=arm,subject=subject)
                return HttpResponse(json.dumps(kk), mimetype='application/json')
                # return render_to_response('assignment/tview.html',{'data':myassign})
                
    else:
        return HttpResponseRedirect('/login/')



def editca(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.staffname
        sec = ''
        pry = ''
        for j in appused.objects.all():
            pry = j.primary
            sec = j.secondary
        if sec is True :
            pass
        else:
            return HttpResponseRedirect('/assessment/access-denied/')
        varerr =''
        getdetails = SubjectScore.objects.get(id = vid)
        admno1 = getdetails.academic_rec.student.admissionno
        klass1 = getdetails.klass
        arm1 = getdetails.arm
        subject1 = getdetails.subject
        session1 = getdetails.session
        term1 = getdetails.term
        if request.method == 'POST':
             ca1 = request.POST['firstca']
             ca2 = request.POST['secondca']
             ca3 = request.POST['thirdca']
             ca4 = request.POST['fourthca']
             exam = request.POST['exam']
             if exam == "":
                 exam = 0
             if ca1 == "":
                 ca1 = 0
             if ca2 == "":
                 ca2 = 0
             if ca3 == "":
                 ca3 = 0
             if ca4 == "":
                 ca4 = 0
             try:
                h = int(exam)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
             try:
                 h1 = int(ca1)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
             try:
                 h2 = int(ca2)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
             try:
                 h3 = int(ca3)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
             try:
                 h4 = int(ca4)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
             if klass1 =='SS 3' and term1 =='Second':
                 h1 = 0
                 h2 = 0
                 h3 = 0
             elif klass1 =='JS 3' and term1 =='Second':
                 h1 = 0
                 h2 = 0
                 h3 = 0
             else:
                 if h > 70 :
                     h = 0
                 if h1 > 10 :
                     h1 = 0
                 if h2 > 10 :
                     h2 = 0
                 if h3 > 10 :
                     h3 = 0
                 if h4 > 10 :
                     h4 = 0
             getdetails.first_ca = h1
             getdetails.second_ca = h2
             getdetails.third_ca = h3
             getdetails.fourth_ca = h4
        #     getdetails.sixth_ca = h3
        #     getdetails.fifth_ca = h1+h2
             getdetails.exam_score = h
             getdetails.save()
             #**********************getting the class average
             getdetails2 = SubjectScore.objects.get(id = vid)
             admno = getdetails2.academic_rec.student.admissionno
             klass = getdetails2.klass
             arm = getdetails2.arm
             subject = getdetails2.subject
             session = getdetails2.session
             term = getdetails2.term
             fullname = getdetails2.academic_rec.student.fullname

             #************TOTTAL STUDENT IN CLASS offering subject************
             totstudent = SubjectScore.objects.filter(session = session,term = term,klass = klass,arm = arm,subject = subject).count()
             #********************term score total****************
             totsubject = SubjectScore.objects.filter(session = session,term = term,klass = klass,arm = arm,subject = subject).aggregate(Sum('end_term_score'))

             varrid = totsubject['end_term_score__sum']
             subavg = varrid/totstudent
             annavg = 0
             if term == 'Third':
                 an = annualaverage(str(admno),str(session),str(arm),str(klass),str(subject))
             SubjectScore.objects.filter(klass = klass,arm = arm,subject = subject,session = session,term = term).update(subject_teacher = uenter.upper(),subject_avg = subavg)
             #***************************getting subject position**************************#
             sp = subjectposition(str(session),str(subject),str(term),str(klass),str(arm))
             #*****************************calculate percentage
             tn = percent(str(session),str(klass),str(arm),str(admno),str(term))
             #***********************getting the class position
             cp = classposition(str(session),str(term),str(klass),str(arm))
             #************getting stream position****************
             cp1 = classposition1(str(session),str(term),str(klass))
             c = klass[0] #if the first alphabet of thee selected class is P FOR PRIMMARY, Y FOR YEAR, B FOR BASIC , N FOR NURSERY C FOR CLASS, L FOR LOWER PRIMARY
             if c.upper() =='P' or c.upper() == 'Y' or c.upper() == 'B' or c.upper() == 'N' or c.upper() == 'C' or c.upper() == 'L':
                 return HttpResponseRedirect('/assessment/primary_assessment/%s/%s/%s/%s/%s/'%(str(session).replace('/','j'),str(klass).replace(' ','k'),str(arm).replace(' ','k'),str(fullname).replace(' ','z'),str(term).replace(' ','0')))
             else:  #for JSS AND SSS
                 #return HttpResponseRedirect('/assessment/enterca/')
                 return HttpResponseRedirect('/assessment/secondary_assessment/%s/%s/%s/%s/%s/'%(str(session).replace('/','j'),str(klass).replace(' ','k'),str(arm).replace(' ','k'),str(subject).replace(' ','z'),str(term).replace(' ','0')))
        else:
            form = caform()
            return render_to_response('assessment/editca.html',{'form':form,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')



def editcas2(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.staffname
        sec = ''
        pry = ''
        for j in appused.objects.all():
            pry = j.primary
            sec = j.secondary
        if sec is True :
            pass
        else:
            return HttpResponseRedirect('/assessment/access-denied/')
        varerr =''
        getdetails = SubjectScore.objects.get(id = vid)
        admno1 = getdetails.academic_rec.student.admissionno
        klass1 = getdetails.klass
        arm1 = getdetails.arm
        subject1 = getdetails.subject
        session1 = getdetails.session
        term1 = getdetails.term

        if request.method == 'POST':
             ca4 = request.POST['fourthca']
             ca5 = request.POST['fifthca']
             ca6 = request.POST['sixthca']
             rep = request.POST['report']

             if ca4 == "":
                 ca4 = 0
             if ca5 == "":
                 ca5 = 0
             if ca6 == "":
                 ca6 = 0



             h4 = int(ca4)
             h5 = int(ca5)
             h6 = int(ca6)

             if klass1 =='SS 3' and term1 =='Second':
                 h1 = 0
                 h2 = 0
             elif klass1 =='JS 3' and term1 =='Second':
                 h1 = 0
                 h2 = 0
             else:

                 if h4 > 20 :
                     h4 = 0
                 if h5 > 20 :
                     h5 = 0
                 if h6 > 60 :
                     h6 = 0

             getdetails.fourth_ca = h4
             getdetails.fifth_ca = h5
             getdetails.sixth_ca = h6
             getdetails.save()

             #**********************getting the classroom average*********************
             getdetails2 = SubjectScore.objects.get(id = vid)
             admno = getdetails2.academic_rec.student.admissionno
             klass = getdetails2.klass
             arm = getdetails2.arm
             grp=getdetails2.subject_group
             subject = getdetails2.subject
             session = getdetails2.session
             term = getdetails2.term
             fullname = getdetails2.academic_rec.student.fullname

             
             #************TOTAL STUDENT IN CLASS offering subject************
             totstudent = SubjectScore.objects.filter(session = session,term = term,klass = klass,arm = arm,subject = subject).count()
             

             #********************term score total****************
             totsubject = SubjectScore.objects.filter(session = session,term = term,klass = klass,arm = arm,subject = subject).aggregate(Sum('end_term_score'))
             varrid = totsubject['end_term_score__sum']
             subavg = varrid/totstudent
             SubjectScore.objects.filter(klass = klass,arm = arm,subject = subject,session = session,term = term).update(subject_teacher = uenter.upper(),subject_avg = subavg)
            
             annavg = 0
             if term == 'Third':
                 an = annualaverage(str(admno),str(session),str(arm),str(klass),str(subject))

            
             
             #***************************getting subject position**************************#
             sp = subjectposition(str(session),str(subject),str(term),str(klass),str(arm))
             

             #*****************************calculate percentage
             # tn = percent(str(session),str(klass),str(arm),str(admno),str(term))
             

             #******************getting mid term classroom average*****************           
             ca=classaverageEnd(klass,session,term,arm)

             sa=studentaverageEnd(admno,term,session,klass,arm)



             #***********************getting the classroom position*******
             cp = classposition(str(session),str(term),str(klass),str(arm))

             
             #************getting class position****************
             cp1 = classposition1(str(session),str(term),str(klass))
             c = klass[0]

             return HttpResponseRedirect('/assessment/secondary_assessment/%s/%s/%s/%s/%s/%s/%s/'%(str(session).replace('/','j'),str(klass).replace(' ','k'),str(arm).replace(' ','k'),str(subject).replace(' ','k'),str(term).replace(' ','0'),str(grp).replace(' ','m'),str(rep).replace(' ','p')))


        else:
            form = caform()
            return render_to_response('assessment/editca.html',{'form':form,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')



def editcas1(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.staffname
        sec = ''
        pry = ''
        for j in appused.objects.all():
            pry = j.primary
            sec = j.secondary
        if sec is True :
            pass
        else:
            return HttpResponseRedirect('/assessment/access-denied/')
        varerr =''
        getdetails = SubjectScore.objects.get(id = vid)
        admno1 = getdetails.academic_rec.student.admissionno
        klass1 = getdetails.klass
        arm1 = getdetails.arm
        subject1 = getdetails.subject
        session1 = getdetails.session
        term1 = getdetails.term

        if request.method == 'POST':
             ca1 = request.POST['firstca']
             ca2 = request.POST['secondca']
             ca3 = request.POST['thirdca']
             rep = request.POST['report']

             if ca1 == "":
                 ca1 = 0
             if ca2 == "":
                 ca2 = 0
             if ca3 == "":
                 ca3 = 0

             h1= ca1
             h2 = int(ca2)
             h3 = int(ca3)
                   

             if klass1 =='SS 3' and term1 =='Second':
                 h1 = 0
                 h2 = 0
             elif klass1 =='JS 3' and term1 =='Second':
                 h1 = 0
                 h2 = 0
             else:
                 if h1 > 10 :
                     h1 = 0
                 if h2 > 10 :
                     h2 = 0
                 if h3> 20 :
                     h3 = 0

             getdetails.first_ca = h1
             getdetails.second_ca = h2
             getdetails.third_ca = h3 
            
             getdetails.save()

             #**********************getting the classroom average*********************
             getdetails2 = SubjectScore.objects.get(id = vid)
             admno = getdetails2.academic_rec.student.admissionno
             klass = getdetails2.klass
             arm = getdetails2.arm
             grp=getdetails2.subject_group
             subject = getdetails2.subject
             session = getdetails2.session
             term = getdetails2.term
             fullname = getdetails2.academic_rec.student.fullname

             
             #************Subject Average************
             totstudent = SubjectScore.objects.filter(session = session,term = term,klass = klass,arm = arm,subject = subject).count()
             totsubject = SubjectScore.objects.filter(session = session,term = term,klass = klass,arm = arm,subject = subject).aggregate(Sum('mid_term_score'))
             varrid = totsubject['mid_term_score__sum']
             subavg = varrid/totstudent
             SubjectScore.objects.filter(klass = klass,arm = arm,subject = subject,session = session,term = term).update(subject_teacher = uenter.upper(),subject_avg = subavg)

             #s**********************Student average*********************
             sa=studentaveragemid(admno,term,session,klass,arm)

          ##*****************classroom average *************************
             ca=classaveragemid(admno,klass,session,term,arm)

             c = klass[0]

             return HttpResponseRedirect('/assessment/secondary_assessment/%s/%s/%s/%s/%s/%s/%s/'%(str(session).replace('/','j'),str(klass).replace(' ','k'),str(arm).replace(' ','k'),str(subject).replace(' ','k'),str(term).replace(' ','0'),str(grp).replace(' ','m'),str(rep).replace(' ','p')))


        else:
            form = caform()
            return render_to_response('assessment/editca.html',{'form':form,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')









def editcapry(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.staffname
        sec = ''
        pry = ''
        for j in appused.objects.all():
            pry = j.primary
            sec = j.secondary
        if pry is True :
            pass
        else:
            return HttpResponseRedirect('/assessment/access-denied/')
        varerr =''
        getdetails = SubjectScore.objects.get(id = vid)
        admno1 = getdetails.academic_rec.student.admissionno
        klass1 = getdetails.klass
        arm1 = getdetails.arm
        subject1 = getdetails.subject
        session1 = getdetails.session
        term1 = getdetails.term
        if request.method == 'POST':
             ca1 = request.POST['firstca']
             ca2 = request.POST['secondca']
             ca3 = request.POST['thirdca']
             exam = request.POST['exam']
             if exam == "":
                 exam = 0
             if ca1 == "":
                 ca1 = 0
             if ca2 == "":
                 ca2 = 0
             if ca3 == "":
                 ca3 = 0
             try:
                h = int(exam)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
             try:
                 h1 = int(ca1)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
             try:
                 h2 = int(ca2)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
             try:
                 h3 = int(ca3)
             except :
                 return HttpRsponseRedirect('/assessment/enterca/')
             if klass1 =='SS 3' and term1 =='Second':
                 h1 = 0
                 h2 = 0
                 h3 = 0
             elif klass1 =='JS 3' and term1 =='Second':
                 h1 = 0
                 h2 = 0
                 h3 = 0
             else:
                 if h > 70 :
                     h = 0
                 if h1 > 10 :
                     h1 = 0
                 if h2 > 10 :
                     h2 = 0
                 if h3 > 10 :
                     h3 = 0
             getdetails.first_ca = h1
             getdetails.second_ca = h2
             getdetails.third_ca = h3
             getdetails.sixth_ca = h3
             getdetails.fifth_ca = h1+h2
             getdetails.exam_score = h
             getdetails.save()
             #**********************getting the class average
             getdetails2 = SubjectScore.objects.get(id = vid)
             admno = getdetails2.academic_rec.student.admissionno
             klass = getdetails2.klass
             arm = getdetails2.arm
             subject = getdetails2.subject
             session = getdetails2.session
             term = getdetails2.term
             fullname = getdetails2.academic_rec.student.fullname
             #************TOTTAL STUDENT IN CLASS offering subject************
             totstudent = SubjectScore.objects.filter(session = session,term = term,klass = klass,arm = arm,subject = subject).count()
             #********************term score total****************
             totsubject = SubjectScore.objects.filter(session = session,term = term,klass = klass,arm = arm,subject = subject).aggregate(Sum('end_term_score'))
             varrid = totsubject['end_term_score__sum']
             subavg = varrid/totstudent
             annavg = 0
             if term == 'Third':
                 an = annualaverage(str(admno),str(session),str(arm),str(klass),str(subject))
             SubjectScore.objects.filter(klass = klass,arm = arm,subject = subject,session = session,term = term).update(subject_teacher = uenter.upper(),subject_avg = subavg)
             #***************************getting subject position**************************#
             sp = subjectposition(str(session),str(subject),str(term),str(klass),str(arm))
             #*****************************calculate percentage
             tn = percent(str(session),str(klass),str(arm),str(admno),str(term))
             #***********************getting the class position
             cp = classposition(str(session),str(term),str(klass),str(arm))
             #************getting stream position****************
             cp1 = classposition1(str(session),str(term),str(klass))
             c = klass[0] #if the first alphabet of thee selected class is P FOR PRIMMARY, Y FOR YEAR, B FOR BASIC , N FOR NURSERY C FOR CLASS, L FOR LOWER PRIMARY
             if c.upper() =='P' or c.upper() == 'Y' or c.upper() == 'B' or c.upper() == 'N' or c.upper() == 'C' or c.upper() == 'L':
                 return HttpResponseRedirect('/assessment/primary_assessment/%s/%s/%s/%s/%s/'%(str(session).replace('/','j'),str(klass).replace(' ','k'),str(arm).replace(' ','k'),str(fullname).replace(' ','z'),str(term).replace(' ','0')))
             else:  #for JSS AND SSS
                 #return HttpResponseRedirect('/assessment/enterca/')
                 return HttpResponseRedirect('/assessment/secondary_assessment/%s/%s/%s/%s/%s/'%(str(session).replace('/','j'),str(klass).replace(' ','k'),str(arm).replace(' ','k'),str(subject).replace(' ','z'),str(term).replace(' ','0')))
        else:
            form = caform()
            return render_to_response('assessment/editca.html',{'form':form,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')


"""
def editca(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.staffname
        sec = ''
        pry = ''
        for j in appused.objects.all():
            pry = j.primary
            sec = j.secondary
        #if pry is True :
        #    pass
        #else:
        #    return HttpResponseRedirect('/assessment/access-denied/')
        varerr =''
        getdetails = SubjectScore.objects.get(id = vid)
        if request.method == 'POST':
             ca1 = request.POST['firstca']
             ca2 = request.POST['secondca']
             ca3 = request.POST['thirdca']
             exam = request.POST['exam']
             if exam == "":
                 exam = 0
             if ca1 == "":
                 ca1 = 0
             if ca2 == "":
                 ca2 = 0
             if ca3 == "":
                 ca3 = 0
             try:
                h = float(exam)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
             try:
                 h1 = float(ca1)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
             try:
                 h2 = float(ca2)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
             try:
                 h3 = float(ca3)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
             if h > 70 :
                 h = 70
             if h1 > 10 :
                 h1 = 10
             if h2 > 10 :
                 h2 = 10
             if h3 > 10 :
                 h3 = 10
             getdetails.first_ca = str(h1)
             getdetails.second_ca = str(h2)
             getdetails.third_ca = str(h3)
             getdetails.exam_score = str(h)
             getdetails.fifth_ca = str(h2)+str(h1)
             getdetails.save()
             #**********************getting the class average
             getdetails2 = SubjectScore.objects.get(id = vid)
             admno = getdetails2.academic_rec.student.admissionno
             klass = getdetails2.klass
             arm = getdetails2.arm
             subject = getdetails2.subject
             session = getdetails2.session
             term = getdetails2.term
             fullname = getdetails2.academic_rec.student.fullname
             totstudent = SubjectScore.objects.filter(klass = klass,arm = arm,subject = subject,session = session,term = term).count()
             totsubject = SubjectScore.objects.filter(klass = klass,arm = arm,subject = subject,session = session,term = term).aggregate(Sum('end_term_score'))
             varrid = totsubject['end_term_score__sum']
             subavg = varrid/totstudent
             annavg = 0
             ns1 = str(subject).replace(' ','z')
             ns = str(ns1).replace('$','q')
             if term == 'Third':
                 an = annualaverage(str(admno),str(session),str(arm),str(klass),str(subject))
                 #print 'Annual Average :',an
             SubjectScore.objects.filter(klass = klass,arm = arm,subject = subject,session = session,term = term).update(subject_teacher = uenter.upper(),subject_avg = subavg)

             #*************************************************************************getting subject position
             sp = subjectposition(str(session),str(subject),str(term),str(klass),str(arm))
             #*****************************calculate percentage
             tn = percent(str(session),str(klass),str(arm),str(admno),str(term))
             #***********************getting the class position
             cp = classposition(str(session),str(term),str(klass),str(arm))
             c = klass[0]
             if c.upper() =='P' or c.upper() == 'Y' or c.upper() == 'B' or c.upper() == 'N' or c.upper() == 'C' or c.upper() == 'L':
                #here i redirect to primary page
                 #return primary_url(str(session),str(klass),str(arm),str(fullname),str(term))
                 fname1 = str(fullname).replace(' ','z')
                 fname2 = fname1.replace('-','i')
                 fname  = fname2.replace("'",'u')
                 return HttpResponseRedirect('/assessment/primary_assessment/%s/%s/%s/%s/%s/'%(str(session).replace('/','j'),str(klass).replace(' ','k'),str(arm).replace(' ','k'),fname,str(term).replace(' ','0')))
             else:
                 #return HttpResponseRedirect('/assessment/enterca/')
                 return HttpResponseRedirect('/assessment/secondary_assessment/%s/%s/%s/%s/%s/'%(str(session).replace('/','j'),str(klass).replace(' ','k'),str(arm).replace(' ','k'),ns,str(term).replace(' ','0')))
        else:
            form = caform()
            return render_to_response('assessment/editca.html',{'form':form,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')
"""

def getsubjectscore(request):
        if  "userid" in request.session:
            if request.is_ajax():
                if request.method == 'POST':
                    varuser = request.session['userid']
                    varerr =""
                    post = request.POST.copy()
                    acccode = post['userid']
                    getdetails = SubjectScore.objects.get(id = acccode)
                    return render_to_response('assessment/editca.html',{'getdetails':getdetails})
                else:
                    gdata = ""
                    return render_to_response('index.html',{'gdata':gdata})
            else:

                gdata = ""
                return render_to_response('getlg.htm',{'gdata':gdata})
        else:
            return HttpResponseRedirect('/login/')

def getsubjectscore1(request):
        if  "userid" in request.session:
            if request.is_ajax():
                if request.method == 'POST':
                    varuser = request.session['userid']
                    varerr =""
                    post = request.POST.copy()
                    acccode = post['userid']
                    vid,acccode= acccode.split(':')
                    getdetails = SubjectScore.objects.get(id = vid)

                    if acccode=='End term':
                        return render_to_response('assessment/editca2.html',{'getdetails':getdetails,'ak':acccode})
                    elif acccode=='Mid term':
                        return render_to_response('assessment/editca1.html',{'getdetails':getdetails,'ak':acccode})
                else:
                    gdata = ""
                    return render_to_response('index.html',{'gdata':gdata})
            else:

                gdata = ""
                return render_to_response('getlg.htm',{'gdata':gdata})
        else:
            return HttpResponseRedirect('/login/')


def getsubjectscore2(request):
        if  "userid" in request.session:
            if request.is_ajax():
                if request.method == 'POST':
                    varuser = request.session['userid']
                    varerr =""
                    post = request.POST.copy()
                    acccode = post['userid']

                    # svid,reporttype= acccode.split(':')
                    getdetails = SubjectScore.objects.get(id = acccode)
                    return render_to_response('assessment/editca1.html',{'getdetails':getdetails,'ak':acccode})
                else:
                    gdata = ""
                    return render_to_response('index.html',{'gdata':gdata})
            else:

                gdata = ""
                return render_to_response('getlg.htm',{'gdata':gdata})
        else:
            return HttpResponseRedirect('/login/')
                                    
def getsubjectscorep(request):
        if  "userid" in request.session:
            if request.is_ajax():
                if request.method == 'POST':
                    varuser = request.session['userid']
                    varerr =""
                    post = request.POST.copy()
                    acccode = post['userid']
                    getdetails = SubjectScore.objects.get(id = acccode)
                    return render_to_response('assessment/editcap.html',{'getdetails':getdetails})
                else:
                    gdata = ""
                    return render_to_response('index.html',{'gdata':gdata})
            else:

                gdata = ""
                return render_to_response('getlg.htm',{'gdata':gdata})
        else:
            return HttpResponseRedirect('/login/')


def affectivedomain(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        if ClassTeacher.objects.filter(teachername = varuser).count() == 0 :
            return HttpResponseRedirect('/assessment/access-denied/')
        varerr =''
        getdetails =''
        form = caform()
        return render_to_response('assessment/affective.html',{'varuser':varuser,'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')

def getcomm(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        if ClassTeacher.objects.filter(teachername = varuser).count() == 0 :
            return HttpResponseRedirect('/assessment/access-denied/')
        user = userprofile.objects.get(username = varuser)
        varerr =''
        getdetails =''
        form = caform()
        return render_to_response('assessment/comm.html',{'varuser':varuser,'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')

def getclassaff(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state = acccode
                kk = []
                sdic = {}
                data = ClassTeacher.objects.filter(teachername = varuser,session = state).order_by('klass')
                for j in data:
                    j = j.klass
                    s = {j:j}
                    sdic.update(s)
                klist = sdic.values()
                for p in klist:
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

def getarmaff(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state = acccode
                kk = []
                sdic = {}
                data = ClassTeacher.objects.filter(teachername = varuser,session = state).order_by('arm')
                for j in data:
                    j = j.arm
                    s = {j:j}
                    sdic.update(s)
                klist = sdic.values()
                for p in klist:
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

def getstudentaff(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                session,klass,arm,term = acccode.split(':')
                #print klass
                data = []
                getstu = Student.objects.filter(admitted_class = klass,admitted_arm=arm,admitted_session = session,gone = False).order_by('-sex','fullname')
                for p in getstu:
                    if StudentAcademicRecord.objects.filter(student = p,term = term):
                        comm = StudentAcademicRecord.objects.get(student = p,term = term)
                        affec = AffectiveSkill.objects.get(academic_rec = comm)
                        psyco = PsychomotorSkill.objects.get(academic_rec = comm)
                        stdic = {'studentinfo':p,'comment':comm,'affective':affec,'psyco':psyco}
                        data.append(stdic)
                return render_to_response('assessment/affec.html',{'klass':klass,
                    'data':data,'session':session,'term':term,'arm':arm})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def comment(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                session,klass,arm,term = acccode.split(':')
                #print klass
                data = []
                getstu = Student.objects.filter(admitted_class = klass,admitted_arm=arm,admitted_session = session,gone = False).order_by('-sex','fullname')
                for p in getstu:
                    if StudentAcademicRecord.objects.filter(student = p,term = term):
                        comm = StudentAcademicRecord.objects.get(student = p,term = term)
                        affec = AffectiveSkill.objects.get(academic_rec = comm)
                        psyco = PsychomotorSkill.objects.get(academic_rec = comm)
                        stdic = {'studentinfo':p,'comment':comm,'affective':affec,'psyco':psyco}
                        data.append(stdic)
                return render_to_response('assessment/comment.html',{'data':data})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getaffective(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = AffectiveSkill.objects.get(id = acccode)
                return render_to_response('assessment/editaff.html',{'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getaffective2(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.expensedecription
        varerr =''
        getdetails = SubjectScore.objects.get(id = vid)
        if request.method == 'POST':
            ca1 = request.POST['firstca']
            ca2 = request.POST['secondca']
            exam = request.POST['exam']
            if exam == "":
                exam = 0
            if ca1 == "":
                ca1 = 0
            if ca2 == "":
                ca2 = 0
            try:
                h = int(exam)
            except :
                return HttpResponseRedirect('/assessment/enterca/')
            try:
                h1 = int(ca1)
            except :
                return HttpResponseRedirect('/assessment/enterca/')
            try:
                h2 = int(ca2)
            except :
                return HttpResponseRedirect('/assessment/enterca/')
            if h > 60 :
                h = 60
            if h1 > 20 :
                h1 = 20
            if h2 > 20 :
                h2 = 20
            getdetails.first_ca = h1
            getdetails.second_ca = h2
            getdetails.exam_score = h
            getdetails.save()
            return HttpResponseRedirect('/assessment/enterca/')
        else:
            form = caform()

        return render_to_response('assessment/editca.html',{'form':form,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')


def getpsyco(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = PsychomotorSkill.objects.get(id = acccode)
                return render_to_response('assessment/editpsyco.html',{'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getcomment(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = StudentAcademicRecord.objects.get(id = acccode)
               # print getdetails
                return render_to_response('assessment/editcomment.html',{'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getcommentca(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                vid,ca =acccode.split(':')
                getdetails = StudentAcademicRecord.objects.get(id = vid)
                dit=getdetails.stu_ave1 * 5
                if ca == 'Mid term':
                    return render_to_response('assessment/edicacom.html',{'ca':ca,'getdetails':getdetails,'dit':dit})
                elif ca=='End term':
                    return render_to_response('assessment/editcacom.html',{'ca':ca,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def editcomment(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =''
        getdetails = ''
        if request.method == 'POST':
            comments = request.POST['class_teacher_comment']
            absent = request.POST['noabsent']
            if comments == "" or absent == "":
                return HttpResponseRedirect('/assessment/ca_comments/')

            getdetails = StudentAcademicRecord.objects.get(id = vid)
            session = getdetails.session
            term = getdetails.term
                        
            getdetails.days_present = int(getdetails.days_open) - int(absent)
            getdetails.class_teacher_comment = comments 
            getdetails.days_absent = absent      
            getdetails.save()
            # StudentAcademicRecord.objects.filter(session = session,term = term).update(next_term_start = tday)

            return HttpResponseRedirect('/assessment/ca_comments/')
        else:
            form = caform()
        return render_to_response('assessment/editca.html',{'form':form,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')

def editcommentca1(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =''
        getdetails = ''
        if request.method == 'POST':
            comments = request.POST['comment']
            getdetails = StudentAcademicRecord.objects.filter(id = vid).update(com1=comments)
            return HttpResponseRedirect('/assessment/ca_comments/')
    else:
        return HttpResponseRedirect('/login/')

def editcommentca2(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =''
        getdetails = ''
        if request.method == 'POST':
            comments = request.POST['comment']
            getdetails = StudentAcademicRecord.objects.filter(id = vid).update(com2=comments)
            return HttpResponseRedirect('/assessment/ca_comments/')
    else:
        return HttpResponseRedirect('/login/')


def editpsyco(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =''
        getdetails = ''
        if request.method == 'POST':
            attendance = request.POST['attendance']
            motivation = request.POST['motivation']
            contribution = request.POST['contribution']
            social_behaviour = request.POST['social_behaviour']
            if contribution == "" or motivation == "" or attendance == "" or social_behaviour == "" :
                return HttpResponseRedirect('/assessment/affective/')
            getdetails = PsychomotorSkill.objects.get(id = vid)
            getdetails.attendance = attendance.upper()
            getdetails.motivation = motivation.upper()
            getdetails.contribution = contribution.upper()
            getdetails.social_behaviour = social_behaviour.upper()
            getdetails.save()
            return HttpResponseRedirect('/assessment/affective/')
        else:
            form = caform()

        return render_to_response('assessment/editca.html',{'form':form,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')

def editaffective(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =''
        getdetails = ''
        if request.method == 'POST':
            punctuality = request.POST['punctuality']
            neatness = request.POST['neatness']
            honesty = request.POST['honesty']
            initiative = request.POST['initiative']
            self_control = request.POST['self_control']
            reliability = request.POST['reliability']
            perseverance = request.POST['perseverance']
            politeness = request.POST['politeness']
            attentiveness = request.POST['attentiveness']
            rel_with_people = request.POST['rel_with_people']
            cooperation = request.POST['cooperation']
            organizational_ability = request.POST['organizational_ability']
            if punctuality == "" or self_control == "" or initiative == "" or honesty == "" or neatness == "" or reliability == "" or perseverance == "" or politeness == "" or attentiveness == "" or rel_with_people == ""  or cooperation =="" or organizational_ability =="":
                return HttpResponseRedirect('/assessment/affective/')
            getdetails = AffectiveSkill.objects.get(id = vid)
            getdetails.punctuality = punctuality.upper()
            getdetails.neatness = neatness.upper()
            getdetails.honesty = honesty.upper()
            getdetails.initiative = initiative.upper()
            getdetails.self_control = self_control.upper()
            getdetails.reliability = reliability.upper()
            getdetails.perseverance = perseverance.upper()
            getdetails.politeness = politeness.upper()
            getdetails.attentiveness = attentiveness.upper()
            getdetails.rel_with_people = rel_with_people.upper()
            getdetails.cooperation = cooperation.upper()
            getdetails.organizational_ability = organizational_ability.upper()
            getdetails.save()
            return HttpResponseRedirect('/assessment/affective/')
        else:
            form = caform()
        return render_to_response('assessment/editca.html',{'form':form,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')

def addsubject(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        try:
            if Student.objects.get(fullname=varuser,admitted_session=currse,gone=False):
                return HttpResponseRedirect('/assessment/student/my_subjects/')
        except:
            if ClassTeacher.objects.filter(teachername = varuser).count() == 0 :
                return HttpResponseRedirect('/assessment/access-denied/')
        varerr =''
        getdetails =''
        form = addsubjectform()
        return render_to_response('assessment/addsubject.html',{'varuser':varuser,'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')

def addstudentsubject(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        
        user = userprofile.objects.get(username = varuser)
        uenter = user.expensedecription


        if ClassTeacher.objects.filter(teachername = varuser).count() == 0 :
            return HttpResponseRedirect('/assessment/access-denied/')

        varerr =''
        getdetails =''
        if request.method == 'POST':
            form = addsubjectform(request.POST) # A form bound to the POST data
            if form.is_valid():
                expenses = form.cleaned_data['expenses']
                return HttpResponseRedirect('/bill/expensesname/')
        else:
            form = addsubjectform()
        return render_to_response('assessment/addsubject.html',{'varuser':varuser,'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')

def getstudentsubject(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                post = request.POST.copy()
                acccode = post['userid']
                session,klass,arm,term = acccode.split(':')
                kk = []

                if term =='First':
                    data = Student.objects.filter(admitted_session = session,admitted_class = klass,first_term=True,admitted_arm = arm,gone = False).order_by('fullname')
                elif term == 'Second':
                    data = Student.objects.filter(admitted_session = session,admitted_class = klass,second_term=True,admitted_arm = arm,gone = False).order_by('fullname')

                elif term=='Third':
                    data = Student.objects.filter(admitted_session = session,admitted_class = klass,third_term=True,admitted_arm = arm,gone = False).order_by('fullname')

                for p in data:
                    kk.append(p.fullname)
                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def getsubject4student(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                getdetails = ''
                post = request.POST.copy()
                acccode = post['userid']
                session,klass,arm,term,student = acccode.split(':')
                getstu = Student.objects.get(admitted_class = klass,admitted_arm=arm,admitted_session = session,fullname = student,gone = False)
                if StudentAcademicRecord.objects.filter(student = getstu,term = term):
                   comm = StudentAcademicRecord.objects.get(student = getstu,term = term)
                   getdetails = SubjectScore.objects.filter(session = session,klass = klass, arm = arm,term = term,academic_rec = comm).order_by('num')
                return render_to_response('assessment/subject.html',{'varuser':varuser,'getdetails':getdetails,'stuid':getstu.id,'fullname':getstu.fullname,'session':session,'term':term})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

# def addmoresubject(request):
#     if  "userid" in request.session:
#         varuser = request.session['userid']
#         user = userprofile.objects.get(username = varuser)
#         uenter = user.expensedecription
#         varerr =''
#         getdetails =''
#         term_l = ['First','Second','Third']
#         if request.method == 'POST':
#             admno = request.POST['admno']
#             session = request.POST['session']
#             term1 = request.POST['term']
#             subclass = request.POST['subclass']
#             subjectlist = request.POST['subjectlist']
#             stuacarec = Student.objects.get(admissionno = admno,admitted_session = session)
#             for term in term_l:
#                 if StudentAcademicRecord.objects.filter(student = stuacarec,term = term):
#                     pass
#                 else:
#                     academic_record = StudentAcademicRecord(student=stuacarec, klass=stuacarec.admitted_class,arm=stuacarec.admitted_arm, term=term, session=stuacarec.admitted_session)
#                     academic_record.save()
#                     aff =  AffectiveSkill(academic_rec=academic_record)
#                     aff.save()
#                     psyco = PsychomotorSkill(academic_rec=academic_record)
#                     psyco.save()

#             gets = Subject.objects.filter(subject = subjectlist)
#             num = 1
#             for p in gets:
#                num = p.num
#             if term1 == 'First':
#                 for term in term_l:
#                     stuac = StudentAcademicRecord.objects.get(student = stuacarec,term = term)
#                     if SubjectScore.objects.filter(academic_rec = stuac,term = term,subject = subjectlist).count() == 0:
#                        SubjectScore(academic_rec = stuac,term = term,subject = subjectlist,num = num,session = session,klass = stuacarec.admitted_class,arm = stuacarec.admitted_arm).save()
#                 return HttpResponseRedirect('/assessment/addsubject/')
#             else:
#                 stuac = StudentAcademicRecord.objects.get(student = stuacarec,term = term1)
#                 if SubjectScore.objects.filter(academic_rec = stuac,term = term1,subject = subjectlist).count() == 0:
#                     SubjectScore(academic_rec = stuac,term = term1,subject = subjectlist,num = num,session = session,klass = stuacarec.admitted_class,arm = stuacarec.admitted_arm).save()
#                     return HttpResponseRedirect('/assessment/addsubject/')
#                 else:
#                    return HttpResponseRedirect('/assessment/addsubject/')
#         else:
#             form = addsubjectform()
#         return render_to_response('assessment/addsubject.html',{'form':form,'varerr':varerr})
#     else:
#         return HttpResponseRedirect('/login/')


def editsubgrp(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        if request.method == 'POST':
            cate = request.POST['subjectlist']
            getdetails = SubjectScore.objects.get(id = invid)
            getdetails.subject_group=cate
            getdetails.save()
            return HttpResponseRedirect('/assessment/class_list/')
        else:
            return HttpResponseRedirect('/setup/subject/')
    else:
        return HttpResponseRedirect('/login/')


def changesubgrp(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails =  SubjectScore.objects.get(id = acccode)
                subjectlist = Subject_group.objects.all().order_by('id')
                fs = {}
                for k in subjectlist:
                    l = {k.subject_group:k.subject_group}
                    fs.update(l)
                nlist = fs.keys()
                return render_to_response('assessment/changegrp.html',{'varuser':varuser,'subjectlist':nlist,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def getmorestudentsubject(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                code = post['userid']
                acccode,ter = str(code).split(':')
                getstu = Student.objects.get(id = acccode)
                session = getstu.admitted_session
                admno = getstu.admissionno
                klass = getstu.admitted_class
                subclass = getstu.subclass
                arm = getstu.admitted_arm
                term = ter
                fullname = getstu.fullname
                subjectlist = Subject.objects.filter(category = subclass, category2 = 'Optional').order_by('num')
                fs = {}
                for k in subjectlist:
                    l = {k.subject:k.subject}
                    fs.update(l)
                nlist = fs.keys()
                chk=tblcf.objects.get(session=session,term=term)
                chkdate = chk.deadline
                if chkdate < date:
                    return render_to_response('assessment/checkbackcf.html',{'ckk':chkdate})

                return render_to_response('assessment/moresubject.html',{'session':session,
                    'fullname':fullname,
                    'admno':admno,
                    'subjectlist':nlist,
                    'klass':klass,
                    'subclass':subclass,
                    'arm':arm,
                    'term':ter})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')




def getmoresubject(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                code = post['userid']
                acccode,ter = str(code).split(':')
                getstu = Student.objects.get(id = acccode)
                session = getstu.admitted_session
                admno = getstu.admissionno
                klass = getstu.admitted_class
                subclass = getstu.subclass
                arm = getstu.admitted_arm
                term = ter
                fullname = getstu.fullname
                subjectlist = Subject.objects.filter(category = subclass, category2 = 'Optional').order_by('num')
                fs = {}
                for k in subjectlist:
                    l = {k.subject:k.subject}
                    fs.update(l)
                nlist = fs.keys()
                return render_to_response('assessment/moresubject.html',{'session':session,'fullname':fullname,'admno':admno,'subjectlist':nlist,'klass':klass,'subclass':subclass,'arm':arm,'term':term})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def addmoresubject(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        # user = userprofile.objects.get(username = varuser)
        # uenter = user.expensedecription
        varerr =''
        getdetails =''
        term_l = ['First','Second','Third']
        if request.method == 'POST':
            admno = request.POST['admno']
            session = request.POST['session']
            term1 = request.POST['term']
            subclass = request.POST['subclass']
            subjectlist = request.POST['subjectlist']
            stuacarec = Student.objects.get(admissionno = admno,admitted_session = session,gone=False)
            for term in term_l:
                if StudentAcademicRecord.objects.filter(student = stuacarec,term = term):
                    pass
                else:
                    academic_record = StudentAcademicRecord(student=stuacarec, klass=stuacarec.admitted_class,arm=stuacarec.admitted_arm, term=term, session=stuacarec.admitted_session)
                    academic_record.save()
                    aff =  AffectiveSkill(academic_rec=academic_record)
                    aff.save()
                    psyco = PsychomotorSkill(academic_rec=academic_record)
                    psyco.save()

            gets = Subject.objects.filter(subject = subjectlist)
            num = 1
            for p in gets:
               num = p.num
            if term1 == 'First':
                for term in term_l:
                    stuac = StudentAcademicRecord.objects.get(student = stuacarec,term = term)
                    if SubjectScore.objects.filter(academic_rec = stuac,term = term,subject = subjectlist).count() == 0:
                       SubjectScore(academic_rec = stuac,term = term,subject = subjectlist,num = num,session = session,klass = stuacarec.admitted_class,arm = stuacarec.admitted_arm).save()               
            else:
                stuac = StudentAcademicRecord.objects.get(student = stuacarec,term = term1)
                if SubjectScore.objects.filter(academic_rec = stuac,term = term1,subject = subjectlist).count() == 0:
                    SubjectScore(academic_rec = stuac,term = term1,subject = subjectlist,num = num,session = session,klass = stuacarec.admitted_class,arm = stuacarec.admitted_arm).save()                   
            return HttpResponseRedirect('/assessment/secondary_cf/%s/%s/%s/'%(str(session).replace('/','j'),str(admno).replace('/','k'),str(term1).replace(' ','m')))
        else:
            form = addsubjectform()
        return render_to_response('assessment/addsubject.html',{'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')

def secondary_cf(request,session,admn,term):
    varuser = request.session['userid']
    sec = ''
    for j in appused.objects.all():
        sec = j.secondary
    if sec is True :
        pass
    else:
        return HttpResponseRedirect('/assessment/access-denied/')
    session = str(session).replace('j','/')
    admno = str(admn).replace('k','/')
    term = str(term).replace('m',' ')
    stud = Student.objects.get(admissionno=admno,admitted_session=session,gone=False)
    acadec = StudentAcademicRecord.objects.get(student=stud,term=term)
    cf = SubjectScore.objects.filter(academic_rec=acadec,term =term)
    return render_to_response('assessment/stu_sub.html',{'getdetails':cf,'stuid':stud.id,'session':stud.admitted_session,'arm':stud.admitted_arm, 'varuser':varuser,'admno':admno,'term':term,'name':stud.fullname,'klass':stud.admitted_class})




def deletemoresubject(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getstu = SubjectScore.objects.get(id = acccode)
                session = getstu.academic_rec.student.admitted_session
                admno = getstu.academic_rec.student.admissionno
                klass = getstu.academic_rec.student.admitted_class
                subject = getstu.subject
                arm = getstu.academic_rec.student.admitted_arm
                term = getstu.term
                fullname = getstu.academic_rec.student.fullname
                return render_to_response('assessment/deletemoresubject.html',{'session':session,'fullname':fullname,'admno':admno,'klass':klass,'arm':arm,'term':term,'subject':subject,'id':acccode})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def confirmdeletemoresubject(request,pid):
    if  "userid" in request.session:
        getstu = SubjectScore.objects.get(id = pid)
        session = getstu.academic_rec.student.admitted_session
        admno = getstu.academic_rec.student.admissionno
        term1=getstu.term
        getstu.delete()
        return HttpResponseRedirect('/assessment/secondary_cf/%s/%s/%s/'%(str(session).replace('/','j'),str(admno).replace('/','k'),str(term1).replace(' ','m')))
    else:
        return HttpResponseRedirect('/login/')

def principalcomment(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.expensedecription
        if Principal.objects.filter(teachername = varuser).count() == 0:
            return HttpResponseRedirect('/assessment/access-denied/')
        varerr =''
        getdetails =''
        if request.method == 'POST':
            form = caform(request.POST) # A form bound to the POST data
            if form.is_valid():
                expenses = form.cleaned_data['expenses']
                return HttpResponseRedirect('/bill/expensesname/')
        else:
            form = caform()
        return render_to_response('assessment/principalcomment.html',{'varuser':varuser,'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')

def getstudentprincipalcomment(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                session,klass,arm,term = acccode.split(':')
                #print klass
                data = []
                getstu = Student.objects.filter(admitted_class = klass,admitted_arm=arm,admitted_session = session,gone = False).order_by('-sex','fullname')
                for p in getstu:
                    if StudentAcademicRecord.objects.filter(student = p,term = term):
                        comm = StudentAcademicRecord.objects.get(student = p,term = term)
                        stdic = {'studentinfo':p,'comment':comm}
                        data.append(stdic)
                return render_to_response('assessment/princomment.html',{'data':data})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getprincipalcomment(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = StudentAcademicRecord.objects.get(id = acccode)
                # print getdetails
                return render_to_response('assessment/editprincipalcomment.html',{'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def editcommentprin(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =''
        getdetails = ''
        if request.method == 'POST':
            comments = request.POST['class_teacher_comment']
            if comments == "":
                return HttpResponseRedirect('/assessment/affective/')
            getdetails = StudentAcademicRecord.objects.get(id = vid)
            getdetails.principal_comment = comments
            getdetails.save()
            return HttpResponseRedirect('/assessment/principalcomment/')
        else:
            form = caform()

        return render_to_response('assessment/editca.html',{'form':form,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')

def getstudentacademic(request):#*******************now
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = StudentAcademicRecord.objects.get(id = acccode)
                academic = SubjectScore.objects.filter(academic_rec = getdetails).order_by('num')
                return render_to_response('assessment/academicrecord.html',{'getdetails':getdetails,'academic':academic})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def addsubject4pry(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.expensedecription
        if ClassTeacher.objects.filter(teachername = varuser).count() == 0 :
            return HttpResponseRedirect('/assessment/access-denied/')
        sec = ''
        pry = ''
        for j in appused.objects.all():
            pry = j.primary
            sec = j.secondary
        if pry is True :
            pass
        else:
            return HttpResponseRedirect('/assessment/access-denied/')
        varerr =''
        getdetails =''
        if request.method == 'POST':
            form = addsubjectform(request.POST) # A form bound to the POST data
            if form.is_valid():
                expenses = form.cleaned_data['expenses']
                return HttpResponseRedirect('/bill/expensesname/')
        else:
            form = addsubjectform()
        return render_to_response('assessment/capry.html',{'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')

def getsubject4studentpry(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                getdetails = ''
                post = request.POST.copy()
                acccode = post['userid']
                session,klass,arm,term,student = acccode.split(':')
                getstu = Student.objects.get(admitted_class = klass,admitted_arm=arm,admitted_session = session,fullname = student)
                if StudentAcademicRecord.objects.filter(student = getstu,term = term):
                    comm = StudentAcademicRecord.objects.get(student = getstu,term = term)
                    getdetails = SubjectScore.objects.filter(session = session,klass = klass, arm = arm,term = term,academic_rec = comm).order_by('num')
                return render_to_response('assessment/subjectpry.html',{'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getclassaffpry(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state = acccode
                kk = []
                sdic = {}
                data = ClassTeacher.objects.filter(teachername = varuser,session = state).exclude(klass__startswith ='J').exclude(klass__startswith ='S').order_by('klass')
                for j in data:
                    j = j.klass

                    s = {j:j}
                    sdic.update(s)
                klist = sdic.values()
                for p in klist:
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


def indreport(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user= userprofile.objects.get(username=varuser)
        uenter = user.reportsheet
        if uenter is False:
            return HttpResponseRedirect('/assessment/access-denied/')
        varerr = ''
        getdetails= ''
        bal = 250
        
        school = get_object_or_404(School,pk=1)
        if request.method == 'POST':
            form = indreportform(request.POST)
            if form.is_valid():
                session = form.cleaned_data['session']
                term = form.cleaned_data['term']
                admno = form.cleaned_data['admno']
                Pin = form.cleaned_data['Pin']
                replist = [] 
                varclas=[]               
                varused= 0
                varurem = 0
                if Student.objects.filter(admissionno=admno,admitted_session=session).count()==0:
                    varerr= 'ADMISSION NUMBER NOT FOUND'
                    form = indreportform()
                    return render_to_response ('assessment/indreport.html',{'form':form, 'varerr':varerr})


                if tblrpin.objects.filter(rpin=Pin).count()== 0:                    
                    varerr= 'PLEASE CHECK THE PIN AND TRY AGAIN'
                    return render_to_response('assessment/indreport.html',{'varerr':varerr,'form':form})

                
                if tblexpress.objects.filter(pin = Pin):
                    usd = tblexpress.objects.get(pin=Pin)
                    usdpin = usd.pin
                    usdterm = usd.term
                    usdsession = usd.session
                    usdadmno = usd.admno
                    if usdadmno == admno and usdterm==term and usdsession==session and usdpin==Pin:
                        varu = count( Pin) 
                        if varu >='5':
                           varerr= 'PIN ALREADY USED '+ varu + ' TIMES'
                           return render_to_response('assessment/indreport.html',{'varerr':varerr,'form':form})
                        else:
                            varused= int(varu) +1
                            tblexpress.objects.filter(pin=  Pin).update(count= varused)
                            varurem =5 - varused
                    else:
                       varerr= 'THIS PIN HAS BEEN USED'
                       return render_to_response('assessment/indreport.html',{'varerr':varerr,'form':form})     
                else:
                    totbil = printbill (admno,session,term)
                    allowable_debt = 0.15 * int(totbil)
                    allowable_debt = locale.format('%.0f',allowable_debt)
                    allowable_debt= int(allowable_debt) # what i can owe

                    acc=tblaccount.objects.get(acccode = admno)
                    actual_debt = acc.accbal
                    actual_debt = int(actual_debt) # what i'm actually owing
                    bal = actual_debt            
                    if allowable_debt <= actual_debt:                  
                        varerr = "KINDLY UPDATE YOUR WARD'S ACCOUNT " #+totbil+ '  ' +str(actual_debt)
                        return render_to_response('assessment/indreport.html',{'varerr':varerr,'form':form})
                    else:
                        st = Student.objects.get(admissionno=admno, admitted_session=session)
                        tblexpress(count=1,session=session, admno=admno, klass=st.admitted_class, term=term,pin=Pin).save()
                        varurem = 4

              ##########  calc. total bill for the term ******************
                totbil = printbill (admno,session,term)
                allowable_debt = 0.15 * int(totbil)
                allowable_debt = locale.format('%.0f',allowable_debt)
                allowable_debt= int(allowable_debt) # what i can owe
############## cal account balaance *************************************
                acc=tblaccount.objects.get(acccode = admno)
                actual_debt = acc.accbal
                actual_debt = int(actual_debt) # what i'm actually owing
                bal = actual_debt

    
                classtot = 0
                totsub = 0
                totalmarkcount = 0
                st = Student.objects.get(admissionno=admno, admitted_session=session)
                if term == "First":
                    stuno1 = Student.objects.filter(
                        admitted_session = session,
                        first_term = 1, admitted_class = st.admitted_class,
                        admitted_arm = st.admitted_arm,gone = False).count()
                    stuinfo = Student.objects.get(
                        admitted_session = session,
                        admissionno = admno, 
                        first_term = 1)
                elif term == "Second":
                    stuno1 = Student.objects.filter(admitted_session = session,second_term = 1, admitted_class = st.admitted_class,admitted_arm = st.admitted_arm,gone = False).count()
                    stuinfo = Student.objects.get(admitted_session = session, admissionno = admno, second_term = 1)
                else:
                    stuno1 = Student.objects.filter(admitted_session = session,third_term = 1,term = term, admitted_class = varclass,admitted_arm = vararm,gone = False).count()
                    stuinfo = Student.objects.get(admitted_session = session, admissionno = admno, third_term = 1,term=term)
                varclass= stuinfo.admitted_class
                vararm = stuinfo.admitted_arm
                varclas=varclass[0]
                getgrading=gradingsys.objects.filter(classsub__startswith = varclas)
                
                if StudentAcademicRecord.objects.filter(student = stuinfo,term = term):
                    acaderec = StudentAcademicRecord.objects.get(student = stuinfo,term = term)
                    affskill = AffectiveSkill.objects.get(academic_rec = acaderec)
                    psycho = PsychomotorSkill.objects.get(academic_rec = acaderec)
                    subsco = SubjectScore.objects.filter(academic_rec = acaderec,term = term).order_by('num')
                    totsub = SubjectScore.objects.filter(academic_rec = acaderec,term = term).count()
                    totalmark2 = 0
                    if SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term):
                        totalmark = SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term).aggregate(Sum('end_term_score'))
                        totalmark2 = totalmark['end_term_score__sum']
                        totalmarkcount = SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term).count()
                        rtotal = int(totalmark2)
                        if float(totsub) == 0:
                            perc = 0
                        else:
                            perc = float(rtotal)/float(totsub)
                        classtot += rtotal
                        ks = totalmarkcount * 100
                        totsub += ks
                        jdic = {'studentinfo':stuinfo,'academic':acaderec,'affective':affskill,'pyscho':psycho,'subject':subsco,'totalmark':rtotal,'getgrading':getgrading,'percentage':locale.format("%.2f",perc,grouping=True)}
                        replist.append(jdic)
                if classtot == 0 or stuno1 == 0:
                   clavg = 0.0
                else:
                    j = classtot/stuno1
                    clavg =j/float(totalmarkcount)


                #varclas= varclass[0]

                if varclas == 'S':
                    return render_to_response('assessment/reportsss.html',{'form':form,'varu':varurem,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno})

                if varclas == 'N' or varclas == 'K' or varclas == 'P':
                    return render_to_response('assessment/reportnpin.html',{'form':form,'varclas':varclas,'varu':varurem,'bal':bal,'pin':Pin,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno1':stuno1,'classavg':locale.format("%.2f",clavg,grouping=True)})

                if varclas =='J':
                    return render_to_response('assessment/reportpin.html',{'form':form,'varclas':varclas,'varu':varurem,'bal':bal,'pin':Pin,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno1':stuno1,'classavg':locale.format("%.2f",clavg,grouping=True)})


            else:
                varerr='FILL OUT ALL BOXES'
                return render_to_response('assessment/indreport.html',{'form':form, 'varerr':varerr})
        else:
            form = indreportform()
            return render_to_response('assessment/indreport.html',{'form':form,})
    else:
        return HttpResponseRedirect('/login/')

def reportopt(request):
    if "userid" in request.session:
        return render_to_response('assessment/select.html')
    else:
        return HttpResponseRedirect('/login/')

        # user=userprofile.objects.get(username=varuser)
        # uenter=user.createuser
        # if uenter is False:
        #     return HttpResponseRedirect('/welcome/')


def reportsheetnew(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.reportsheet
        if uenter is False :
            return HttpResponseRedirect('/assessment/access-denied/')
        varerr =''
        getdetails =''
        school = get_object_or_404(School, pk=1)
        if request.method == 'POST':
            form = reportsheetform(request.POST)
            if form.is_valid():
                session = form.cleaned_data['session']
                klass = form.cleaned_data['klass']
                term = form.cleaned_data['term']
                arm = form.cleaned_data['arm']
                stuno = Student.objects.filter(admitted_session = session,admitted_class = klass,admitted_arm = arm,gone = False).count()
                stuinfo = Student.objects.filter(admitted_session = session,admitted_class = klass,admitted_arm = arm,gone = False).order_by('-sex','fullname')
                replist = []
                varbeg = klass[0]
                getgrading = gradingsys.objects.filter(classsub__startswith = varbeg)
                classtot = 0
                totsub = 0
                totalmarkcount = 0
                if term == "First":
                    for j in stuinfo:
                        if StudentAcademicRecord.objects.filter(student = j,term = term):
                            acaderec = StudentAcademicRecord.objects.get(student = j,term = term)
                            affskill = AffectiveSkill.objects.get(academic_rec = acaderec)
                            psycho = PsychomotorSkill.objects.get(academic_rec = acaderec)
                            subsco = SubjectScore.objects.filter(academic_rec = acaderec,term = term).order_by('num')
                            totsub = SubjectScore.objects.filter(academic_rec = acaderec,term = term).count()
                            totalmark2 = 0
                            if SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term):
                               totalmark = SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term).aggregate(Sum('term_score'))
                               totalmark2 = totalmark['term_score__sum']
                            totalmarkcount = SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term).count()
                            rtotal = int(totalmark2)
                            if float(totsub) == 0:
                                perc = 0
                            else:
                                perc = float(rtotal)/float(totsub)
                            classtot += rtotal
                            ks = totalmarkcount * 100
                            totsub += ks
                            jdic = {'studentinfo':j,'academic':acaderec,'affective':affskill,'pyscho':psycho,'subject':subsco,'totalmark':rtotal,'getgrading':getgrading,'percentage':locale.format("%.2f",perc,grouping=True)}
                            replist.append(jdic)
                    if classtot == 0 or stuno == 0:
                       clavg = 0.0
                    else:
                        j = classtot/stuno
                        clavg =j/float(totalmarkcount)
                    if klass[0] == 'S':
                        if form.cleaned_data['pdffile']:
                            template ='assessment/reportviewsss.html'
                            context = {'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno}
                            return render_to_pdf(template, context)
                        else:
                            return render_to_response('assessment/reportsss.html',{'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno})

                    elif klass[0] == 'N' or klass[0] == 'C' or klass[0] == 'L':
                        if form.cleaned_data['pdffile']:
                            template ='assessment/reportnview.html'
                            context = {'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)}
                            return render_to_pdf(template, context)
                        else:
                            return render_to_response('assessment/reportn.html',{'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)})

                    else:
                        if form.cleaned_data['pdffile']:
                           template ='assessment/reportview.html'
                           context = {'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)}
                           return render_to_pdf(template, context)
                        else:
                           return render_to_response('assessment/report.html',{'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)})
                elif term == 'Second':
                    for j in stuinfo:
                        if StudentAcademicRecord.objects.filter(student = j,term = term):
                            acaderec = StudentAcademicRecord.objects.get(student = j,term = term)
                            acaderec1 = StudentAcademicRecord.objects.get(student = j,term = 'First')
                            affskill = AffectiveSkill.objects.get(academic_rec = acaderec)
                            psycho = PsychomotorSkill.objects.get(academic_rec = acaderec)
                            totsub = SubjectScore.objects.filter(academic_rec = acaderec,term = term).count()
                            totalmarkcount = SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term).count()
                            subsco = SubjectScore.objects.filter(academic_rec = acaderec,term = term).order_by('num')
                            secsublist = []
                            sdic = {}
                            for h in subsco:
                                if SubjectScore.objects.filter(academic_rec = acaderec1,term = 'First',subject = h.subject).count() == 0:
                                    fscore = '-'
                                else:
                                    fsc = SubjectScore.objects.get(academic_rec = acaderec1,term = 'First',subject = h.subject)
                                    if float(fsc.term_score) <= 0:
                                        fscore = '-'
                                    else:
                                        fsco = fsc.term_score
                                        fscore = str(fsco)
                                secdic ={'secondterm':h,'firstterm':fscore}
                                secsublist.append(secdic)
                            totalmark2 = 0
                            if SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term):
                                totalmark = SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term).aggregate(Sum('term_score'))
                                totalmark2 = totalmark['term_score__sum']
                            rtotal = int(totalmark2)
                            if float(totsub) == 0:
                                perc = 0
                            else:
                                perc = float(rtotal)/float(totsub)
                            classtot += rtotal
                            ks = totalmarkcount * 100
                            totsub += ks

                            #total for first term
                            totalmark2sec = 0
                            rtotalsec = 0
                            if SubjectScore.objects.filter(academic_rec = acaderec1,session = session,term = 'First'):
                                totalmarksec = SubjectScore.objects.filter(academic_rec = acaderec1,session = session,term = 'First').aggregate(Sum('term_score'))
                                totalmark2sec = totalmarksec['term_score__sum']
                                rtotalsec = int(totalmark2sec)

                            jdic = {'studentinfo':j,'academic':acaderec,'affective':affskill,'pyscho':psycho,'subject':secsublist,'totalmark':rtotal,'totalmark1':rtotalsec,'getgrading':getgrading,'percentage':locale.format("%.2f",perc,grouping=True)}
                            replist.append(jdic)
                    if classtot == 0 or stuno == 0:
                            clavg = 0.0
                    else:
                             j = classtot/stuno
                             clavg =j/float(totalmarkcount)
                    if klass[0] == 'S':
                        if form.cleaned_data['pdffile']:
                            template ='assessment/reportviewsecondsss.html'
                            context = {'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno}
                            return render_to_pdf(template, context)
                        else:
                            return render_to_response('assessment/reportsecondsss.html',{'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno})
                    elif klass[0] == 'N' or klass[0] == 'C' or klass[0] == 'L':
                        if form.cleaned_data['pdffile']:
                            template ='assessment/reportnviewsecond.html'
                            context = {'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)}
                            return render_to_pdf(template, context)
                        else:
                            return render_to_response('assessment/reportnsecond.html',{'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)})

                    else:
                        if form.cleaned_data['pdffile']:
                            template ='assessment/reportviewsecond.html'
                            context = {'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)}
                            return render_to_pdf(template, context)
                        else:
                            return render_to_response('assessment/reportsecond.html',{'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)})
                else:
                    stuno = Student.objects.filter(admitted_session = session,admitted_class = klass,gone = False).count()
                    for j in stuinfo:
                        if StudentAcademicRecord.objects.filter(student = j,term = term):
                            acaderec = StudentAcademicRecord.objects.get(student = j,term = term)
                            acaderec1 = StudentAcademicRecord.objects.get(student = j,term = 'First')
                            acaderec2 = StudentAcademicRecord.objects.get(student = j,term = 'Second')
                            affskill = AffectiveSkill.objects.get(academic_rec = acaderec)
                            psycho = PsychomotorSkill.objects.get(academic_rec = acaderec)
                            totsub = SubjectScore.objects.filter(academic_rec = acaderec,term = term).count()
                            totalmarkcount = SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term).count()
                            subsco = SubjectScore.objects.filter(academic_rec = acaderec,term = term).order_by('num')
                            secsublist = []
                            sdic = {}
                            for h in subsco:
                                if SubjectScore.objects.filter(academic_rec = acaderec1,term = 'First',subject = h.subject).count() == 0:
                                    fscore = '-'
                                    fscoret = '-'
                                else:
                                    fsc = SubjectScore.objects.get(academic_rec = acaderec1,term = 'First',subject = h.subject)
                                    if float(fsc.term_score) <= 0:
                                        fscore = '-'
                                    else:
                                        fsco = fsc.term_score
                                        fscore = str(fsco)
                                if SubjectScore.objects.filter(academic_rec = acaderec2,term = 'Second',subject = h.subject).count() == 0:
                                    fscoret = '-'
                                else:
                                    fsct = SubjectScore.objects.get(academic_rec = acaderec2,term = 'Second',subject = h.subject)
                                    if float(fsct.term_score) <= 0:
                                        fscoret ='-'
                                    else:
                                        fscot = fsct.term_score
                                        fscoret = str(fscot)
                                secdic ={'thirdterm':h,'firstterm':fscore,'secondterm':fscoret}
                                secsublist.append(secdic)
                            totalmark = SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term).aggregate(Sum('term_score'))
                            totalmark2 = totalmark['term_score__sum']
                            rtotal = int(totalmark2)
                            perc = float(rtotal)/float(totsub)
                            classtot += rtotal
                            ks = totalmarkcount * 100
                            totsub += ks
                            #total for first term
                            totalmark2sec = 0
                            rtotalsec = 0
                            if SubjectScore.objects.filter(academic_rec = acaderec1,session = session,term = 'First'):
                                totalmarksec = SubjectScore.objects.filter(academic_rec = acaderec1,session = session,term = 'First').aggregate(Sum('term_score'))
                                totalmark2sec = totalmarksec['term_score__sum']
                                rtotalsec = int(totalmark2sec)
                            #*********************************************
                            totalmark2sec1 = 0
                            rtotalsec1 = 0
                            if SubjectScore.objects.filter(academic_rec = acaderec2,session = session,term = 'Second'):
                                totalmarksec1 = SubjectScore.objects.filter(academic_rec = acaderec2,session = session,term = 'Second').aggregate(Sum('term_score'))
                                totalmark2sec1 = totalmarksec1['term_score__sum']
                                rtotalsec1 = int(totalmark2sec1)
                            #**************************************************
                            #annual average
                            totalmark24 = 0
                            rtotal4 = 0
                            if SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term):
                                totalmark4 = SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term).aggregate(Sum('annual_avg'))
                                totalmark24 = totalmark4['annual_avg__sum']
                                rtotal4 = float(totalmark24)
                            #**********************************************
                            jdic = {'studentinfo':j,'academic':acaderec,'affective':affskill,'pyscho':psycho,'subject':secsublist,'totalmark':rtotal,'totalmark1':rtotalsec,'totalmark2':rtotalsec1,'annualavg':locale.format("%.2f",rtotal4,grouping=True),'getgrading':getgrading,'percentage':locale.format("%.2f",perc,grouping=True)}
                            replist.append(jdic)
                    if classtot == 0 or stuno == 0:
                        clavg = 0.0
                    else:
                        j = classtot/stuno
                        clavg =j/float(totalmarkcount)
                    if klass[0] == 'S':
                        if form.cleaned_data['pdffile']:
                            template ='assessment/reportviewthirdsss.html'
                            context = {'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno}
                            return render_to_pdf(template, context)
                        else:
                            return render_to_response('assessment/reportthirdsss.html',{'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno})
                    elif klass[0] == 'N' or klass[0] == 'C' or klass[0] == 'L':
                        if form.cleaned_data['pdffile']:
                            template ='assessment/reportnviewthird.html'
                            context = {'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)}
                            return render_to_pdf(template, context)
                        else:
                            return render_to_response('assessment/reportnthird.html',{'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)})

                    else:
                        if form.cleaned_data['pdffile']:
                            template ='assessment/reportviewthird.html'
                            context = {'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)}
                            return render_to_pdf(template, context)
                        else:
                            return render_to_response('assessment/reportthird.html',{'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)})
        else:
            form = reportsheetform()
        return render_to_response('assessment/report.html',{'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')









def reportsheet(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.createuser
        if uenter is False :
            return HttpResponseRedirect('/assessment/access-denied/')
        varerr =''
        getdetails =''
        # school = get_object_or_404(School, pk=1)
        school=School.objects.get(id =1)
        if request.method == 'POST':
            form = reportsheetform(request.POST)
            if form.is_valid():
                session = form.cleaned_data['session']
                klass = form.cleaned_data['klass']
                term = form.cleaned_data['term']
                arm = form.cleaned_data['arm']
                try:
                  codi = ClassTeacher.objects.get(klass=klass,session=session,teachername='N/A')
                except:
                  codi= 'Not Set'
                replist = []
                
                varbeg = klass[0]
                getgrading = gradingsys.objects.filter(classsub__startswith = varbeg)
                
                
                if term == 'First':
                    stuinfo = Student.objects.filter(first_term = True,admitted_session = session, admitted_class = klass,admitted_arm = arm,gone = False).order_by('fullname')

                    for j in stuinfo:       
                        acaderec = StudentAcademicRecord.objects.get(session=session,student = j,term = term)
                        affective=AffectiveSkill.objects.get(academic_rec=acaderec) 
                        subsco = SubjectScore.objects.filter(academic_rec = acaderec).order_by('num')
                           
                        totalmark12 = 0
                        if SubjectScore.objects.filter(academic_rec=acaderec, term='First').count()>0:
                            totalmark = SubjectScore.objects.filter(academic_rec = acaderec, term='First').aggregate(Sum('end_term_score'))
                            totalmark12 = totalmark['end_term_score__sum']
                            totalmark12 = int(totalmark12)

                        jdic = {'totalmark':totalmark12,'studentinfo':j,'affective':affective,'codi':codi,'grading':getgrading, 'academic':acaderec,'subject':subsco}
                        replist.append(jdic)

                    if varbeg=='J':
                        return render_to_response('assessment/mysummarysheet.html',{'varuser':varuser,'school':school,'form':form,'date':date,'varerr':varerr,'replist':replist,'term':term})
                    
                elif term=='Second':
                    stuinfo = Student.objects.filter(second_term = True,admitted_session = session, admitted_class = klass,admitted_arm = arm,gone = False).order_by('fullname')

                    for j in stuinfo:
                        acaderec = StudentAcademicRecord.objects.get(student = j,term = term,session=session)           
                        affective=AffectiveSkill.objects.get(academic_rec=acaderec)
                        subsco = SubjectScore.objects.filter(academic_rec = acaderec,term = term ,session=session).order_by('num')

                        festrec='False'
                        try:
                            acaderec1 = StudentAcademicRecord.objects.get(student = j,term = 'First',session=session)
                        except:
                            festrec='True'

                        totalmark2 = 0
                        
                        totalmark = SubjectScore.objects.filter(academic_rec = acaderec).aggregate(Sum('end_term_score'))
                        totalmark2 = totalmark['end_term_score__sum']
                        totalmark2 = int(totalmark2)

                        totalmark12 = 0
                        if festrec=='False': #IE FIRST TERM RECORD FOUND
                            totalmarkk = SubjectScore.objects.filter(academic_rec = acaderec1,term='First',session=session).aggregate(Sum('end_term_score'))
                            totalmark12 = totalmarkk['end_term_score__sum']
                            totalmark12 = int(totalmark12)
                        else:
                            totalmark12=0
                        

                        secsublist = []
                        secdic = {}

                        for h in subsco:
                            if festrec=='True': #IE NO FIRST TERM RECORD
                                fscore = '-'
                            else:
                                fsc = SubjectScore.objects.get(academic_rec = acaderec1,term = 'First',subject = h.subject,session=session)
                                fsco = fsc.end_term_score
                                fscore = str(fsco)
                            secdic ={'secondterm':h,'firstterm':fscore}
                            secsublist.append(secdic)

                        jdic = {'totalmark2':totalmark2,'totalmark1':totalmark12,'studentinfo':j,'affective':affective,'codi':codi,'grading':getgrading, 'academic':acaderec,'subject':secsublist}
                        replist.append(jdic)
             
                    if varbeg=='J':
                        return render_to_response('assessment/reportnsecond.html',{'varuser':varuser,'school':school,'form':form,'date':date, 'varerr':varerr,'replist':replist,'term':term})



                elif term =='Third':
                    stuinfo = Student.objects.filter(third_term = True,admitted_session = session, admitted_class = klass,admitted_arm = arm,gone = False)#.order_by('fullname')
                                       
                    for j in stuinfo:
                        acaderec = StudentAcademicRecord.objects.get(student = j,term = term,session=session)
                        affskill = AffectiveSkill.objects.get(academic_rec = acaderec)
                        psycho = PsychomotorSkill.objects.get(academic_rec = acaderec)
                        subsco = SubjectScore.objects.filter(academic_rec = acaderec,term = term,session = session).order_by('num')

 ##OBTAINING FIRST TERM RECORDS *******************                                                   
                        firstrec='False'
                        secrec='False'
                        try:
                            acaderec1 = StudentAcademicRecord.objects.get(student = j,term = 'First',session=session)
                        except:
                            firstrec='True'
                                                       
 ##OBTAINING SECOND TERM RECORDS *******************
                        try:
                            acaderec2 = StudentAcademicRecord.objects.get(student = j,term = 'Second',session=session)
                        except:
                            secrec='True'

                        secsublist = []
                        secdic = {}

                        for h in subsco:
                            if firstrec=='True':
                                fscore = '-'
                            else:
                                fsc = SubjectScore.objects.get(session=session, academic_rec = acaderec1,term = 'First',subject = h.subject)
                                fsco = fsc.end_term_score
                                fscore = str(fsco)

                            if secrec=='True':
                                fscoret = '-'
                            else:
                                fsct = SubjectScore.objects.get(session=session, academic_rec = acaderec2,term = 'Second',subject = h.subject)
                                fscot = fsct.end_term_score
                                fscoret = str(fscot)
                            secdic ={'thirdterm':h,'firstterm':fscore,'secondterm':fscoret}
                            secsublist.append(secdic)
                        
                        

                        rtotals=0
                        totalmark = SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term).aggregate(Sum('end_term_score'))
                        totalmark2 = totalmark['end_term_score__sum']
                        rtotals = int(totalmark2)



                        #******total for first term*********************

                        totalmark2sec = 0
                        rtotalsec = 0
                        

                        if firstrec=='False':# IE IF FIRST TERM RECORD IS FOUND
                            totalmarksec = SubjectScore.objects.filter(academic_rec = acaderec1,session = session,term = 'First').aggregate(Sum('end_term_score'))
                            totalmark2sec = totalmarksec['end_term_score__sum']
                            rtotalsec = int(totalmark2sec)
                        else:
                            rtotalsec = 0


                        #*******total for second term***************************
                        totalmark2sec1 = 0
                        rtotalsec1 = 0

                        if secrec=='False':#IE SECOND TERM RECORD IS FOUND
                            totalmarksec1 = SubjectScore.objects.filter(academic_rec = acaderec2,session = session,term = 'Second').aggregate(Sum('end_term_score'))
                            totalmark2sec1 = totalmarksec1['end_term_score__sum']
                            rtotalsec1 = int(totalmark2sec1)

                        else:
                            rtotalsec1 = 0

                        #*************************#annual average********************
                        totalmark24 = 0
                        rtotal4 = 0
                        totalmark4 = SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term).aggregate(Sum('annual_avg'))
                        totalmark24 = totalmark4['annual_avg__sum']
                        rtotal4 = float(totalmark24)


                        #**********************************************
                        jdic = {'studentinfo':j,'academic':acaderec,'affective':affskill,'pyscho':psycho,'subject':secsublist,'totalmark':rtotals,'totalmark1':rtotalsec,'totalmark2':rtotalsec1,'annualavg':locale.format("%.2f",rtotal4,grouping=True),'getgrading':getgrading}
                        replist.append(jdic)

                    if klass[0] == 'S':
                        # if form.cleaned_data['pdffile']:
                        #     template ='assessment/reportviewthirdsss.html'
                        #     context = {'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno}
                        #     return render_to_pdf(template, context)
                        # else:
                        return render_to_response('assessment/reportthirdsss.html',{'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno})
                    elif klass[0] == 'N' or klass[0] == 'C' or klass[0] == 'L':
                        # if form.cleaned_data['pdffile']:
                        #     template ='assessment/reportnviewthird.html'
                        #     context = {'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)}
                        #     return render_to_pdf(template, context)
                        # else:
                        return render_to_response('assessment/reportnthird.html',{'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)})

                    else:
                        # if form.cleaned_data['pdffile']:
                        #     template ='assessment/reportviewthird.html'
                        #     context = {'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)}
                        #     return render_to_pdf(template, context)
                        # else:
                        return render_to_response('assessment/reportthird.html',{'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term})

        else:
            form = reportsheetform()
        return render_to_response('assessment/report.html',{'varuser':varuser,'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')

#***********************************************treating MID-TERM Report ****************************
def reportsheetmidterm(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.createuser
        if uenter is False :
            return HttpResponseRedirect('/assessment/access-denied/')
        varerr =''
        getdetails =''
      #  school = get_object_or_404(School, pk=1)
        school=School.objects.get(id =1)
        if request.method == 'POST':
            form = reportsheetmidform(request.POST)
            if form.is_valid():
                session = form.cleaned_data['session']
                klass = form.cleaned_data['klass']
                term = form.cleaned_data['term']
                arm = form.cleaned_data['arm']
                ca = form.cleaned_data['ca']
                
                if term=='First':
                    stuinfo = Student.objects.filter(first_term=True,
                        admitted_session = session,
                        admitted_class = klass,
                        admitted_arm = arm,
                        gone = False).order_by('fullname')
                    stuno = Student.objects.filter(first_term=True,
                        admitted_session = session,
                        admitted_class = klass,
                        admitted_arm = arm,
                        gone = False).count()
                elif term=='Second':
                    stuinfo = Student.objects.filter(second_term=True,
                        admitted_session = session,
                        admitted_class = klass,
                        admitted_arm = arm,
                        gone = False).order_by('fullname')
                    stuno = Student.objects.filter(second_term=True,
                        admitted_session = session,
                        admitted_class = klass,
                        admitted_arm = arm,
                        gone = False).count()
                else:
                    stuinfo = Student.objects.filter(third_term=True,
                        admitted_session = session,
                        admitted_class = klass,
                        admitted_arm = arm,
                        gone = False).order_by('fullname')
                    stuno= Student.objects.filter(third_term=True,
                        admitted_session = session,
                        admitted_class = klass,
                        admitted_arm = arm,
                        gone = False).count()


                try:
                  codi = ClassTeacher.objects.get(klass=klass,session=session,teachername='N/A')
                except:
                  codi='Not Available'
                if ca == '1st CA':
                    replist = []
                    varbeg = klass[0]
                    for j in stuinfo:
                        totsub = 0
                        acaderec = StudentAcademicRecord.objects.get(student = j,term = term)
                        psycho = PsychomotorSkill.objects.get(academic_rec = acaderec)
                        subsco = SubjectScore.objects.filter(academic_rec = acaderec).order_by('num')
                        totsub = SubjectScore.objects.filter(academic_rec = acaderec).count()
                        msublist = []
                        for jj in subsco:
                            fca = jj.first_ca
                            totalperc1 = fca/20
                            totalperc = totalperc1 * 100
                            if varbeg == 'S':
                                remark = seniorgrade(float(totalperc))                                    
                            else:
                                remark = juniorgrade(float(totalperc))
                            msub = {'subject':jj.subject,
                            'first_ca':fca,
                            'totalperc':locale.format("%.1f",totalperc,grouping=True),
                            'remark':remark['remark'],
                            'grade':remark['grade'],
                            'teacher':jj.subject_teacher}
                            msublist.append(msub)
                        #****************all i need in report******************************
                        jdic = {'date':date,
                        'codi':codi,
                        'studentinfo':j,
                        'academic':acaderec,
                        'pyscho':psycho,
                        'subject':msublist}
                        replist.append(jdic)

                    return render_to_response('assessment/midreport1.html',{'session':session, 
                        'form':form,
                        'varuser':varuser,
                        'varerr':varerr,
                        'replist':replist,
                        'school':school,
                        'term':term})

                elif ca == '2nd CA':
                    replist = []
                    varbeg = klass[0]
                    for j in stuinfo:
                        totsub = 0
                        acaderec = StudentAcademicRecord.objects.get(student = j,term = term)
                        psycho = PsychomotorSkill.objects.get(academic_rec = acaderec)
                        subsco = SubjectScore.objects.filter(academic_rec = acaderec).order_by('num')
                        totsub = SubjectScore.objects.filter(academic_rec = acaderec).count()
                        msublist = []
                        for jj in subsco:
                            sca = jj.second_ca
                            totalperc1 = sca/20
                            totalperc = totalperc1 * 100
                            if varbeg == 'S':
                                remark = seniorgrade(float(totalperc))                                    
                            else:
                                remark = juniorgrade(float(totalperc))
                            msub = {'subject':jj.subject,
                            'second_ca':sca,
                            'totalperc':locale.format("%.1f",totalperc,grouping=True),
                            'remark':remark['remark'],
                            'grade':remark['grade'],
                            'teacher':jj.subject_teacher}
                            msublist.append(msub)
                        #****************all i need in report******************************
                        jdic = {'date':date,
                        'codi':codi,
                        'studentinfo':j,
                        'academic':acaderec,
                        'pyscho':psycho,
                        'subject':msublist}
                        replist.append(jdic)

                    return render_to_response('assessment/midreport2.html',{
                        'session':session,
                        'varuser':varuser, 
                        'form':form,
                        'varerr':varerr,
                        'replist':replist,
                        'school':school,
                        'term':term})
        else:
            form = reportsheetmidform()
        return render_to_response('assessment/reportmid.html',{'varuser':varuser,'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')




#*****************************************************************************************************
def broadsheet(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.createuser
        if uenter is False :
            return HttpResponseRedirect('/assessment/access-denied/')
        varerr =''
        getdetails =''
        school = get_object_or_404(School, pk=1)
        if request.method == 'POST':
            form = broadsheetform(request.POST)
            if form.is_valid():
                session = form.cleaned_data['session']
                klass = form.cleaned_data['klass']
                term = form.cleaned_data['term']
                arm = form.cleaned_data['arm']
                #***********************************************getting the subjects
                if klass.startswith('J'):
                    k= Subject.objects.filter(category='JS').order_by('num')
                elif klass.startswith('Y'):
                    k= Subject.objects.filter(category='Year').order_by('num')
                else:
                    k= Subject.objects.all().exclude(category='Year').exclude(category='JS').order_by('num')
                subjdic = {}
                for sub in k:
                    jk = {sub.subject:sub.subject}
                    subjdic.update(jk)
                sublist = subjdic.keys()
                #print 'the subject list :',sublist
                #*************************************************************************
                if klass.startswith('S'):
                    ll = bsheetforsa(term,session,klass,arm)
                    response = HttpResponse(mimetype="application/ms-excel")
                    response['Content-Disposition'] = 'attachment; filename=broadsheet.xls'
                    wb = xlwt.Workbook()
                    ws = wb.add_sheet('broadsheet')
                    ws.write(0, 2, school.name)
                    ws.write(1, 2, school.address)
                    ws.write(2, 2, '%s %s %s Term Broad Sheet for %s Session' %(klass,arm, term, session) )
                    v = 2
                    ws.write(3,0,'Admission No')
                    ws.write(3,1,'Student Name')
                    for p in sublist:
                        ws.write(3, v, p)
                        v += 1
                    ws.write(3, v, 'GRADE')
                    k = 4
                    for jd in ll:
                       c = 2
                       ws.write(k, 0, jd['admno'])
                       ws.write(k, 1, jd['stname'])
                       for q in sublist:
                           ws.write(k, c, jd['subjects'][q])
                           c += 1
                       ws.write(k, c, jd['grade'])
                       k += 1
                    wb.save(response)
                    # return response
                else:
                   ll = bsheetforja(term,session,klass,arm)
                   response = HttpResponse(mimetype="application/ms-excel")
                   response['Content-Disposition'] = 'attachment; filename=broadsheet.xls'
                   wb = xlwt.Workbook()
                   ws = wb.add_sheet('broadsheet')
                   ws.write(0, 2, school.name)
                   ws.write(1, 2, school.address)
                   ws.write(2, 2, '%s %s %s Term Broad Sheet for %s Session' %(klass,arm, term, session) )
                   v = 2
                   ws.write(3,0,'Admission No')
                   ws.write(3,1,'Student Name')
                   for p in sublist:
                       ws.write(3, v, p)
                       v += 1
                   ws.write(3, v, 'TOTAL SCORE')
                   v += 1
                   ws.write(3, v, 'AVERAGE SCORE')
                   v += 1
                   ws.write(3, v, 'POSITION')
                   k = 4
                   for jd in ll:
                       c = 2
                       ws.write(k, 0, jd['studentlist']['admno'])
                       ws.write(k, 1, jd['studentlist']['stname'])
                       for q in sublist:
                           ws.write(k, c, jd['studentlist']['subjects'][q])
                           c += 1
                       ws.write(k, c, jd['studentlist']['totalscore'])
                       c += 1
                       ws.write(k, c, '%.2f'%jd['studentlist']['avgscore'])
                       c += 1
                       ws.write(k, c, jd['pos'])
                       k += 1
                   wb.save(response)
                return response
                # return HttpResponseRedirect('/assessment/broadsheet/','response':response)
                # return render_to_response('assessment/broadsheet.html',{'varuser':varuser,'form':form,'varerr':varerr})
                        #end of position
        else:
            form = broadsheetform()
        return render_to_response('assessment/broadsheet.html',{'varuser':varuser,'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')
#********************************************************Mid Term Broad Sheet *****************************************
def mid_term_broadsheet(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.reportsheet
        if uenter is False :
            return HttpResponseRedirect('/assessment/access-denied/')
        varerr =''
        getdetails =''
        school = get_object_or_404(School, pk=1)
        if request.method == 'POST':
            form = broadsheetform(request.POST)
            if form.is_valid():
                session = form.cleaned_data['session']
                klass = form.cleaned_data['klass']
                term = form.cleaned_data['term']
                #***********************************************getting the subjects
                if klass.startswith('J'):
                    k= Subject.objects.filter(category='JS').order_by('num')
                elif klass.startswith('Y'):
                    k= Subject.objects.filter(category='Year').order_by('num')
                else:
                    k= Subject.objects.all().exclude(category='Year').exclude(category='JS').order_by('num')
                subjdic = {}
                for sub in k:
                    jk = {sub.subject:sub.subject}
                    subjdic.update(jk)
                sublist = subjdic.keys()
                #print 'the subject list :',sublist
                #*************************************************************************
                if klass.startswith('S'):
                    ll = mid_term_bsheetfors(term,session,klass)
                    response = HttpResponse(mimetype="application/ms-excel")
                    response['Content-Disposition'] = 'attachment; filename=broadsheet.xls'
                    wb = xlwt.Workbook()
                    ws = wb.add_sheet('broadsheet')
                    ws.write(0, 2, school.name)
                    ws.write(1, 2, school.address)
                    ws.write(2, 2, '%s %s Term Broad Sheet for %s Session' %(klass,term, session) )
                    v = 2
                    ws.write(3,0,'Admission No')
                    ws.write(3,1,'Student Name')
                    for p in sublist:
                        ws.write(3, v, p)
                        v += 1
                    ws.write(3, v, 'GRADE')
                    k = 4
                    for jd in ll:
                       c = 2
                       ws.write(k, 0, jd['admno'])
                       ws.write(k, 1, jd['stname'])
                       for q in sublist:
                           ws.write(k, c, jd['subjects'][q])
                           c += 1
                       ws.write(k, c, jd['grade'])
                       k += 1
                    wb.save(response)
                    return response
                else:
                   ll = mid_term_bsheetforj(term,session,klass)
                   response = HttpResponse(mimetype="application/ms-excel")
                   response['Content-Disposition'] = 'attachment; filename=broadsheet.xls'
                   wb = xlwt.Workbook()
                   ws = wb.add_sheet('broadsheet')
                   ws.write(0, 2, school.name)
                   ws.write(1, 2, school.address)
                   ws.write(2, 2, '%s %s Term Broad Sheet for %s Session' %(klass,term, session) )
                   v = 2
                   ws.write(3,0,'Admission No')
                   ws.write(3,1,'Student Name')
                   for p in sublist:
                       ws.write(3, v, p)
                       v += 1
                   ws.write(3, v, 'TOTAL SCORE')
                   v += 1
                   ws.write(3, v, 'AVERAGE SCORE')
                   v += 1
                   ws.write(3, v, 'POSITION')
                   k = 4
                   for jd in ll:
                       c = 2
                       ws.write(k, 0, jd['studentlist']['admno'])
                       ws.write(k, 1, jd['studentlist']['stname'])
                       for q in sublist:
                           ws.write(k, c, jd['studentlist']['subjects'][q])
                           c += 1
                       ws.write(k, c, jd['studentlist']['totalscore'])
                       c += 1
                       ws.write(k, c, '%.2f'%jd['studentlist']['avgscore'])
                       c += 1
                       ws.write(k, c, jd['pos'])
                       k += 1
                   wb.save(response)
                   return response
                return render_to_response('assessment/midtermbroadsheet.html',{'form':form,'varerr':varerr})
                        #end of position
        else:
            form = broadsheetform()
        return render_to_response('assessment/midtermbroadsheet.html',{'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')



#*****************************************Taking Care Of Returning function for primary School**************************
def primary_url(request,session1,klass1,arm1,name1,term1):
        pry = ''
        for j in appused.objects.all():
            pry = j.primary
        if pry is True :
            pass
        else:
            return HttpResponseRedirect('/assessment/access-denied/')
        session = str(session1).replace('j','/')
        klass = str(klass1).replace('k',' ')
        arm = str(arm1).replace('k',' ')
        name11 = str(name1).replace('z',' ')
        fname2 = name11.replace('i','-')
        name  = fname2.replace('u',"'")
        term = str(term1).replace('0',' ')
        getdetails = ''
        getstu = Student.objects.get(admitted_class = klass,admitted_arm=arm,admitted_session = session,fullname = name)
        if StudentAcademicRecord.objects.filter(student = getstu,term = term):
            comm = StudentAcademicRecord.objects.get(student = getstu,term = term)
            getdetails = SubjectScore.objects.filter(session = session,klass = klass, arm = arm,term = term,academic_rec = comm).order_by('num')
        return render_to_response('assessment/subjectpry1.html',{'getdetails':getdetails,'session':session,'klass':klass,'arm':arm , 'd':getstu})

#*****************************************Taking Care Of Returning function for Secondary School**************************
def secondary_url(request,session1,klass1,arm1,name1,term1,grp,rep):
    varuser = request.session['userid']
    sec = ''
    for j in appused.objects.all():
        sec = j.secondary
    if sec is True :
        pass
    else:
        return HttpResponseRedirect('/assessment/access-denied/')
    session = str(session1).replace('j','/')
    klass = str(klass1).replace('k',' ')
    arm = str(arm1).replace('k',' ')
    grp = str(grp).replace('m',' ')
    grp1 = str(grp).replace(' ','m')
    subject = str(name1).replace('k',' ')
    term = str(term1).replace('0',' ')
    rep=str(rep).replace('p',' ')
    stlist = []

    if grp =='ALL':

        for j in Student.objects.filter(admitted_session = session,admitted_class = klass,admitted_arm = arm,gone = False).order_by('fullname'):
            if StudentAcademicRecord.objects.filter(student = j,session = session,term = term):
                st = StudentAcademicRecord.objects.get(student = j,session = session,term = term)
                if SubjectScore.objects.filter(academic_rec = st,klass = klass,subject = subject,session = session,arm=arm,term =term):
                    gs = SubjectScore.objects.get(academic_rec = st,
                        klass = klass,
                        subject = subject,
                        session = session,
                        arm=arm,
                        term =term)

                    kk = {'id':gs.id,
                    'admissionno':j.admissionno,
                    'fullname':j.fullname,
                    'sex':j.sex,
                    'subject':gs.subject,
                    'term':str(term),
                    'first_ca':gs.first_ca,
                    'second_ca':gs.second_ca,                    
                    'third_ca':gs.third_ca,
                    'fourth_ca':gs.fourth_ca,
                    'fifth_ca':gs.fifth_ca,
                    'sixth_ca':gs.sixth_ca,
                    'exam_score':gs.end_term_score}
                    stlist.append(kk)
                else:
                    pass

        if rep == 'Mid term':
            # if klass == 'JS 1' or klass == 'SS 1':
            return render_to_response('assessment/casecond.htm',{'varuser':varuser,'data':stlist,'session':session,'klass':klass,'arm':arm,'subject':subject,'session1':session1,'klass1':klass1,'arm1':arm1,'name1':name1,'term1':term1,'rep':rep})
            # else:
                # return render_to_response('assessment/caredirect.htm',{'varuser':varuser,'data':stlist,'session':session,'klass':klass,'arm':arm,'subject':subject,'session1':session1,'klass1':klass1,'arm1':arm1,'name1':name1,'term1':term1})
        elif rep== 'End term':
            return render_to_response('assessment/caredirect.htm',{'varuser':varuser,'data':stlist,'session':session,'klass':klass,'arm':arm,'subject':subject,'session1':session1,'klass1':klass1,'arm1':arm1,'name1':name1,'term1':term1,'rep':rep})
    else:

        for j in Student.objects.filter(admitted_session = session,admitted_class = klass,gone = False).order_by('fullname'):
            if StudentAcademicRecord.objects.filter(student = j,session = session,term = term):
                st = StudentAcademicRecord.objects.get(student = j,session = session,term = term)
                if SubjectScore.objects.filter(academic_rec = st,klass = klass,subject = subject,session = session,subject_group=grp,term =term):
                    gs = SubjectScore.objects.get(academic_rec = st,
                        klass = klass,
                        subject = subject,
                        session = session,
                        term =term)
                    
                    kk = {'id':gs.id,
                    'admissionno':j.admissionno,
                    'arm':gs.arm,
                    'fullname':j.fullname,
                    'sex':j.sex,
                    'subject':gs.subject,
                    'term':str(term),
                    'first_ca':gs.first_ca,
                    'second_ca':gs.second_ca,
                    'third_ca':gs.third_ca,
                    'fourth_ca':gs.fourth_ca,
                    'fifth_ca':gs.fifth_ca,
                    'sixth_ca':gs.sixth_ca,
                    'exam_score':gs.end_term_score}
                    stlist.append(kk)

        if rep =='Mid term':
            # if klass == 'JS 1' or klass1 == 'SS 1':
                return render_to_response('assessment/grpbased.html',{'grp1':grp,'varuser':varuser,'data':stlist,'session':session,'klass':klass,'subject':subject,'session1':session1,'klass1':klass1,'grp':grp1,'name1':name1,'term1':term1})
            # else:
                # return render_to_response('assessment/caredirect.htm',{'varuser':varuser,'data':stlist,'session':session,'klass':klass,'arm':arm,'subject':subject,'session1':session1,'klass1':klass1,'arm1':arm1,'name1':name1,'term1':term1})
        else:
            return render_to_response('assessment/casecond.htm',{'varuser':varuser,'data':stlist,'session':session,'klass':klass,'arm':arm,'subject':subject,'session1':session1,'klass1':klass1,'arm1':arm1,'name1':name1,'term1':term1})




#*****************************************Printing Secondary School Teacher Report**************************

def secondary_teacher_report(request,session1,klass1,arm1,name1,reporttype,term1):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        session = str(session1).replace('j','/')
        klass = str(klass1).replace('k',' ')
        arm = str(arm1).replace('m',' ')
        subject = str(name1).replace('k',' ')
        term = str(term1).replace('0',' ')
        reporttype = str(reporttype).replace('w',' ')
        stlist = []
        school = get_object_or_404(School, pk=1)

        try:
            Arm.objects.get(arm=arm)
            for j in Student.objects.filter(admitted_session = session,admitted_class = klass,admitted_arm = arm,gone = False).order_by('fullname'):
                if StudentAcademicRecord.objects.filter(student = j,session = session,term = term):
                    st = StudentAcademicRecord.objects.get(student = j,session = session,term = term)
                    if SubjectScore.objects.filter(academic_rec = st,klass = klass,subject = subject,session = session,arm=arm,term =term):
                        
                        gs = SubjectScore.objects.get(academic_rec = st,
                            klass = klass,
                            subject = subject,
                            session = session,
                            arm=arm,
                            term =term)
                        
                        kk = {'id':gs.id,
                        'arm':j.admitted_arm,
                        'klass':j.admitted_class,
                        'admissionno':j.admissionno,
                        'fullname':j.fullname,
                        'subject':gs.subject,
                        'term':str(term),
                        'first_ca':gs.first_ca,
                        'second_ca':gs.second_ca,
                        'third_ca':gs.third_ca,
                        'unified_test':gs.fifth_ca,
                        'exam_score':gs.mid_term_score,
                        'termscore':gs.end_term_score,
                        'remark':gs.grade,
                        'position':gs.subposition}
                        stlist.append(kk)
        except:
            for j in Student.objects.filter(admitted_session = session,admitted_class = klass,gone = False).order_by('fullname'):
                if StudentAcademicRecord.objects.filter(student = j,session = session,term = term):
                    st = StudentAcademicRecord.objects.get(student = j,session = session,term = term)
                    if SubjectScore.objects.filter(academic_rec = st,klass = st.klass,subject = subject,session = session,subject_group=arm,term =term):
                        gs = SubjectScore.objects.get(academic_rec = st,
                            klass = st.klass,
                            subject = subject,
                            session = session,
                            subject_group=arm,
                            term =term)
                        
                        kk = {'arm1':j.admitted_arm,
                        'klass':j.admitted_class,
                        'id':gs.id,
                        'admissionno':j.admissionno,
                        'fullname':j.fullname,
                        'sex':j.sex,
                        'subject':gs.subject,
                        'term':str(term),
                        'first_ca':gs.first_ca,
                        'unified_test':gs.unified_test,
                        'second_ca':gs.second_ca,
                        'third_ca':gs.third_ca,
                        'exam_score':gs.exam_score,
                        'termscore':gs.end_term_score,
                        'remark':gs.grade,
                        'position':gs.subposition}
                        stlist.append(kk)

        if reporttype == "Mid term":
            return render_to_response('assessment/printcamid.html',{'data':stlist,'name1':name1,'session':session,'klass':klass,'arm':arm,'subject':subject,'term':term,'teacher':str(user.staffname).title(),'school':school})
        else:
            return render_to_response('assessment/printca.htm',{'data':stlist,'name1':name1,'session':session,'klass':klass,'arm':arm,'subject':subject,'term':term,'teacher':str(user.staffname).title(),'school':school})


    else:
        return HttpResponseRedirect('/login/')
