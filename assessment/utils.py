import os
from xlwt import Workbook, easyxf
from xhtml2pdf import pisa
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.utils.html import escape
from django.template import Template, Context, RequestContext
from myproject.academics.models import *
from myproject.assessment.getordinal import *
from django.db.models import Max,Sum

try:
    import cStringIO as StringIO
except:
    import StringIO

class UnsupportedMediaPathException(Exception): pass

def fetch_resources2(uri):
    """
    Callback to allow xhtml2pdf/reportlab to retrieve Images,Stylesheets, etc.
    `uri` is the href attribute from the html link element.
    `rel` gives a relative path, but it's not used here.

    """
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT,
            uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT,
            uri.replace(settings.STATIC_URL, ""))
    else:
        # if relative path is used tries to prefix path with static root
        # if this does not yield a file, tries prefixing with media root
        # if this fails too raise exception
        path = os.path.join(settings.STATIC_ROOT,
            uri.replace(settings.STATIC_URL, ""))

        if not os.path.isfile(path):
            path = os.path.join(settings.MEDIA_ROOT,
                uri.replace(settings.MEDIA_URL, ""))

            if not os.path.isfile(path):
                raise UnsupportedMediaPathException(
                    'media urls must start with %s or %s' % (
                        settings.MEDIA_ROOT, settings.STATIC_ROOT))
    return path

def fetch_resources(uri,rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path

#def dm_monthly(request, year, month):
   # html  = render_to_string('reports/dmmonthly.html', { 'pagesize' : 'A4', }, context_instance=RequestContext(request))
   # result = StringIO.StringIO()
    #pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), dest=result, link_callback=fetch_resources )
    #if not pdf.err:
     #   return HttpResponse(result.getvalue(), mimetype='application/pdf')
    #return HttpResponse('Gremlins ate your pdf! %s' % cgi.escape(html))

def count(Pin):
    count = tblexpress.objects.get(pin = Pin)
    vcount = count.count
    return vcount


def render_to_pdf(template_src, context_dict):
    """Function to render html template into a pdf file"""
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO()
    #
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")),
        dest=result,
        encoding='UTF-8',
        link_callback=fetch_resources)
    if not pdf.err:
        response = HttpResponse(result.getvalue(),
            mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=report.pdf'
        return response

    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

def render_to_xls(context_dict):
    """Function to output data in a queryset to MS Excel"""

    students_list, title, school = context_dict.get('students_list'), context_dict.get('report_title'), context_dict.get('school')

    style0 = easyxf('font: name Times New Roman, colour blue, bold on')
    style1 = easyxf('',num_format_str='D-MMM-YY')

    wb = Workbook()
    ws = wb.add_sheet()
    ws.write(0, 0, school.name, style0)
    ws.write(1, 0, school.address, style0)
    ws.write(1, 0, school.website, style0)
    ws.write(3, 0, title, style0)
    ws.write(3, 4, datetime.now(), style1)

    if 'withdraw' in title.lower():
        field_names = ['S/N', 'Name', 'Admission No', 'Reason', 'Date']
    else:
        field_names = ['S/N', 'Name', 'Sex', 'Admission No', 'Class', 'Arm', 'House']

    for i in len(field_names):
        ws.write(5, i, field_names[i], style0)

    row, counter = 6, 1
    for student in students_list:
        if 'withdraw' in title.lower():
            ws.write(row, 0, counter)
            ws.write(row, 1, student.fullname)
            ws.write(row, 2, student.admissionno)
            ws.write(row, 3, student.withdrawal__reason)
            ws.write(row, 4, student.withdrawal__date_withdrawn, style1)
        else:
            ws.write(row, 0, counter)
            ws.write(row, 1, student.fullname)
            ws.write(row, 2, student.sex)
            ws.write(row, 3, student.admissionno)
            ws.write(row, 4, student.admitted_class)
            ws.write(row, 5, student.admitted_arm)
            ws.write(row, 6, student.house)

        row += 1; counter += 1

    xls = StringIO.StringIO()
    wb.save(xls)
    response = HttpResponse(xls.getvalue(), mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=report.xls'

    return response

def studentaveragemid(admno,term,session,klass,arm): #mid term student average
     stu = Student.objects.get(admitted_session=session,gone=False,admitted_class=klass,admitted_arm=arm,admissionno=admno)
     acaderec=StudentAcademicRecord.objects.get(student=stu,term=term)
     totsub = SubjectScore.objects.filter(academic_rec = acaderec,term = term).count()
     subcount = SubjectScore.objects.filter(academic_rec = acaderec,term = term).aggregate(Sum('mid_term_score'))
     casum = subcount['mid_term_score__sum']
     staver=casum/int(totsub)
     StudentAcademicRecord.objects.filter(student=stu,term=term).update(stu_ave1=staver)
     
     return 'ok'

       

def studentaverageEnd(admno,term,session,klass,arm):

     if term=='third':
         j = Student.objects.filter(admissionno=admno, admitted_session=session,gone=False,admitted_class=klass,admitted_arm=arm)                
         acaderec=StudentAcademicRecord.objects.get(student=j,term=term)
         totsub = SubjectScore.objects.filter(academic_rec = acaderec,term = term).count()
         totalmark = SubjectScore.objects.filter(academic_rec = acaderec,term = term).aggregate(Sum('annual_avg'))
         totalmark2 = totalmark['annual_avg__sum']
         stave2=totalmark2 / int(totsub)
         StudentAcademicRecord.objects.filter(student=j,term=term).update(stu_ave2=stave2)   
     

     else:

         j = Student.objects.filter(admissionno=admno, admitted_session=session,gone=False,admitted_class=klass,admitted_arm=arm)                
         acaderec=StudentAcademicRecord.objects.get(student=j,term=term)
         totsub = SubjectScore.objects.filter(academic_rec = acaderec,term = term).count()
         totalmark = SubjectScore.objects.filter(academic_rec = acaderec,term = term).aggregate(Sum('end_term_score'))
         totalmark2 = totalmark['end_term_score__sum']
         stave2=totalmark2 / int(totsub)
         StudentAcademicRecord.objects.filter(student=j,term=term).update(stu_ave2=stave2)   
     
     return 'ok'


def classaveragemid(admno,klass,session,term,arm):
    if term == 'Third':
        academicins = StudentAcademicRecord.objects.get(term = term,
            session = session,
            klass = klass,
            arm = arm,
            student = Student.objects.get(admitted_session = session,gone=False,admitted_arm = arm,admitted_class = klass,admissionno = admno))
        totalsub = SubjectScore.objects.filter(klass = klass,arm = arm,academic_rec = academicins,session = session,term = term).count()
        totalmark = SubjectScore.objects.filter(klass = klass,arm = arm,academic_rec = academicins,session = session,term = term).aggregate(Sum('annual_avg'))
        totalmark2 = totalmark['annual_avg__sum']
        totalpecen = totalmark2/totalsub
        academicins.stu_ave2 = totalpecen
        academicins.save()

    else:
        casum=0
        totsub=0
        stu = Student.objects.filter(admitted_session=session,gone=False,admitted_class=klass,admitted_arm=arm)  
        for j in stu:
            acaderec=StudentAcademicRecord.objects.get(student=j,term=term)
            totsubject = SubjectScore.objects.filter(academic_rec = acaderec,term = term).count()
            subcount = SubjectScore.objects.filter(academic_rec = acaderec,term = term).aggregate(Sum('mid_term_score'))
            midsum = subcount['mid_term_score__sum']
            totsub=totsub+totsubject
            casum=casum+ midsum

        clasAve=casum/int(totsub)
        for j in stu:
            StudentAcademicRecord.objects.filter(student=j,term=term).update(class_ave1=clasAve)
         
        return 'ok'


def classaverageEnd(klass,session,term,arm):

    if term == 'Third':
        casum=0
        totsub=0
        stu = Student.objects.filter(admitted_session=session,gone=False,admitted_class=klass,admitted_arm=arm)  
        for j in stu:
            acaderec=StudentAcademicRecord.objects.get(student=j,term=term)
            totsubject = SubjectScore.objects.filter(academic_rec = acaderec,term = term).count()
            subcount = SubjectScore.objects.filter(academic_rec = acaderec,term = term).aggregate(Sum('annual_avg'))
            midsum = subcount['annual_avg__sum']
            totsub=totsub+totsubject
            casum=casum+ midsum

        clasAve=casum/int(totsub)
        for j in stu:
            StudentAcademicRecord.objects.filter(student=j,term=term).update(class_ave2=clasAve)








        # academicins = StudentAcademicRecord.objects.get(term = term, session = session,klass = klass,
        #     arm = arm, student = Student.objects.filter(admitted_session = session,gone=False,admitted_arm = arm,admitted_class = klass))
        
        # totalsub = SubjectScore.objects.filter(klass = klass,arm = arm,academic_rec = academicins,session = session,term = term).count()
        # totalmark = SubjectScore.objects.filter(klass = klass,arm = arm,academic_rec = academicins,session = session,term = term).aggregate(Sum('annual_avg'))
        # totalmark2 = totalmark['annual_avg__sum']
        # totalpecen = totalmark2/totalsub
        # academicins.class_ave2 = totalpecen
        # academicins.save()

    else:
        casum=0
        totsub=0
        stu = Student.objects.filter(admitted_session=session,gone=False,admitted_class=klass,admitted_arm=arm)  
        for j in stu:
            acaderec=StudentAcademicRecord.objects.get(student=j,term=term)
            totsubject = SubjectScore.objects.filter(academic_rec = acaderec,term = term).count()
            subcount = SubjectScore.objects.filter(academic_rec = acaderec,term = term).aggregate(Sum('end_term_score'))
            midsum = subcount['end_term_score__sum']
            totsub=totsub+totsubject
            casum=casum+ midsum

        clasAve=casum/int(totsub)
        for j in stu:
            StudentAcademicRecord.objects.filter(student=j,term=term).update(class_ave2=clasAve)
         
        return 'ok' 





def annualaverage(admno,session,arm,klass,subject):
    stuinfo = Student.objects.get(admitted_session = session,admitted_class = klass,admissionno = admno,admitted_arm = arm)
    acaderec = StudentAcademicRecord.objects.filter(student = stuinfo,session = session)
    summ = 0
    tcount = 0
    for j in acaderec:
        if SubjectScore.objects.filter(academic_rec = j,klass = klass,subject = subject,session = session):
            totsubject1 = SubjectScore.objects.get(academic_rec = j,klass = klass,subject = subject,session = session)
            if float(totsubject1.end_term_score) <= 0 :
                pass
            else:
                summ = summ + totsubject1.end_term_score
                tcount  += 1
        else:
            pass
    if tcount == 0:
        annavg = 0
    else:
        annavg = float(summ)/float(tcount)
    stuinfo3 = Student.objects.get(admitted_session = session,admitted_class = klass,admissionno = admno,admitted_arm = arm)
    acaderect = StudentAcademicRecord.objects.get(student = stuinfo3,session = session,term = 'Third')
    if SubjectScore.objects.filter(academic_rec = acaderect,klass = klass,subject = subject,session = session,term = 'Third'):
        jannual = SubjectScore.objects.get(academic_rec = acaderect,klass = klass,subject = subject,session = session,term = 'Third')
        jannual.annual_avg = annavg
        jannual.save()
    else:
        pass
    return 'ok'


def percent(session,klass,arm,admno,term):
    if term == 'Third':
        academicins = StudentAcademicRecord.objects.get(term = term,session = session,klass = klass,arm = arm,student = Student.objects.get(admitted_session = session,admitted_arm = arm,admitted_class = klass,admissionno = admno))
        totalsub = SubjectScore.objects.filter(klass = klass,arm = arm,academic_rec = academicins,session = session,term = term).count()
        totalmark = SubjectScore.objects.filter(klass = klass,arm = arm,academic_rec = academicins,session = session,term = term).aggregate(Sum('annual_avg'))
        totalmark2 = totalmark['annual_avg__sum']
        totalpecen = totalmark2/totalsub
        academicins.stu_ave2 = totalpecen
        academicins.save()
    else:
        academicins = StudentAcademicRecord.objects.get(term = term,session = session,klass = klass,arm = arm,student = Student.objects.get(admitted_session = session,admitted_arm = arm,admitted_class = klass,admissionno = admno))
        totalsub = SubjectScore.objects.filter(klass = klass,arm = arm,academic_rec = academicins,session = session,term = term).count()
        totalmark = SubjectScore.objects.filter(klass = klass,arm = arm,academic_rec = academicins,session = session,term = term).aggregate(Sum('end_term_score'))
        totalmark2 = totalmark['end_term_score__sum']
        totalpecen = totalmark2/totalsub
        academicins.stu_ave2 = totalpecen
        academicins.save()
    return 'ok'

def classposition(session,term,klass,arm):
    if term == 'Third':
        stulist = StudentAcademicRecord.objects.filter(term = term,session = session,klass = klass)
        stuperc = []
        for k in stulist:
            stuperc.append(k.stu_ave2)
        stuperc.sort(reverse=True)
        dicper ={}
        for g in stuperc:
            dic = {g:g}
            dicper.update(dic)
        flist = dicper.values()
        flist.sort(reverse=True)
        n = 1
        for d in flist:
            pos = ordinal(n)
            StudentAcademicRecord.objects.filter(term = term,session = session,klass = klass,stu_ave2 = d).update(position = pos)
            j = stuperc.count(d)
            n  += j
            #end of position
    else:
        stulist = StudentAcademicRecord.objects.filter(term = term,session = session,klass = klass,arm = arm)
        stuperc = []
        for k in stulist:
            stuperc.append(k.stu_ave2)
        stuperc.sort(reverse=True)
        dicper ={}
        for g in stuperc:
            dic = {g:g}
            dicper.update(dic)
        flist = dicper.values()
        flist.sort(reverse=True)
        n = 1
        for d in flist:
            pos = ordinal(n)
            StudentAcademicRecord.objects.filter(term = term,session = session,klass = klass,arm = arm,stu_ave2 = d).update(position = pos)
            j = stuperc.count(d)
            n += j
    return 'ok'

def classposition1(session,term,klass):
    if term == 'Third':
        stulist =StudentAcademicRecord.objects.filter(term = term,session = session,klass = klass)
        stuperc = []
        for k in stulist:
            stuperc.append(k.stu_ave2)
        stuperc.sort(reverse=True)
        dicper ={}
        for g in stuperc:
            dic = {g:g}
            dicper.update(dic)
        flist = dicper.values()
        flist.sort(reverse=True)
        n = 1
        for d in flist:
            pos = ordinal(n)
            StudentAcademicRecord.objects.filter(term = term,session = session,klass = klass,stu_ave2 = d).update(position1 = pos)
            j = stuperc.count(d)
            n  += j
            #end of position
    else:
        stulist = StudentAcademicRecord.objects.filter(term = term,session = session,klass = klass)
        stuperc = []
        for k in stulist:
            stuperc.append(k.stu_ave2)
        stuperc.sort(reverse=True)
        dicper ={}
        for g in stuperc:
            dic = {g:g}
            dicper.update(dic)
        flist = dicper.values()
        flist.sort(reverse=True)
        n = 1
        for d in flist:
            pos = ordinal(n)
            StudentAcademicRecord.objects.filter(term = term,session = session,klass = klass,stu_ave2 = d).update(position1 = pos)
            j = stuperc.count(d)
            n += j
    return 'ok'



def subjectposition(session,subject,term,klass,arm):
    if term == 'Third':
        subpli = SubjectScore.objects.filter(klass = klass,arm = arm,subject = subject,session = session,term = term)
        stusubp = []
        for h in subpli:
            stusubp.append(h.annual_avg)
        stusubp.sort(reverse=True)
        dicsubp = {}
        for n in stusubp:
            ddic = {n:n}
            dicsubp.update(ddic)
        dflist = dicsubp.values()
        dflist.sort(reverse=True)
        b = 1
        for t in dflist:
            spos = ordinal(b)
            SubjectScore.objects.filter(klass = klass,arm = arm,subject = subject,session = session,term = term,annual_avg = t).update(subposition = spos)
            f = stusubp.count(t)
            b += f
    else:
        subpli = SubjectScore.objects.filter(klass = klass,arm = arm,subject = subject,session = session,term = term)
        stusubp = []
        for h in subpli:
            stusubp.append(h.end_term_score)
        stusubp.sort(reverse=True)
        dicsubp = {}
        for n in stusubp:
            ddic = {n:n}
            dicsubp.update(ddic)
        dflist = dicsubp.values()
        dflist.sort(reverse=True)
        b = 1
        for t in dflist:
            spos = ordinal(b)
            SubjectScore.objects.filter(klass = klass,arm = arm,subject = subject,session = session,term = term,end_term_score = t).update(subposition = spos)
            f = stusubp.count(t)
            b += f
    return 'ok'

#*************This function get the position at run term for mid-term Position *************************
def mid_term_position(session,term,klass,arm):
    stuperc = []
    stuinfo = Student.objects.filter(admitted_session = session,admitted_class = klass,admitted_arm = arm,gone = False).order_by('-sex','fullname')
    submid = 0
    for uuu in Subject.objects.all():
        submid = uuu.ca
    submiddiv = int(submid)/2 #divide total CA by 2 e.g if ca = 30 we need 15
    if klass [0] == 'N' or klass [0] == 'P':
        submiddiv = 40
    else:
        submiddiv= 30

    for j in stuinfo:
        stuper = 0
        if StudentAcademicRecord.objects.filter(student = j,term = term):
           acaderec = StudentAcademicRecord.objects.get(student = j,term = term)
           totsub = SubjectScore.objects.filter(academic_rec = acaderec,term = term).count()
           totalmarkcount = SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term).count()
           subsco = SubjectScore.objects.filter(academic_rec = acaderec,term = term).order_by('num')
           tscore = 0
           for jj in subsco:
               mca = jj.mid_term
               fca = jj.first_ca
               sca = jj.second_ca
               tca = jj.third_ca
               totalca = mca
               #totalca = fca #+ sca+tca
               totalperc1 = totalca/submiddiv
               totalperc = totalperc1 * 100 # getting the percentage
               tscore += totalperc
               if totalmarkcount == 0:
                  stuper = 0
               else:
                  stuper = tscore / totalmarkcount
        else:
           pass
        stuperc.append(stuper)
    stuperc.sort(reverse=True)
    dicper ={}
    for g in stuperc:
        dic = {g:g}
        dicper.update(dic)
    flist = dicper.values()
    flist.sort(reverse=True)
    n = 1
    fdic = {}
    for d in flist:
        pos = ordinal(n)
        fdic.update({d:pos})
        j = stuperc.count(d)
        n  += j
    return fdic



def mid_term_position1(session,term,klass,arm):
    stuperc = []
    stuinfo = Student.objects.filter(admitted_session = session,admitted_class = klass,admitted_arm = arm,gone = False).order_by('-sex','fullname')
    submid = 0
    for uuu in Subject.objects.all():
        submid = uuu.ca
    submiddiv = int(submid)/2 #divide total CA by 2 e.g if ca = 30 we need 15
    if klass [0] == 'N' or klass [0] == 'P':
        submiddiv = 40
    else:
        submiddiv= 20
    for j in stuinfo:
        stuper = 0
        if StudentAcademicRecord.objects.filter(student = j,term = term):
           acaderec = StudentAcademicRecord.objects.get(student = j,term = term)
           totsub = SubjectScore.objects.filter(academic_rec = acaderec,term = term).count()
           totalmarkcount = SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term).count()
           subsco = SubjectScore.objects.filter(academic_rec = acaderec,term = term).order_by('num')
           tscore = 0
  
           for jj in subsco:
               mca = jj.mid_term
               fca = jj.first_ca
               sca = jj.second_ca
               tca = jj.third_ca
               totalca = mca
               #totalca = fca #+ sca+tca
               totalperc1 = fca/submiddiv
               totalperc = totalperc1 * 100 # getting the percentage
               tscore += totalperc
               if totalmarkcount == 0:
                  stuper = 0
               else:
                  stuper = tscore / totalmarkcount
        else:
           pass
        stuperc.append(stuper)
    stuperc.sort(reverse=True)
    dicper ={}
    for g in stuperc:
        dic = {g:g}
        dicper.update(dic)
    flist = dicper.values()
    flist.sort(reverse=True)
    n = 1
    fdic = {}
    for d in flist:
        pos = ordinal(n)
        fdic.update({d:pos})
        j = stuperc.count(d)
        n  += j
    return fdic

#************************getting mid term subject position **************************************
def mid_term_subjectposition(session,subject,term,klass,arm):
        subpli = SubjectScore.objects.filter(klass = klass,arm = arm,subject = subject,session = session,term = term)
        stusubp = []
        for h in subpli:
            stusubp.append(h.mid_term_score)
        stusubp.sort(reverse=True)
        dicsubp = {}
        for n in stusubp:
            ddic = {n:n}
            dicsubp.update(ddic)
        dflist = dicsubp.values()
        dflist.sort(reverse=True)
        b = 1
        fdic = {}
        for t in dflist:
            spos = ordinal(b)
            fdic.update({t:spos})
            f = stusubp.count(t)
            b += f
        #print 'Dic',fdic,'student score :',stuper
        stuposi = fdic[stuper]
        return stuposi


