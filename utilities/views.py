# Create your views here.
from django.template import loader, Context,RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import  HttpResponseRedirect
from django.contrib.sessions.models import Session



from myproject.utilities.form import *
from myproject.assessment.utils import *
from myproject.utilities.capy import monthrange




from django.db.models import Max,Sum
from django.contrib.admin.views.decorators import staff_member_required
import datetime
from datetime import date
import xlrd
import xlwt
import random
import os
import locale
from myproject.settings import MEDIA_ROOT as m_root
locale.setlocale(locale.LC_ALL,'')


def allaccount(request):
    if request.method == 'POST':
        getacc = tblaccount.objects.all().order_by('acccode')
        return render_to_response('utilities/allaccount.htm',{'form': '','acc':getacc})
    else:
        return render_to_response('utilities/allaccount.htm', {'form': ''})
allaccount = staff_member_required(allaccount)

def transactionsview(request):
    if request.method == 'POST':
        succ =""
        form = dateformpl(request.POST)
        if form.is_valid():
            caldate1 = form.cleaned_data['startdate']
            caldate11 = form.cleaned_data['enddate']
            caldate2 = caldate1.split('/')
            varstart = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
            caldate22 = caldate11.split('/')
            varend = date(int(caldate22[2]),int(caldate22[0]),int(caldate22[1]))
            if varstart > varend :
                succ = "Invalid Date"
                return render_to_response('utilities/trans.htm', {'form': form,'succ':succ})

            trans = tbltransaction.objects.filter(transdate__range=(varstart,varend)).order_by('transdate','id')
            getdata = tbltransaction.objects.filter(transdate__range=(varstart,varend)).aggregate(Sum('debit'),Sum('credit'))
            debit = getdata['debit__sum']
            credit = getdata['credit__sum']
            return render_to_response('utilities/trans.htm',{'form': form,'acc':trans,'debit':locale.format("%.2f",float(debit),grouping=True),'credit':locale.format("%.2f",float(credit),grouping=True)})
        else:
            succ = 'Invaid Form'
            return render_to_response('utilities/trans.htm', {'form': form,'succ':succ})
    else:
        form = dateformpl()
        return render_to_response('utilities/trans.htm', {'form': form})
transactionsview = staff_member_required(transactionsview)



def verifyposting(rid):
    #gettrans = tbltransaction.objects.get(id = rid)
    #transid = gettrans.transid
    #transdate = gettrans.transdate
    trans = tbltransaction.objects.filter(transid = rid)
    tlist = []
    for j in trans:
        kd = {'id':j.id,'acccode':j.acccode,'accname':j.accname.title(),'debit':locale.format("%.2f",float(j.debit),grouping=True),'credit':locale.format("%.2f",float(j.credit),grouping=True),'balance':locale.format("%.2f",float(j.balance),grouping=True),'transid':j.transid,'transdate':j.transdate,'particulars':j.particulars,'refno':j.refno,'transtype':'','userid':j.userid,'authorise':j.userid}
        tlist.append(kd)
    ledger = {'trans':tlist}
    return ledger


#***********************Delete Transaction *****************************
def deletetrans(request):
    if request.method == 'POST':
        succ =""
        form = accsearch(request.POST, request.FILES)
        if form.is_valid():
            transid = form.cleaned_data['accname']
            tbltransaction.objects.filter(transid = transid).delete()
            succ = 'OPERATION SUCCESSFUL'
            return render_to_response('utilities/deletetrans.htm',{'form': form,'succ':succ})
    else:
        form = accsearch()
        return render_to_response('utilities/deletetrans.htm', {'form': form})
deletetrans = staff_member_required(deletetrans)

def deletetransbydate(request):
    if request.method == 'POST':
        j = request.POST.getlist(u'pickone')
        for p in j:
            tbltransaction.objects.filter(transid = p).delete()
        return HttpResponseRedirect('/utils/removetransaction/')
    else:
       return render_to_response('utilities/removetrans.htm', {'data': tbltransaction.objects.filter(transdate = date(2012,12,31))})
deletetransbydate = staff_member_required(deletetransbydate)



def newaccview(request):# To CHANGE old GL TO NEW WHEN MIGRATING
    succ =""
    if request.method == 'POST':
        succ =""
        form = newaccount(request.POST)
        if form.is_valid():
            oldacc = request.POST['oldacc']
            newacc = request.POST['newacc']
            acc = tblaccount.objects.get(acccode = oldacc)
            tblaccount.objects.filter(acccode = oldacc).update(acccode = newacc,groupname ='CURRENT ASSETS',subgroupname = 'TAKE-ON-STOCKS',groupcode = '30000',subgroupcode ='30700')
            tbltransaction.objects.filter(acccode = oldacc).update(acccode = newacc,groupname ='CURRENT ASSETS',subname = 'TAKE-ON-STOCKS')
            succ = "Successful !!!"
            return render_to_response('utilities/oldtonewacc.htm',{'form': form,'succ':succ})
    else:
        form = newaccount()
    return render_to_response('utilities/oldtonewacc.htm', {'form': form,'succ':succ})
newaccview = staff_member_required(newaccview)

def updateacc(request):
    succ =""
    if request.method == 'POST':
        acc = Student.objects.all()
        for k in acc:
            if tblaccount.objects.filter(acccode = k.admissionno):
                pass
            else:
                used = tblaccount(groupname = "CURRENT ASSETS",groupcode = "30000",subgroupname = "RECEIVABLES",subgroupcode="30200",datecreated = datetime.datetime.today(),userid ='FAMADE',accname = k.fullname.upper(),acccode = k.admissionno,accbal= 0,accstatus ="ACTIVE",recreport ="STUDENTS" )
                used.save()
        succ = "Successfull"
        return render_to_response('utilities/upgradeacc.htm', {'succ':succ})
    else:
          return render_to_response('utilities/upgradeacc.htm', {'succ':succ})

def temppromotion(request):# For temporary Promotion
    succ =""
    if request.method == 'POST':
        succ =""
        form = promotionform(request.POST)
        if form.is_valid():
            oldclass = request.POST['oldclass']
            newclass = request.POST['newclass']
            session = request.POST['session']
            #'studentpix/user.png'
            for p in Student.objects.filter(admitted_session = '2012/2013',admitted_class = oldclass,gone = False):
               ll = str(p.studentpicture).split('/')[1]
               n,e = str(ll).split('.')
               stpic = str(n)+'.'+str(e).lower()
               sp = os.path.join(m_root, 'studentpix/%s'%stpic)
               if os.path.exists(sp) is True:
                   pics = 'studentpix/'+stpic#p.studentpicture
               else:
                   #pics = str(p.studentpicture)
                   pics = 'studentpix/user.png'
               if Student.objects.filter(admitted_session = session,admissionno = p.admissionno):
                   Student.objects.filter(admitted_session = session,admissionno = p.admissionno).delete()
                   submit = Student(birth_date= p.birth_date,admitted_session = session,firstname = p.firstname,surname = p.surname,othername = p.othername,address = p.address,sex = p.sex,birth_place = p.birth_place,state_of_origin =p.state_of_origin,lga = p.lga,fathername =p.fathername,fatheraddress = p.fatheraddress,fathernumber = p.fathernumber,fatheroccupation =p.fatheroccupation,fatheremail = p.fatheremail,prev_school =p.prev_school,prev_class = p.prev_class,admitted_class = newclass,admitted_arm = p.admitted_arm,admissionno = p.admissionno,house = p.house,dayboarding = p.dayboarding,subclass = p.subclass,userid = p.userid,studentpicture = pics)
                   submit.save()
               else:
                  submit = Student(birth_date= p.birth_date,admitted_session = session,firstname = p.firstname,surname = p.surname,othername = p.othername,address = p.address,sex = p.sex,birth_place = p.birth_place,state_of_origin =p.state_of_origin,lga = p.lga,fathername =p.fathername,fatheraddress = p.fatheraddress,fathernumber = p.fathernumber,fatheroccupation =p.fatheroccupation,fatheremail = p.fatheremail,prev_school =p.prev_school,prev_class = p.prev_class,admitted_class = newclass,admitted_arm = p.admitted_arm,admissionno = p.admissionno,house = p.house,dayboarding = p.dayboarding,subclass = p.subclass,userid = p.userid,studentpicture = pics)
                  submit.save()
            succ = "Successful !!!"
            return render_to_response('utilities/promotion.htm',{'form': form,'succ':succ})
    else:
        form = promotionform()
    return render_to_response('utilities/promotion.htm', {'form': form,'succ':succ})
temppromotion = staff_member_required(temppromotion)

def updateassview(request):# For updating the student assessment but no more in use
    succ =""
    if request.method == 'POST':
        succ =""
        form = updateassform(request.POST)
        if form.is_valid():
            oldclass = request.POST['oldclass']
            arm = request.POST['arm']
            session = request.POST['session']
            term = 'Third'
            for p in Student.objects.filter(admitted_session = session,admitted_class = oldclass,admitted_arm = arm):
                #print 'Student :',p.admissionno,'Class',p.admitted_class,'Arm',p.admitted_arm
                if StudentAcademicRecord.objects.filter(student = p,session = session,term = term):
                    acaderec = StudentAcademicRecord.objects.get(student = p,session = session,term = term)
                    for s in SubjectScore.objects.filter(academic_rec = acaderec,klass = oldclass,session = session):
                        aa =annualaverage(p.admissionno,session,p.admitted_arm,oldclass,s.subject)
                        sp = subjectposition(session,s.subject,term,oldclass,p.admitted_arm)
                        pe = percent(session,oldclass,p.admitted_arm,p.admissionno,term)
                        cp = classposition(session,term,oldclass,p.admitted_arm)
                else:
                    pass
            succ = "Successful !!!"
            return render_to_response('utilities/ass.htm',{'form': form,'succ':succ})
    else:
        form = updateassform()
    return render_to_response('utilities/ass.htm', {'form': form,'succ':succ})
updateassview = staff_member_required(updateassview)
#**********************************creating Pin***********************************
#for encryption using $RW?AUFGHS -0-9
def encrypt(code):  
    p = str(code)
    s = ''
    for n in p: 
        if n == '0':
            j = '$'
        elif n == '1':
            j = 'R'
        elif n == '2':
            j = 'W'
        elif n == '3':
            j = '?'
        elif n == '4':
            j = 'A'
        elif n == '5':
            j = 'U'
        elif n == '6':
            j = 'F'
        elif n == '7':
            j = 'G'
        elif n == '8':
            j = 'H'
        elif n == '9':
            j = 'S'
        else:
            j = ''
        s = str(s) + str(j)
    return s
# for decryption
def decrypt(code):     
    p = str(code)         
    s = ''
    for n in p:         
        if n == '$':          
            j = '0'
        elif n == 'R':
            j = '1'
        elif n == 'W':
            j = '2'
        elif n == '?':
            j = '3'
        elif n == 'A':
            j = '4'
        elif n == 'U':
            j = '5'
        elif n == 'F':
            j = '6'
        elif n == 'G':
            j = '7'
        elif n == 'H':
            j = '8'
        elif n == 'S':
            j = '9'
        else:
            j = ''
        s = str(s) + str(j)
    return s
#**********************************************************
#for encryption using .@#!+,()*%  -0-9
def encrypt1(code):    
    p = str(code)
    s = ''
    for n in p:
        if n == '0':               
            j = '.'
        elif n == '1':
            j = '@'
        elif n == '2':
            j = '#'
        elif n == '3':
            j = '!'
        elif n == '4':
            j = '+'
        elif n == '5':
            j = ','
        elif n == '6':
            j = '('
        elif n == '7':
            j = ')'
        elif n == '8':
            j = '*'
        elif n == '9':
            j = '%'
        else:
            j = ''
        s = str(s) + str(j)
    return s

# for decryption  .@#!+,()*%
def decrypt1(code):
    p = str(code)
    s = ''
    for n in p:
        if n == '.':
            j = '0'
        elif n == '@':
            j = '1'
        elif n == '#':
            j = '2'
        elif n == '!':
            j = '3'
        elif n == '+':
            j = '4'
        elif n == ',':
            j = '5'
        elif n == '(':
            j = '6'
        elif n == ')':
            j = '7'
        elif n == '*':
            j = '8'
        elif n == '%':
            j = '9'
        else:
            j = ''
        s = str(s) + str(j)
    return s

#getting random number
def getrandom():
    uid = ''
    for m in range(25):
        k = random.randint(1,999999)
        uid += str(k)
    return uid



#to generate pin
def generatepin(request):
    succ =""
    #response = HttpResponse(mimetype="application/ms-excel")
    #response['Content-Disposition'] = 'attachment; filename=pin.xls'
    #wb = xlwt.Workbook()
    #ws = wb.add_sheet('pin')
    comp = tblcompanyinfo.objects.all()
    logo = ''
    address = ''
    compname = ''
    for k in comp:
        logo = k.picture
        address = k.address
        compname = k.name
    note = "This Page will create a pin for our yearly maintenance fees"
    head = "Generate Pin"
    rlist = []
    rlist1 = tblpin.objects.all()
    for t in rlist1:
        ddic ={'ydate':t.ydate,'pin':t.pin,'used':decrypt(t.pin)}
        rlist.append(ddic)
    if request.method == 'POST':
        if tblpin.objects.all().count() == 0:
            pass
        else:
            succ = "Pin Already Generated !!!"
            return render_to_response('upload/preparedb.htm',{'form': '','succ':succ,'note':note,'head':head,'data':rlist,'comp':compname,'address':address,'logo':logo})
        d = 2016
        r = 0
        for m in range(200):
            d += 1
            k = random.randint(0,9)
            y = random.randint(0,9)
            x = random.randint(0,9)
            z = random.randint(0,9)
            a = random.randint(0,9)
            b = random.randint(0,9)
            c = random.randint(0,9)
            e = random.randint(0,9)
            pin =  str(k) + str(y) + str(x) + str(z)+ str(a)+ str(b)+ str(c)+ str(e)
            used = encrypt(pin)
            ydate = date(d,3,15)
            tsave = tblpin(ydate =ydate,pin = used,used = '0')
            tsave.save()
        return HttpResponseRedirect('/utils/generatepin/')
        #ws.write(r, 0, dd)
        #ws.write(r, 1, used)
        #ws.write(r, 2, pin)
        #r += 1
        #wb.save(response)
        #return response
        #succ = "Operation Successful !!!"
        #return render_to_response('upload/preparedb.htm',{'form': '','succ':succ,'note':note,'head':head,'data':rlist})
    else:
        return render_to_response('upload/preparedb.htm', {'form': '','succ':succ,'note':note,'head':head,'data':rlist,'comp':compname,'address':address,'logo':logo})
generatepin = staff_member_required(generatepin)

def preparedb(request):
    succ =""
    note = "This Page is to prepare our database for fresh deployment"
    head = "Prepare DB"
    if request.method == 'POST':
        tbltransaction.objects.all().delete()
        tbltemp.objects.all().delete()
        tbltempreceipt.objects.all().delete()
        tbltemppayment.objects.all().delete()
        tbljournal.objects.all().delete()
        tblstandard.objects.all().delete()
        #end of postings********************
        staffonloan.objects.all().delete()
        receivables.objects.all().delete()
        payables.objects.all().delete()
        tblaccount.objects.all().exclude(acccode = "30701").exclude(acccode = "30301").exclude(acccode = "40201").exclude(groupcode = "60000").exclude(groupcode = "10000",subgroupcode ='10100').exclude(groupcode = "20000").exclude(groupcode = "80000",subgroupcode ='80400').exclude(groupcode = "40000",subgroupcode ='40500').exclude(groupcode = "80000",subgroupcode ='81000').exclude(groupcode = "80000",subgroupcode ='80300').delete()
        #tblaccountoff.objects.all().delete()
        #tblministock.objects.all().delete()
        #tblstock.objects.all().delete()
        ##************end of setup**************************
        #tblasset.objects.all().delete()#for asset table
        #tblassetdepartment.objects.all().delete()
        ##***************end if assets
        #tblbudget.objects.all().delete()
        ##***********end of budget **************
        #tbltemp1.objects.all().delete()
        #tbltempreceipt1.objects.all().delete()
        #tbltemppayment1.objects.all().delete()
        #tbljournal1.objects.all().delete()
        #tblstandard1.objects.all().delete()
        #tbltransactiontemp.objects.all().delete()
        ##******************end of new year*************************
        #upresentedtrans.objects.all().delete()
        #upresentedtranstemp.objects.all().delete()
        #uncreditedtrans.objects.all().delete()
        #upcreditedtranstemp.objects.all().delete()
        ##*****************end of reconciliation **********
        #tblstocktransaction.objects.all().delete()
        #tblstocktemp.objects.all().delete()
        #tblstocktempout.objects.all().delete()
        #**************end of stock**************************
        #******************************end of new year **********
        userprofile.objects.all().delete()
        succ = "Operation Successful !!!"
        return render_to_response('upload/preparedb.htm',{'form': '','succ':succ,'note':note,'head':head})
    else:
        return render_to_response('upload/preparedb.htm', {'form': '','succ':succ,'note':note,'head':head})
preparedb = staff_member_required(preparedb)

#********************to get transaction ID **********************
def gettransid(varyear):# here uid represent the auto_number of the user that is posting and varyear is the calender enddate.year
    if tbltransaction.objects.filter(transdate__year = varyear).count() == 0 :
        varrid = 1
    else:
        varrid1 = tbltransaction.objects.filter(transdate__year = varyear).aggregate(Max('recid'))
        varrid = varrid1['recid__max']
        varrid = int(varrid)
    return varrid

def gettransidtemp(varyear,uid):# here uid represent the auto_number of the user that is posting and varyear is the calender enddate.year
    if tbltransactiontemp.objects.filter(transdate__year = varyear).count() == 0 :
        varrid = 1
    else:
        varrid1 = tbltransactiontemp.objects.filter(transdate__year = varyear).aggregate(Max('recid'))
        varrid = varrid1['recid__max']
        varrid  += 1
    vyear =  str(varyear)
    vayear = vyear[2]+ vyear[3]
    vartransid = str(vayear)+str(uid)+ str(varrid) #trans id
    varrecid = varrid
    k = {'vartransid':vartransid,'varrecid':varrecid}
    return k
