# Create your views here.
from django.shortcuts import render_to_response
from django.shortcuts import render_to_response, get_object_or_404
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from django.template import Template, Context, RequestContext
from django.views.decorators.csrf import *
from django.db.models import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.serializers.json import json
from myproject.bill.forms import *
from myproject.bill.models import *
from myproject.student.models import *
# from myproject.ruffwal.rsetup.models import *
#from myproject.ruffwal.stock.models import *
from myproject.sysadmin.forms import calendar_form
from django.db.models import Max,Sum
from myproject.assessment.utils import *
import locale
locale.setlocale(locale.LC_ALL,'')
import xlwt
#currse = currentsession.objects.get(id = 1)
def sessi():
    if billsession.objects.all().count() == 0:
        currse = currentsession.objects.get(id = 1)
    else:
        currse = billsession.objects.get(id = 1)
    return currse

def wel(request):
    if  "userid" in request.session:
        varuser=request.session['userid']
        return render_to_response('bill/success1.html',{'varuser':varuser})
    else:
        return HttpResponseRedirect('/login/')
def well(request):
    if  "userid" in request.session:
        return render_to_response('bill/success1.html')
    else:
        return HttpResponseRedirect('/login/')

def addexpensesname(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.expensedecription
        if uenter is False :
            return HttpResponseRedirect('/unauthorised/')
        varerr =''
        getdetails =''
        if request.method == 'POST':
            form = expensesForm(request.POST) # A form bound to the POST data
            if form.is_valid():
                expenses = form.cleaned_data['expenses']
                na = expenses.upper()
                if tblexpenses.objects.filter(name=na):
                    varerr = 'Bill Already Exists!'
                    getdetails = tblexpenses.objects.all()
                    return render_to_response('bill/expenses.html',{'form':form,'varerr':varerr,'getdetails':getdetails,'varuser':varuser})
                savecon = tblexpenses(name = na)
                savecon.save()
                return HttpResponseRedirect('/bill/billname/')
        else:
            form = expensesForm()
            getdetails = tblexpenses.objects.all()

        return render_to_response('bill/expenses.html',{'form':form,'varerr':varerr,'getdetails':getdetails,'varuser':varuser})
    else:
        return HttpResponseRedirect('/login/')

def deleteexpensesname(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.expensedecription
        if uenter is False :
            return HttpResponseRedirect('/unauthorised/')
        varerr =''
        getdetails = tblexpenses.objects.get(id = vid)
        getdetails.delete()
        return HttpResponseRedirect('/bill/billname/')
    else:
        return HttpResponseRedirect('/login/')

def billsetup(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.billsetup
        if uenter is False :
            return HttpResponseRedirect('/unauthorised/')
        varerr =''
        getdetails =''
        if request.method == 'POST':
            form = billForm(request.POST) # A form bound to the POST data
            if form.is_valid():
                klass = form.cleaned_data['klass']
                desc = form.cleaned_data['desc']
                billamount = form.cleaned_data['billamount']
                acccode = form.cleaned_data['acccode']
                dayboarding = form.cleaned_data['dayboarding']
                term = form.cleaned_data['term']
                try:
                    from myproject.ruffwal.rsetup.models import tblaccount
                    if tblaccount.objects.filter(acccode = acccode):
                        pass
                    else:
                        varerr = 'GL Account Code Not In Existence!'
                        #getdetails = tblexpenses.objects.all()
                        return render_to_response('bill/bill.html',{'form':form,'varerr':varerr})
                except :
                    pass

                if tblbill.objects.filter(klass=klass,dayboarding = dayboarding,desc = desc,term = term):
                    varerr = 'Bill Already Exists!'
                    #getdetails = tblexpenses.objects.all()
                    return render_to_response('bill/bill.html',{'form':form,'varerr':varerr})
                savecon = tblbill(klass = klass,desc = desc,billamount = billamount,acccode = acccode,dayboarding = dayboarding,term = term, userid = varuser)
                savecon.save()
                return HttpResponseRedirect('/bill/billsetup/')
        else:
            form = billForm()
        return render_to_response('bill/bill.html',{'form':form,'varerr':varerr,'varuser':varuser})
    else:
        return HttpResponseRedirect('/login/')

def billsetupajax(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                varerr = acccode
                klass,term,dayboarding = acccode.split(':')
                data = tblbill.objects.filter(klass = klass,term = term,dayboarding = dayboarding)
                return render_to_response('bill/billajax.html',{'data':data})
            else:
                gdata = ""
                return render_to_response('bill/billajax.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('bill/billajax.html',{'gdata':gdata})

def deletebillajax(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.billsetup
        if uenter is False :
            return HttpResponseRedirect('/unauthorised/')
        varerr =''
        getdetails = tblbill.objects.get(id = vid)
        getdetails.delete()
        return HttpResponseRedirect('/bill/billsetup/')
    else:
        return HttpResponseRedirect('/login/')


def additionalbill(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.additionalexpenses
        if uenter is False :
            return HttpResponseRedirect('/unauthorised/')
        varerr =''
        getdetails =''
        if request.method == 'POST':
            form = additionalbillform(request.POST) # A form bound to the POST data
            if form.is_valid():
                session = form.cleaned_data['session']
                admissionno = form.cleaned_data['admissionno']
                name = form.cleaned_data['name']
                arm = form.cleaned_data['arm']
                term = form.cleaned_data['term']
                billamount = form.cleaned_data['billamount']
                desc = form.cleaned_data['desc']
                acccode = form.cleaned_data['acccode']
                klass = form.cleaned_data['klass']
                try:
                    from myproject.ruffwal.rsetup.models import tblaccount
                    if tblaccount.objects.filter(acccode = acccode):
                        pass
                    else:
                        varerr = 'GL Account Code Not In Existence!'
                        #getdetails = tblexpenses.objects.all()
                        form = additionalbillform()
                        return render_to_response('bill/addbill.html',{'form':form,'varerr':varerr})
                except :
                    pass
                if tbladditionalbill.objects.filter(klass=klass,desc = desc,term = term,session = session,admissionno = admissionno):
                    varerr = '%s Already Exists For This Student !'%desc
                    #getdetails = tblexpenses.objects.all()
                    return render_to_response('bill/addbill.html',{'form':form,'varerr':varerr})
                savecon = tbladditionalbill(klass = klass,session = session,admissionno = admissionno,name = name,arm = arm,term = term,billamount = billamount, desc = desc,acccode = acccode,userid = varuser)
                savecon.save()
                return HttpResponseRedirect('/bill/additionalbill/')
        else:
            form = additionalbillform()
        return render_to_response('bill/addbill.html',{'form':form,'varerr':varerr,'varuser':varuser})
    else:
        return HttpResponseRedirect('/login/')

def json_view(func):
    def wrap(req, *args, **kwargs):
        resp = func(req, *args, **kwargs)
        if isinstance(resp, HttpResponse):
            return resp
        return HttpResponse(json.dumps(resp), mimetype="application/json")

    return wrap

@json_view
def autocomplete(request):
    term = request.GET.get('term').upper()
    #p =  request.GET.get('query')
    #print p
    qset = Student.objects.filter(fullname__contains=term,admitted_session = sessi,gone = False)[:10]

    suggestions = []
    for i in qset:
        suggestions.append({'label': '%s :%s :%s :%s ' % (i.admissionno, i.fullname,i.admitted_class,i.admitted_arm), 'admno': i.admissionno,'name':i.fullname,'klass':i.admitted_class,'arm':i.admitted_arm})
    return suggestions

@json_view
def autocompletename(request):
    term = request.GET.get('term')
    p =  request.GET.get('query')
    #print term
    qset = Student.objects.filter(name__contains=term,admitted_session = sessi,gone = False)[:10]
    suggestions = []
    for i in qset:
        suggestions.append({'label': '%s :%s :%s :%s ' % (i.admissionno, i.fullname,i.admitted_class,i.admitted_arm), 'admno': i.admissionno,'name':i.fullname,'klass':i.admitted_class,'arm':i.admitted_arm})
    return suggestions



def billaddsetupajax(request):
    if "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                # print acccode
                admno,session,term = acccode.split(':')
                data = tbladditionalbill.objects.filter(admissionno = admno,session = session,term = term)
                return render_to_response('bill/addbillajax.html',{'data':data, 'varerr':acccode})
            else:
                gdata = ""
                return render_to_response('bill/addbillajax.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('bill/addbillajax.html',{'gdata':gdata})


def deleteaddbillajax(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.additionalexpenses
        if uenter is False :
            return HttpResponseRedirect('/unauthorised/')
        varerr =''
        getdetails = tbladditionalbill.objects.get(id = vid)
        getdetails.delete()
        return HttpResponseRedirect('/bill/additionalbill/')
    else:
        return HttpResponseRedirect('/login/')


"""def printbill(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.printbill
        if uenter is False :
            return HttpResponseRedirect('/unauthorised/')
        varerr =''
        getdetails =''
        school = get_object_or_404(School, pk=1)
        if request.method == 'POST':
            form = printbillform(request.POST) # A form bound to the POST data
            if form.is_valid():
                session = form.cleaned_data['session']
                name = form.cleaned_data['name']
                term = form.cleaned_data['term']
                klass = form.cleaned_data['klass']
                studata = ''
                bill_list = []
                if form.cleaned_data['excelfile']:
                    studata = Student.objects.filter(admitted_class = klass,admitted_session = session,gone = False).order_by('admissionno')
                else:
          #          studata = Student.objects.filter(admitted_class = klass,admitted_session = session,fullname = name,gone = False).order_by('admissionno')
                    studata = Student.objects.get(admitted_class = klass,admitted_session = session,fullname = name,gone = False).order_by('admissionno')
                varrid2 = 0
                getaddbill = ''
                for st in studata:
                   billlist = []
                   if tblbill.objects.filter(klass = klass,term = term,dayboarding = st.dayboarding).count() == 0:
                       varrid = 0
                   else:
                       getbill = tblbill.objects.filter(klass = klass,term = term,dayboarding = st.dayboarding)
                       varrid1 = tblbill.objects.filter(klass = klass,term = term,dayboarding = st.dayboarding).aggregate(Sum('billamount'))
                       varrid = varrid1['billamount__sum']
                       for j in getbill:
                            billdic = {'desc':j.desc,'billamount':locale.format("%.2f",j.billamount,grouping=True) }
                            #print billdic
                            billlist.append(billdic)
                   if tbladditionalbill.objects.filter(session = session,admissionno = st.admissionno,klass = klass,term = term).count() == 0:
                       varrid2 = 0
                       getaddbill = ''
                   else:
                      getaddbill = tbladditionalbill.objects.filter(session = session,admissionno = st.admissionno,klass = klass,term = term)
                      varrid11 = tbladditionalbill.objects.filter(session = session,admissionno = st.admissionno,klass = klass,term = term).aggregate(Sum('billamount'))
                      varrid2 = varrid11['billamount__sum']
                      for h in getaddbill:
                          billdic = {'desc':h.desc,'billamount':locale.format("%.2f",h.billamount,grouping=True)}
                          billlist.append(billdic)
                   #print 'additional bill',varrid2
                   varrid = varrid + varrid2
                   billdic = {'student':st,'bill':billlist,'totalbill':locale.format("%.2f",varrid,grouping=True)}
                   bill_list.append(billdic)"""


def printbill(request):
    if 'userid' in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.printbill
        if uenter is False:
            return HttpResponseRedirect('/unauthorised/')
        varerr = ''
        getdetails = ''
        school = get_object_or_404(School, pk = 1)
        if request.method == 'POST':
            form = printbillform(request.POST)
            if form.is_valid():
                session = form.cleaned_data['session']
                name = form.cleaned_data['name']
                term = form.cleaned_data['term']
                klass = form.cleaned_data['klass']
                studata = ''
                bill_list = []
                if form.cleaned_data['excelfile']:
                    studata = Student.objects.filter(admitted_class = klass, admitted_session = session, gone = False).order_by('admissionno')
                else:
                    studata = Student.objects.filter(admitted_class = klass, admitted_session = session, fullname = name, gone = False).order_by('admissionno')
                varrid2 = 0
                getaddbill = ''
                for st in studata:
                    billlist = []
                    if tblbill.objects.filter(klass = klass, term = term, dayboarding = st.dayboarding).count() == 0:
                        varrid = 0
                    else:
                        getbill = tblbill.objects.filter(klass = klass, term = term, dayboarding = st.dayboarding)
                        varrid1 = tblbill.objects.filter(klass = klass, term = term, dayboarding = st.dayboarding).aggregate(Sum('billamount'))
                        varrid = varrid1['billamount__sum']
                        for j in getbill:
                            billdic = {
                                'desc': j.desc,
                                'billamount': locale.format('%.2f', j.billamount, grouping = True) }
                            billlist.append(billdic)

                    if tbladditionalbill.objects.filter(session = session, admissionno = st.admissionno, klass = klass, term = term).count() == 0:
                        varrid2 = 0
                        getaddbill = ''
                    else:
                        getaddbill = tbladditionalbill.objects.filter(session = session, admissionno = st.admissionno, klass = klass, term = term)
                        varrid11 = tbladditionalbill.objects.filter(session = session, admissionno = st.admissionno, klass = klass, term = term).aggregate(Sum('billamount'))
                        varrid2 = varrid11['billamount__sum']
                        for h in getaddbill:
                            billdic = {
                                'desc': h.desc,
                                'billamount': locale.format('%.2f', h.billamount, grouping = True) }
                            billlist.append(billdic)

                    varrid = varrid + varrid2
                    billdic = {
                        'student': st,
                        'bill': billlist,
                        'totalbill': locale.format('%.2f', varrid, grouping = True) }
                    bill_list.append(billdic)
                if form.cleaned_data['pdffile']:
                    template ='bill/billreportpdf.html'
                    context ={'varerr':varerr,'bill_list':bill_list,'school':school,'session':session,'term':term,'klass':klass}
                    return render_to_pdf(template, context)
                else:
                    return render_to_response('bill/billreport.html',{'varerr':varerr,'bill_list':bill_list,'school':school,'session':session,'term':term,'klass':klass})
        else:
            form = printbillform()
        return render_to_response('bill/printbill.html',{'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')



def getstuinfoajax(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                # print acccode
                session,klass = acccode.split(':')
                kk = []
                data = Student.objects.filter(admitted_class = klass,admitted_session = session,gone = False).order_by('fullname')
                for p in data:
                    jn = p.fullname
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

def printbillschdule(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.billschedule
        if uenter == False :
            return HttpResponseRedirect('/unauthorised/')
        varerr =''
        getdetails =''
        school = get_object_or_404(School, pk=1)
        if request.method == 'POST':
            form = billscheduleform(request.POST) # A form bound to the POST data
            if form.is_valid():
                session = form.cleaned_data['session']
                term = form.cleaned_data['term']
                klass = form.cleaned_data['klass']
                adddic ={}
                billdic = {}
                if tbladditionalbill.objects.filter(session = session,klass = klass,term = term).count()== 0:
                    addbill = []
                else:
                    addbill = tbladditionalbill.objects.filter(session = session,klass = klass,term = term)
                    for n in addbill:
                        j = n.desc
                        jdic = {j:j}
                        adddic.update(jdic)
                adlist = adddic.keys()
                #print 'Additional bill :',adlist
                if  tblbill.objects.filter(klass = klass,term = term).count()== 0:
                    rbill =''
                else:
                    getbill = tblbill.objects.filter(klass = klass,term = term)
                    for b in getbill:
                        f = b.desc
                        bdic = {f:f}
                        billdic.update(bdic)
                blist =billdic.keys()
                #print 'Bill for class :',blist
                #print 'The Additional Bill :',adlist
                for r in adlist:
                    blist.append(r)
                #print 'The Main Bill : ',blist
                bill_list =[]
                studata = Student.objects.filter(admitted_class = klass,admitted_session = session,gone = False).order_by('admissionno')
                for st in studata:
                    billlist = []
                    addbilllist = []
                    totbill = 0
                    for b in blist:
                        if tblbill.objects.filter(klass = klass,term = term,dayboarding = st.dayboarding,desc = b):
                            amt = tblbill.objects.get(klass = klass,term = term,dayboarding = st.dayboarding,desc = b).billamount
                            billdic = {'desc':b,b:amt}
                            billlist.append(billdic)
                        else:
                            if tbladditionalbill.objects.filter(session = session,admissionno = st.admissionno,klass = klass,term = term,desc = b):
                                amt = tbladditionalbill.objects.get(session = session,admissionno = st.admissionno,klass = klass,term = term,desc = b).billamount
                                billdic = {'desc':b,b:amt}
                                billlist.append(billdic)
                            else:
                                amt = 0
                                billdic = {'desc':b,b:amt}
                                billlist.append(billdic)
                        totbill += amt
                    #**********************************************************************
                    billdic = {'student':st,'bill':billlist,'addbill':addbilllist,'totalbill':totbill}
                    bill_list.append(billdic)


                response = HttpResponse(mimetype="application/ms-excel")
                response['Content-Disposition'] = 'attachment; filename=billschedule.xls'
                wb = xlwt.Workbook()
                ws = wb.add_sheet('billschedule')
                ws.write(0, 1, school.name)
                ws.write(1, 1, school.address)
                ws.write(2, 1, '%s %s Term Student Bill Schedule for %s Session' %(klass,term, session) )
                k = 4
                v = 3
                ws.write(4, 0, 'S/N')
                ws.write(4, 1, 'Student Name')
                ws.write(4, 2, 'Admission Number')
                for bl in blist:
                    ws.write(k, v,bl)
                    v+=1
                ws.write(k, v, 'Total Bill')
                k+=1
                for c,m in enumerate(bill_list):
                    c += 1
                    ws.write(k, 0, c)
                    ws.write(k, 1, m['student'].fullname)
                    ws.write(k, 2, m['student'].admissionno)
                    v = 3
                    for a in m['bill']:
                        aa = a['desc']
                        jd = a[aa]
                        ws.write(k, v, locale.format("%.2f",jd,grouping=True))
                        v += 1
                    ws.write(k, v,locale.format("%.2f",m['totalbill'],grouping=True))
                    k += 1
                wb.save(response)
                return response
                #return render_to_response('bill/billschedule.html',{'form':form,'varerr':varerr,'bill_list':bill_list,'school':school,'session':session,'term':term,'klass':klass,'blist':blist,'adlist':adlist})
        else:
            form = billscheduleform()
        return render_to_response('bill/billschedule.html',{'form':form,'varerr':varerr,'varuser':varuser})
    else:
        return HttpResponseRedirect('/login/')
        
@json_view
def autocompletenameacc(request):
    term = request.GET.get('term').upper()
    p =  request.GET.get('query')
    # term=term.upper()
    #print term
    suggestions = []
    try:
        from myproject.ruffwal.rsetup.models import tblaccount
        getinc = tblaccount.objects.filter(groupcode = '70000',accname__contains=term)[:10]
        getexp = tblaccount.objects.filter(groupcode = '80000',subgroupcode = '81000')
        for i in getinc:
            suggestions.append({'label': '%s :%s' % (i.accname, i.acccode), 'accname': i.accname,'acccode':i.acccode})
        for i in getexp:
            suggestions.append({'label': '%s :%s' % (i.accname, i.acccode), 'accname': i.accname,'acccode':i.acccode})
    except :
        qset = []
        for i in qset:
            suggestions.append({'label': '%s :%s :%s :%s ' % (i.admissionno, i.fullname,i.admitted_class,i.admitted_arm), 'admno': i.admissionno,'name':i.fullname,'klass':i.admitted_class,'arm':i.admitted_arm})
    return suggestions

def printoldbill(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.printbill
        if uenter is False :
            return HttpResponseRedirect('/unauthorised/')
        varerr =''
        getdetails =''
        stuname = ''
        school = get_object_or_404(School, pk=1)
        if request.method == 'POST':
            form = printbillform(request.POST) # A form bound to the POST data
            if form.is_valid():
                session = form.cleaned_data['session']
                name = form.cleaned_data['name']
                term = form.cleaned_data['term']
                klass = form.cleaned_data['klass']
                getbill = ''
                varrid = 0
                admno = ''
                studata = Student.objects.filter(admitted_class = klass,admitted_session = session,fullname = name).order_by('admissionno')
                for st in studata:
                    admno = st.admissionno
                    stuname = st.fullname
                if oldbill.objects.filter(klass = klass,term = term,admissionno = admno,session = session).count() == 0:
                    varrid = 0
                else:
                    getbill = oldbill.objects.filter(klass = klass,term = term,admissionno = admno,session = session)
                    varrid1 = oldbill.objects.filter(klass = klass,term = term,admissionno = admno,session = session).aggregate(Sum('billamount'))
                    varrid = varrid1['billamount__sum']
                return render_to_response('bill/printoldbill.html',{'form':form,'varerr':varerr,'school':school,'session':session,'term':term,'klass':klass,'bill':getbill,'admno':admno,'stuname':stuname,'totalbill':locale.format("%.2f",varrid,grouping=True)})
        else:
            form = printbillform()
        return render_to_response('bill/printoldbill.html',{'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')

def genbill(request):
    ll = tblbill.objects.all().order_by('id')
    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=bill.xls'
    wb = xlwt.Workbook()
    ws = wb.add_sheet('getbill')
    k = 0
    for jd in ll:
        ws.write(k, 0, jd.klass)
        ws.write(k, 1, jd.desc)
        ws.write(k, 2, jd.billamount)
        ws.write(k, 3, jd.acccode)
        ws.write(k, 4, jd.dayboarding)
        ws.write(k, 5, jd.term)
        ws.write(k, 6, jd.userid)
        k += 1
    wb.save(response)
    return response

#**************Updating The School Calendar ****************************************
def bill_calendar_update(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.billsetup
        if uenter is False :
            return HttpResponseRedirect('/unauthorised/')
        varerr = ""
        succ =""
        if request.method == 'POST':
            succ =""
            form = calendar_form(request.POST)
            if form.is_valid():
                session = request.POST['session']
                sessionnew = request.POST['sessionnew']
                x,y = str(session).split('/')
                k = int(x) + 1
                n = int(y) + 1
                newsession = str(k)+'/'+str(n)
                if billsession.objects.all().count() == 0:
                    sa = billsession(session = newsession)
                    sa.save()
                else:
                    billsession.objects.all().update(session = newsession)
                succ = "Successful !!!"
                return render_to_response('bill/promotion1.htm',{'form': form,'succ':succ})
        else:
            form = calendar_form()
        return render_to_response('bill/promotion1.htm', {'form': form,'succ':succ,'varuser':varuser})
    else:
        return HttpResponseRedirect('/login/')

#*****************function to repoint liabiliies account to Income Account
def repoint_account(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.billsetup
        if uenter is False :
            return HttpResponseRedirect('/unauthorised/')
        varerr = ""
        succ ="Operation Successful"
        for h in tblbill.objects.all():
            acccode = h.acccode
            acc = tblaccount.objects.get(acccode = acccode)#,accname__contains=term
            accname = acc.accname
            #print 'Code ',acccode,'Name',accname
            rid = h.id
            if acc.groupcode == '70000' or acc.groupcode == '80000':
                pass
            else:
                if accname == 'DISCOUNT-ALLOWED' or accname == 'DISCOUNT ALLOWED':
                   tblbill.objects.filter(id = rid).update(acccode = '81001')
                else:
                   #print 'Bill Account Name ',str(accname),'Account Code',acccode
                   if tblaccount.objects.filter(accname = accname,groupcode = '70000',subgroupcode = '70100'):
                      nacc = tblaccount.objects.get(accname = accname,groupcode = '70000',subgroupcode = '70100')
                      tblbill.objects.filter(id = rid).update(acccode = nacc.acccode)
                   else:
                       pass

        #****************treating additional bill *******
        for h in tbladditionalbill.objects.all():
            acccode = h.acccode
            if tblaccount.objects.filter(acccode = acccode):
                acc = tblaccount.objects.get(acccode = acccode)#,accname__contains=term
                accname = acc.accname
                rid = h.id
                if acc.groupcode == '70000' or acc.groupcode == '80000':
                    pass
                else:
                    if accname == 'DISCOUNT-ALLOWED' or accname == 'DISCOUNT ALLOWED':
                       tbladditionalbill.objects.filter(id = rid).update(acccode = '81001')
                    else:
                       if tblaccount.objects.filter(accname = accname,groupcode = '70000',subgroupcode = '70100'):
                          nacc = tblaccount.objects.get(accname = accname,groupcode = '70000',subgroupcode = '70100')
                          tbladditionalbill.objects.filter(id = rid).update(acccode = nacc.acccode)
                       else:
                           pass
            else:
                pass

        return render_to_response('bill/promotion1.htm', {'form': '','succ':succ})
    else:
        return HttpResponseRedirect('/login/')

