from myproject.student.models import *
from myproject.bill.models import *
import locale
from django.db.models import Max,Sum

import random

def getrandom(k):
    u = ''
    for m in range(1):
        k = random.randint(1,k)
        u += str(k)
    return u


def printbill(admno,session,term):
    bill_list = []
    studata = Student.objects.get(admitted_session = session, admissionno = admno, gone = False)
    varrid2 = 0
    getaddbill = ''
    billlist = []
    klass = studata.admitted_class
    st=studata.dayboarding

    if tblbill.objects.filter(klass = klass, term = term, dayboarding = st).count() == 0:
        varrid = 0
    else:
        getbill = tblbill.objects.filter(klass = klass, term = term, dayboarding = st)
        varrid1 = tblbill.objects.filter(klass = klass, term = term, dayboarding = st).aggregate(Sum('billamount'))
        varrid1 = tblbill.objects.filter(klass = klass, term = term, dayboarding = st).aggregate(Sum('billamount'))
        varrid = varrid1['billamount__sum']
        for j in getbill:
            billdic = {'desc': j.desc,'billamount': j.billamount}#  locale.format('%.2f', j.billamount, grouping = True) }
            billlist.append(billdic)

    if tbladditionalbill.objects.filter(session = session, admissionno = admno, klass = klass, term = term).count() == 0:
        varrid2 = 0
        getaddbill = ''
    else:
        getaddbill = tbladditionalbill.objects.filter(session = session, admissionno = admno, klass = klass, term = term)
        varrid11 = tbladditionalbill.objects.filter(session = session, admissionno = admno, klass = klass, term = term).aggregate(Sum('billamount'))
        varrid2 = varrid11['billamount__sum']
        for h in getaddbill:
            billdic = {
                'desc': h.desc,
                'billamount': h.billamount }#  locale.format('%.2f', h.billamount, grouping = True) }
            billlist.append(billdic)

    varrid = varrid + varrid2

    billdic = {
        'student': st,
        'bill': billlist,
        'totalbill': varrid } #  locale.format('%.2f', varrid, grouping = True) }
    bill_list.append(billdic)

    #return bill_list
    return locale.format('%.0f', varrid)



