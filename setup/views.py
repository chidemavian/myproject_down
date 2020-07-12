# Create your views here.

from django.shortcuts import render_to_response
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from myproject.setup.forms import *
from myproject.setup.models import *
from myproject.sysadmin.models import *
from myproject.student.models import *
from myproject.academics.models import *
import datetime
from datetime import date
import xlrd
import xlwt
from django.contrib.admin.views.decorators import staff_member_required
currse = currentsession.objects.get(id = 1)


def welcome(request):
    if  "userid" in request.session:
        varuser=request.session['userid']
        return render_to_response('setup/success1.html',{'varuser':varuser})
    else:
        return HttpResponseRedirect('/login/')

def classarm(request):
    if  "userid" in request.session:
         varuser = request.session['userid']
         user = userprofile.objects.get(username = varuser)
         uenter = user.setup
         getdetails = Class.objects.all().order_by('klass')
         getarm = Arm.objects.all().order_by('arm')
         if uenter is False :
            return HttpResponseRedirect('/unauthorised/')
         varerr = ''
         form2 = ArmForm()

         if request.method == 'POST':
           form = ClassForm(request.POST) # A form bound to the POST data
           if form.is_valid():
                klass = form.cleaned_data['klass']
                if Class.objects.filter(klass = klass.upper()).count() == 0:
                   savecon = Class(klass = klass.upper())
                   savecon.save()
                   return HttpResponseRedirect('/setup/class/')
                else:
                    varerr ='Class Already in Set Up'
                return render_to_response('setup/class_and_arm.html',{'form':form,'form2':form2,'class':getdetails,'arm':getarm,'varerr':varerr})

         else:
           form = ClassForm()
         return render_to_response('setup/class_and_arm.html',{'varuser':varuser,'form':form,'form2':form2,'class':getdetails,'arm':getarm})
    else:
        return HttpResponseRedirect('/login/')


def addarm(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.setup
        getdetails = Class.objects.all().order_by('klass')
        getarm = Arm.objects.all().order_by('arm')
        if uenter is False :
           return HttpResponseRedirect('/unauthorised/')
        varerr =''
        form = ClassForm()
        form2 = ArmForm()
        if request.method == 'POST':
            form2 = ArmForm(request.POST) # A form bound to the POST data
            if form2.is_valid():
                arm = form2.cleaned_data['arm']
                if Arm.objects.filter(arm = arm.upper()).count() == 0:
                   savecon = Arm(arm = arm.upper())
                   savecon.save()
                   return HttpResponseRedirect('/setup/arm/')
                else:
                    varerr = 'Arm in Existence'
                    return render_to_response('setup/arm.html',{'form':form,'form2':form2,'class':getdetails,'arm':getarm,'varerr':varerr})

        else:
            form = ClassForm()

        return render_to_response('setup/arm.html',{'form':form,'form2':form2,'varuser':varuser,'class':getdetails,'arm':getarm})
    else:
        return HttpResponseRedirect('/login/')


def deleteclasscode(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        getdetails = Class.objects.get(id = invid)
        k = getdetails.klass
        if Student.objects.filter(admitted_class = k ).count() == 0 :
            seldata = Class.objects.get(id = invid)
            seldata.delete()
            return HttpResponseRedirect('/setup/class/')
        else:
            varerr = 'Students already in this class'
            form = ClassForm()
            form2 = ArmForm()
            getdetails = Class.objects.all().order_by('klass')
            getarm = Arm.objects.all().order_by('arm')
            return render_to_response('setup/class_and_arm.html',{'form':form,'form2':form2,'class':getdetails,'arm':getarm,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')



def deletearmcode(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        getdetails = Arm.objects.get(id = invid)
        k = getdetails.arm
        if Student.objects.filter(admitted_arm = k ).count() == 0 :
            seldata = Arm.objects.get(id = invid)
            seldata.delete()
            return HttpResponseRedirect('/setup/arm/')
        else:
            varerr = 'Students already in this Arm'
            form = ClassForm()
            form2 = ArmForm()
            getdetails = Class.objects.all().order_by('klass')
            getarm = Arm.objects.all().order_by('arm')
            return render_to_response('setup/arm.html',{'form':form,'form2':form2,'class':getdetails,'arm':getarm,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')



def subject(request):
    if  "userid" in request.session:
         varuser = request.session['userid']
         user = userprofile.objects.get(username = varuser)
         uenter = user.setup
         if uenter is False :
            return HttpResponseRedirect('/unauthorised/')
         sublist = ['KG','Nursery','PRY','JS','Art','Science','Commercial','Science/Math','Technology']
         suball = []
         for p in sublist:
             subcat = Subject.objects.filter(category = p).order_by('subject')  #num is a count of similar entries in the db
             sbdic = {'category':p,'subject':subcat}
             suball.append(sbdic)
         varerr =''
         if request.method == 'POST':
            form = SubjectForm(request.POST) # A form bound to the POSTED data
            if form.is_valid():
               category = form.cleaned_data['category']
               cat2 = form.cleaned_data['category2']
               subj = form.cleaned_data['subject']
               # ca = form.cleaned_data['ca']
               # exam = form.cleaned_data['exam']
               subj = subj.upper()
              #cat2 = cat2.upper()
               if Subject.objects.filter(subject=subj, category=category):
                   varerr = 'This Subject Already Exists!'
                   return render_to_response('setup/subjects.html',{'form':form,'varerr':varerr})
               vcount = Subject.objects.filter(category=category).count()
               vcount1 = vcount + 1
               #print vcount,vcount1
               savecon = Subject(status= 'INACTIVE', category = category,category2 = cat2, subject = subj,ca = 40,exam = 60,num = vcount1)
               savecon.save()
               return HttpResponseRedirect('/setup/subject/')
         else:
             form = SubjectForm()
         return render_to_response('setup/subjects.html',{'varuser':varuser,'form':form,'suball':suball,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')


def subjectgroup(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.setup
        getdetails = Subject_group.objects.all().order_by('subject_group')
        getarm = Subject_group.objects.all().order_by('subject_group')
        if uenter is False :
           return HttpResponseRedirect('/unauthorised/')
        varerr =''
        form = subject_groupForm()
        if request.method == 'POST':
            form = subject_groupForm(request.POST) # A form bound to the POST data
            if form.is_valid():
                subgroup = form.cleaned_data['subject_group']
                if Subject_group.objects.filter(subject_group = subgroup.upper()).count() == 0:
                   savecon = Subject_group(subject_group = subgroup.upper())
                   savecon.save()
                   return HttpResponseRedirect('/setup/subject_group/')
                else:
                    varerr = 'Arm in Existence'
                    return render_to_response('setup/subject_group.html',{'form':form,'form2':form2,'class':getdetails,'arm':getarm,'varerr':varerr})

        else:
            form = subject_groupForm()

        return render_to_response('setup/subject_group.html',{'form':form,'varuser':varuser,'class':getdetails,'arm':getarm})
    else:
        return HttpResponseRedirect('/login/')


def deletesubjectgroupcode(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        getdetails = Subject_group.objects.get(id = invid)
        k = getdetails.subject_group
        if SubjectScore.objects.filter(subject_group = k ).count() == 0 :
            seldata = Subject_group.objects.get(id = invid)
            seldata.delete()
            return HttpResponseRedirect('/setup/subject_group/')
        else:
            varerr = 'Students already have this group'
            form = subject_groupForm()
            getarm = Subject_group.objects.all().order_by('id')
            return render_to_response('setup/subject_group.html',{'form':form,'arm':getarm,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')



def house(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.setup
        if uenter is False :
            return HttpResponseRedirect('/unauthorised/')
        varerr =''
        getdetails = House.objects.all().order_by('house')
        if request.method == 'POST':
            form = HouseForm(request.POST) # A form bound to the POST data
            if form.is_valid():
                house = form.cleaned_data['house']
                house = house.upper()
                if House.objects.filter(house=house):
                    varerr = 'This House Already Exists!'
                    return render_to_response('setup/schoolhouse.html',{'form':form,'varerr':varerr,'getdetails':getdetails})
                savecon = House(house = house)
                savecon.save()
                return HttpResponseRedirect('/setup/schoolhouse/')
        else:
            form = HouseForm()
        return render_to_response('setup/schoolhouse.html',{'varuser':varuser,'form':form,'getdetails':getdetails,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')

def deletehousecode(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        getdetails = House.objects.get(id = invid)
        k = getdetails.house
        if Student.objects.filter(house = k ).count() == 0 :
            seldata = House.objects.get(id = invid)
            seldata.delete()
            return HttpResponseRedirect('/setup/schoolhouse/')
        else:
            varerr = 'Students already given this house'
            getdetails = House.objects.all().order_by('house')
            form = HouseForm()
            return render_to_response('setup/schoolhouse.html',{'form':form,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')


def department(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.setup
        if uenter is False :
            return HttpResponseRedirect('/unauthorised/')
        varerr =''
        getdetails = Department.objects.all().order_by('department')
        if request.method == 'POST':
            form = DepartmentForm(request.POST) # A form bound to the POST data
            if form.is_valid():
                department = form.cleaned_data['department']
                department = department.upper()
                if Department.objects.filter(department=department):
                    varerr = 'This Department Already Exists!'
                    return render_to_response('setup/department_and_roles.html',{'form':form,'varerr':varerr,'getdetails':getdetails})
                savecon = Department(department = department)
                savecon.save()
                return HttpResponseRedirect('/setup/departmentsandroles/')
        else:
            form = DepartmentForm()
        return render_to_response('setup/department_and_roles.html',{'form':form,'getdetails':getdetails,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')




def uploadlocalgovt(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.editregistration
        if uenter == False :
            return HttpResponseRedirect('/unauthorised/')
        varerr =''
        succ ="Select file"
        if request.method == 'POST':
            #row =""
            succ =""

            if request.FILES['input_excel']:
                input_excel=request.FILES['input_excel']
                num = []
                rows = "testing"
                book = xlrd.open_workbook(file_contents=input_excel.read())
                sheet = book.sheet_by_index(0)
                for row_no in range(0, sheet.nrows):
                    rows = sheet.row_values(row_no)
                    num.append(rows)
                    #num = raw_str.split(",")
                ncount = len(num)
                # print raw_str
                try:
                    for k in num:
                        j1 = k[0]
                        j2 = k[1]
                        savecon = LGA (state = j1,lga = j2)
                        savecon.save()
                    succ = "Record Uploaded !!!"
                    return render_to_response('setup/upload.html',{'succ':succ})
                except:
                    succ ="Uploading Error "
                return render_to_response('setup/upload.html',{'succ':succ})

            else:
                succ = "No file selected !!!"
                return render_to_response('setup/upload.html',{'succ':succ})
        else:
            return render_to_response('setup/upload.html', {'succ':succ})
    else:
        return HttpResponseRedirect('/login/')
# uploadlocal = staff_member_required(uploadlocal)






def uploadlocal(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""
        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"
            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            try:
                for k in num:
                    j1 = k[0]
                    j2 = k[1]
                    savecon = LGA (state = j1,lga = j2)
                    savecon.save()
                succ = "Record Uploaded !!!"
                return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            except:
                succ ="Uploading Error "
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})

    else:
        form = XlsInputForm()
    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadlocal = staff_member_required(uploadlocal)

def getsubject(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails =  Subject.objects.get(id = acccode)
                subjectlist = Subject.objects.all().order_by('num')
                fs = {}
                for k in subjectlist:
                    l = {k.category2:k.category2}
                    fs.update(l)
                nlist = fs.keys()
                return render_to_response('setup/getsubject.html',{'varuser':varuser,'subjectlist':nlist,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')
#######UPDATE SUBJECT BUTTON ON edit subject dialog box in setup subject******************

def editsubject(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        if request.method == 'POST':
            sub = request.POST['subject']
            gid = request.POST['hcode']
            klass = request.POST['class']
            ca = request.POST['ca']
            exam = request.POST['exam']
            cate = request.POST['subjectlist']
            if ca == "" or exam == "" or klass == "" or "" :
                return HttpResponseRedirect('/setup/subject/')
            getdetails = Subject.objects.get(id = invid)
            if Subject.objects.filter(category = klass, subject = sub).exclude(id = invid).count() == 0:
                getdetails.category2 = cate
                getdetails.save()
                SubjectScore.objects.filter(session = currse,subject = gid).update(subject = sub)
                subjectteacher.objects.filter(subject = gid).update(subject = sub)
                return HttpResponseRedirect('/setup/subject/')
            else:
                return HttpResponseRedirect('/setup/subject/')

        else:
            return HttpResponseRedirect('/setup/subject/')
    else:
        return HttpResponseRedirect('/login/')
        

def uploadaccsubgrp(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""
        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"
            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            try:
                from myproject.ruffwal.rsetup.models import tblsubgroup
                for k in num:
                    j1 = k[0]#groupcode
                    j2 = k[1]#group name
                    j3 = k[2]#subcode
                    j4 = k[3]#sub name
                    j5 = k[4]#user id
                    savecon = tblsubgroup(groupname = str(j2),groupcode = str(j1),subgroupname =j4,subgroupcode = str(j3),userid = j5)
                    savecon.save()
                succ = "Record Uploaded !!!"
                return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            except:
                succ ="Uploading Error "
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
    else:
        form = XlsInputForm()
    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadaccsubgrp = staff_member_required(uploadaccsubgrp)

def uploadacc(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""
        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"
            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            try:
                from myproject.ruffwal.rsetup.models import tblaccount,tblsubgroup
                for k in num:
                    j1 = k[0]#accname
                    j2 = k[1]#acccode
                    j3 = k[2]#datecreated
                    j4 = k[3]#lasttrandate
                    j5 = k[4]#userid
                    j6 = k[5]#accbal
                    j7 = k[6]#accstatus
                    j8 = k[7]#groupname
                    j9 = k[8]#subgroupname
                    j10 = k[9]#recreport
                    j6_as_date = datetime.date(*xlrd.xldate_as_tuple(j3, 0)[:3])
                    j17_as_date = datetime.date(*xlrd.xldate_as_tuple(j4, 0)[:3])
                    #print 'Datecreated ',j6_as_date,'Last trans date',j17_as_date
                    grc = tblsubgroup.objects.filter(groupname = j8)
                    subname = tblsubgroup.objects.filter(subgroupname = j9)
                    groupcode = ''
                    subgroupcode = ''
                    for j in grc:
                        groupcode =j.groupcode
                    for n in subname:
                        subgroupcode = n.subgroupcode

                    savecon = tblaccount(accname = j1,acccode = j2,accbal =j6,groupname = j8,groupcode = groupcode,datecreated = j6_as_date,subgroupname =j9,subgroupcode =subgroupcode,userid = j5,accstatus = j7,recreport = j10,lasttrandate = j17_as_date)
                    savecon.save()
                succ = "Record Uploaded !!!"
                return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            except:
                succ ="Uploading Error "
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
    else:
        form = XlsInputForm()
    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadacc = staff_member_required(uploadacc)

def uploadtransaction(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""
        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"
            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            #try:
            from myproject.ruffwal.rsetup.models import tblaccount,tblsubgroup
            from myproject.ruffwal.posting.models import tbltransaction
            for k in num:
                j1 = k[0]#acccode
                j2 = k[1]#transdate
                j3 = k[2]#cheque no
                j4 = k[3]#particular
                j5 = k[4]#credit
                j6 = k[5]#debit
                j7 = k[6]# balance
                j8 = k[7]#transmode
                j9 = k[8]#recdate
                j10 = k[9]#user id
                j11 = k[10]#trans id
                j2_as_date = datetime.date(*xlrd.xldate_as_tuple(j2, 0)[:3])
                #j17_as_date = datetime.date(*xlrd.xldate_as_tuple(j4, 0)[:3])
                #print 'Last trans date',j2_as_date
                grc = tblaccount.objects.get(acccode = j1)
                savecon = tbltransaction(accname = grc.accname,acccode = j1,debit =j6,credit = j5,balance = j7,transid = str(j11),transdate =j2_as_date,particulars = j4,refno = j3,groupname = grc.groupname,subname = grc.subgroupname,userid = j10,recid = j11)
                savecon.save()
            succ = "Record Uploaded !!!"
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            #except:
             #   succ ="Uploading Error "
            #return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
    else:
        form = XlsInputForm()
    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadtransaction = staff_member_required(uploadtransaction)
def uploadstudent(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""
        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"
            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            #try:
            from myproject.ruffwal.rsetup.models import tblaccount
            for k in num:

                    surname = k[0]#transdate
                    firstname = k[1]#acccode
                    othername = k[2]#cheque no
                    address = k[3]#credit
                    sex = k[4]#debit
                    j2 = k[5]#particular
                    birth_place = k[6]# balance
                    state_of_origin = k[7]#transmode
                    lga = k[8]#recdate
                    studentpicture = k[9]#user id
                    fathername = k[10]#trans id
                    fatheraddress = k[11]#trans id
                    fathernumber = k[12]#trans id
                    fatheroccupation = k[13]#trans id
                    fatheremail = k[14]#trans id
                    prev_school = k[15]#trans id
                    prev_class = k[16]#trans id
                    admitted_class = k[17]#trans id
                    admitted_arm = k[18]#
                    admitted_session = k[19]#trans id
                    fullname = k[20]#trans id
                    admissionno = k[21]#trans id
                    house = k[22]#trans id
                    dayboarding = k[23]#trans id
                    varuser = k[24]#trans id
                    subclass = k[25]#trans id
                    newsession = '2013/2014'

                    birth_date = datetime.date(*xlrd.xldate_as_tuple(j2, 0)[:3])

                    submit = Student(birth_date= birth_date,admitted_session = admitted_session,firstname = firstname,surname = surname,othername = othername,address = address,sex = sex,birth_place = birth_place,state_of_origin =state_of_origin,lga = lga,fathername =fathername,fatheraddress = fatheraddress,fathernumber = fathernumber,fatheroccupation =fatheroccupation,fatheremail = fatheremail,prev_school =prev_school,prev_class = prev_class,admitted_class = admitted_class,admitted_arm = admitted_arm,admissionno = admissionno,house = house,dayboarding = dayboarding,subclass = subclass,userid = varuser,studentpicture = studentpicture)
                    submit.save()
                    #********************************************************
                    submit1 = Student(birth_date= birth_date,admitted_session = newsession,firstname = firstname,surname = surname,othername = othername,address = address,sex = sex,birth_place = birth_place,state_of_origin =state_of_origin,lga = lga,fathername =fathername,fatheraddress = fatheraddress,fathernumber = fathernumber,fatheroccupation =fatheroccupation,fatheremail = fatheremail,prev_school =prev_school,prev_class = prev_class,admitted_class = admitted_class,admitted_arm = admitted_arm,admissionno = admissionno,house = house,dayboarding = dayboarding,subclass = subclass,userid = varuser,studentpicture =  studentpicture)
                    submit1.save()
                    fullname = str(surname) + ' ' + str(firstname) + ' '+ str(othername)
                    #used = tblaccount(groupname = "CURRENT ASSETS",groupcode = "30000",subgroupname = "RECEIVABLES",subgroupcode="30200",datecreated = datetime.datetime.today(),userid =varuser,accname = fullname.upper(),acccode = admissionno,accbal= 0,accstatus ="ACTIVE",recreport ="STUDENTS" )
                    #used.save()

            succ = "Record Uploaded !!!"
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            #except:
             #   succ ="Uploading Error "
            #return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
    else:
        form = XlsInputForm()
    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadstudent = staff_member_required(uploadstudent)

def uploadbill(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""
        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"
            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            #try:
            from myproject.bill.models import tblbill

            for k in num:
                j1 = k[0]#class
                j2 = k[1]#desc
                j3 = k[2]#bill amount
                j4 = k[3]#acc code
                j5 = k[4]#day/boarding
                j6 = k[5]#term
                j7 = k[6]# userid
                savecon = tblbill(klass = str(j1),desc = str(j2),billamount =float(j3),acccode = str(j4),dayboarding = str(j5),term = str(j6),userid = str(j7))
                savecon.save()
            succ = "Record Uploaded !!!"
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            #except:
            #   succ ="Uploading Error "
            #return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
    else:
        form = XlsInputForm()
    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadbill = staff_member_required(uploadbill)



def uploadbillname(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""
        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"
            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            #try:
            from myproject.bill.models import tblexpenses

            for k in num:
                j1 = k[0]#class

                savecon = tblexpenses(name = str(j1))
                savecon.save()
            succ = "Record Uploaded !!!"
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            #except:
            #   succ ="Uploading Error "
            #return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
    else:
        form = XlsInputForm()
    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadbillname = staff_member_required(uploadbillname)

def uploadadditionalbill(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""
        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"
            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            #try:
            from myproject.bill.models import tbladditionalbill
            for k in num:
                j1 = k[0]#session
                j2 = k[1]#name
                j3 = k[2]#klass
                j4 = k[3]#term
                j5 = k[4]#bill amount
                j6 = k[5]#desc
                j7 = k[6]#acccode
                j8 = k[7]#user id
                if Student.objects.filter(fullname = j2):
                    admno = Student.objects.get(fullname = j2,admitted_session = '2012/2013').admissionno
                    arm = Student.objects.get(fullname = j2,admitted_session = '2012/2013').admitted_arm
                else:
                    admno = 'LC/0000000'
                    arm = 'A'
                savecon = tbladditionalbill(session = str(j1),admissionno = admno,name =str(j2),klass = str(j3),arm = arm,term = str(j4),billamount = float(j5),desc = str(j6),acccode = str(j7),userid = str(j8))
                savecon.save()
            succ = "Record Uploaded !!!"
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            #except:
            #   succ ="Uploading Error "
            #return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
    else:
        form = XlsInputForm()
    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadadditionalbill = staff_member_required(uploadadditionalbill)

def uploadpostedbill(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""
        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"
            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            #try:
            from myproject.bill.models import postedbill
            for k in num:
                j1 = k[0]#session
                j2 = k[1]#klass
                j3 = k[2]#term
                j4 = k[3]#userid
                savecon = postedbill(session = str(j1),klass = str(j2),term =str(j3),userid = str(j4))
                savecon.save()
            succ = "Record Uploaded !!!"
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            #except:
            #   succ ="Uploading Error "
            #return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
    else:
        form = XlsInputForm()
    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadpostedbill = staff_member_required(uploadpostedbill)

