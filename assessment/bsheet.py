from myproject.academics.models import *
from myproject.academics.utils import *
from myproject.setup.models import *
from myproject.assessment.getordinal import *
import locale
locale.setlocale(locale.LC_ALL,'')


def bsheetforj(term,session,klass):
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
    stulist = []
    subavg = {}
    gavglist = []
    if term == 'Third':
        stuinfo = Student.objects.filter(admitted_session = session,admitted_class = klass,gone = False)
        for j in stuinfo:
            acaderec = StudentAcademicRecord.objects.filter(student = j,session = session,term = term)
            getdic = {}
            totscore = 0
            tosub = 0
            for js in sublist:
                if SubjectScore.objects.filter(academic_rec = acaderec,klass = klass,session = session,subject = js).count() == 0:
                    u = {js:0}
                else:
                    totsubject = SubjectScore.objects.get(academic_rec = acaderec,klass = klass,session = session,subject = js)
                    u = {js:totsubject.annual_avg}
                    totscore += totsubject.annual_avg
                    tosub += 1
                getdic.update(u)
            if tosub == 0:
                avgscore = 0
            else:
                avgscore = totscore/tosub
            l ={'stname':j.fullname,'admno':j.admissionno,'totalscore':totscore,'avgscore':avgscore,'subjects':getdic}
            stulist.append(l)
            ka = {avgscore:avgscore}
            subavg.update(ka)
            gavglist.append(avgscore)
    else:
        stuinfo = Student.objects.filter(admitted_session = session,admitted_class = klass,gone = False)
        for j in stuinfo:
            acaderec = StudentAcademicRecord.objects.filter(student = j,session = session,term = term)
            getdic = {}
            totscore = 0
            tosub = 0
            for js in sublist:
                if SubjectScore.objects.filter(academic_rec = acaderec,klass = klass,session = session,subject = js).count() == 0:
                    u = {js:0}
                else:
                    totsubject = SubjectScore.objects.get(academic_rec = acaderec,klass = klass,session = session,subject = js)
                    u = {js:totsubject.end_term_score}
                    totscore += totsubject.end_term_score
                    tosub += 1
                getdic.update(u)
            if tosub == 0:
                avgscore = 0
            else:
                avgscore = totscore/tosub
            l ={'stname':j.fullname,'admno':j.admissionno,'totalscore':totscore,'avgscore':avgscore,'subjects':getdic}
            stulist.append(l)
            ka = {avgscore:avgscore}
            subavg.update(ka)
            gavglist.append(avgscore)
    avglist = subavg.keys()
    avglist.sort(reverse=True)
    n = 1
    #print 'old list',stuperc,'new list',flist
    finallist = []
    for d in avglist:
        pos = ordinal(n)
        for stl in stulist:
            if stl['avgscore'] == d:
                jl = {'studentlist':stl,'pos':pos}
                finallist.append(jl)
        j = gavglist.count(d)
        n += j
    return finallist


def bsheetforja(term,session,klass,arm):
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
    stulist = []
    subavg = {}
    gavglist = []
    if term == 'Third':
        stuinfo = Student.objects.filter(admitted_session = session,admitted_class = klass,gone = False, admitted_arm=arm)
        for j in stuinfo:
            acaderec = StudentAcademicRecord.objects.filter(student = j,session = session,term = term)
            getdic = {}
            totscore = 0
            tosub = 0
            for js in sublist:
                if SubjectScore.objects.filter(academic_rec = acaderec,klass = klass,session = session,subject = js).count() == 0:
                    u = {js:0}
                else:
                    totsubject = SubjectScore.objects.get(academic_rec = acaderec,klass = klass,session = session,subject = js)
                    u = {js:totsubject.annual_avg}
                    totscore += totsubject.annual_avg
                    tosub += 1
                getdic.update(u)
            if tosub == 0:
                avgscore = 0
            else:
                avgscore = totscore/tosub
            l ={'stname':j.fullname,'admno':j.admissionno,'totalscore':totscore,'avgscore':avgscore,'subjects':getdic}
            stulist.append(l)
            ka = {avgscore:avgscore}
            subavg.update(ka)
            gavglist.append(avgscore)
    else:
        stuinfo = Student.objects.filter(admitted_session = session,admitted_class = klass,gone = False, admitted_arm=arm)
        for j in stuinfo:
            acaderec = StudentAcademicRecord.objects.filter(student = j,session = session,term = term)
            getdic = {}
            totscore = 0
            tosub = 0
            for js in sublist:
                if SubjectScore.objects.filter(academic_rec = acaderec,klass = klass,session = session,subject = js).count() == 0:
                    u = {js:0}
                else:
                    totsubject = SubjectScore.objects.get(academic_rec = acaderec,klass = klass,session = session,subject = js)
                    u = {js:totsubject.end_term_score}
                    totscore += totsubject.end_term_score
                    tosub += 1
                getdic.update(u)
            if tosub == 0:
                avgscore = 0
            else:
                avgscore = totscore/tosub
            l ={'stname':j.fullname,'admno':j.admissionno,'totalscore':totscore,'avgscore':avgscore,'subjects':getdic}
            stulist.append(l)
            ka = {avgscore:avgscore}
            subavg.update(ka)
            gavglist.append(avgscore)
    avglist = subavg.keys()
    avglist.sort(reverse=True)
    n = 1
    #print 'old list',stuperc,'new list',flist
    finallist = []
    for d in avglist:
        pos = ordinal(n)
        for stl in stulist:
            if stl['avgscore'] == d:
                jl = {'studentlist':stl,'pos':pos}
                finallist.append(jl)
        j = gavglist.count(d)
        n += j
    return finallist




def bsheetfors(term,session,klass):
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
    stulist = []
    if term == 'Third':
        stuinfo = Student.objects.filter(admitted_session = session,admitted_class = klass,gone = False)
        for j in stuinfo:
            acaderec = StudentAcademicRecord.objects.filter(student = j,session = session,term = term)
            getdic = {}
            da = 0
            db = 0
            dc = 0
            dd = 0
            de = 0
            df = 0
            stgrade = ''
            for js in sublist:
                if SubjectScore.objects.filter(academic_rec = acaderec,klass = klass,session = session,subject = js).count() == 0:
                    u = {js:0}
                else:
                    totsubject = SubjectScore.objects.get(academic_rec = acaderec,klass = klass,session = session,subject = js)
                    u = {js:totsubject.annual_avg}
                    g = totsubject.grade
                    if g[0] == 'A':
                        da += 1
                    elif g[0] == 'B':
                        db += 1
                    elif  g[0] == 'C':
                        dc += 1
                    elif g[0] == 'D':
                        dd += 1
                    elif  g[0] == 'E':
                       de += 1
                    else:
                        df +=1
                stgrade = str(da) +'A,'+str(db)+'B,'+str(dc)+'C,'+str(dd)+'D,'+str(de)+'E,'+str(df)+'F'
                getdic.update(u)
            l ={'stname':j.fullname,'admno':j.admissionno,'grade':stgrade,'subjects':getdic}
            stulist.append(l)
    else:
        stuinfo = Student.objects.filter(admitted_session = session,admitted_class = klass,gone = False)
        for j in stuinfo:
            acaderec = StudentAcademicRecord.objects.filter(student = j,session = session,term = term)
            getdic = {}
            da = 0
            db = 0
            dc = 0
            dd = 0
            de = 0
            df = 0
            stgrade = ''
            for js in sublist:
                if SubjectScore.objects.filter(academic_rec = acaderec,klass = klass,session = session,subject = js).count() == 0:
                    u = {js:0}
                else:
                    totsubject = SubjectScore.objects.get(academic_rec = acaderec,klass = klass,session = session,subject = js)
                    u = {js:totsubject.end_term_score}
                    g = totsubject.grade
                    if g[0] == 'A':
                        da += 1
                    elif g[0] == 'B':
                        db += 1
                    elif  g[0] == 'C':
                        dc += 1
                    elif g[0] == 'D':
                        dd += 1
                    elif  g[0] == 'E':
                        de += 1
                    else:
                        df +=1
                stgrade = str(da) +'A,'+str(db)+'B,'+str(dc)+'C,'+str(dd)+'D,'+str(de)+'E,'+str(df)+'F'
                getdic.update(u)
            l ={'stname':j.fullname,'admno':j.admissionno,'grade':stgrade,'subjects':getdic}
            stulist.append(l)
    return stulist


def bsheetforsa(term,session,klass,arm):
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
    stulist = []
    if term == 'Third':
        stuinfo = Student.objects.filter(admitted_session = session,admitted_class = klass,gone = False,admitted_arm=arm)
        for j in stuinfo:
            acaderec = StudentAcademicRecord.objects.filter(student = j,session = session,term = term)
            getdic = {}
            da = 0
            db = 0
            dc = 0
            dd = 0
            de = 0
            df = 0
            stgrade = ''
            for js in sublist:
                if SubjectScore.objects.filter(academic_rec = acaderec,klass = klass,session = session,subject = js).count() == 0:
                    u = {js:0}
                else:
                    totsubject = SubjectScore.objects.get(academic_rec = acaderec,klass = klass,session = session,subject = js)
                    u = {js:totsubject.annual_avg}
                    g = totsubject.grade
                    if g[0] == 'A':
                        da += 1
                    elif g[0] == 'B':
                        db += 1
                    elif  g[0] == 'C':
                        dc += 1
                    elif g[0] == 'D':
                        dd += 1
                    elif  g[0] == 'E':
                       de += 1
                    else:
                        df +=1
                stgrade = str(da) +'A,'+str(db)+'B,'+str(dc)+'C,'+str(dd)+'D,'+str(de)+'E,'+str(df)+'F'
                getdic.update(u)
            l ={'stname':j.fullname,'admno':j.admissionno,'grade':stgrade,'subjects':getdic}
            stulist.append(l)
    else:
        stuinfo = Student.objects.filter(admitted_session = session,admitted_class = klass,gone = False,admitted_arm=arm)
        for j in stuinfo:
            acaderec = StudentAcademicRecord.objects.filter(student = j,session = session,term = term)
            getdic = {}
            da = 0
            db = 0
            dc = 0
            dd = 0
            de = 0
            df = 0
            stgrade = ''
            for js in sublist:
                if SubjectScore.objects.filter(academic_rec = acaderec,klass = klass,session = session,subject = js).count() == 0:
                    u = {js:0}
                else:
                    totsubject = SubjectScore.objects.get(academic_rec = acaderec,klass = klass,session = session,subject = js)
                    u = {js:totsubject.end_term_score}
                    g = totsubject.grade
                    if g[0] == 'A':
                        da += 1
                    elif g[0] == 'B':
                        db += 1
                    elif  g[0] == 'C':
                        dc += 1
                    elif g[0] == 'D':
                        dd += 1
                    elif  g[0] == 'E':
                        de += 1
                    else:
                        df +=1
                stgrade = str(da) +'A,'+str(db)+'B,'+str(dc)+'C,'+str(dd)+'D,'+str(de)+'E,'+str(df)+'F'
                getdic.update(u)
            l ={'stname':j.fullname,'admno':j.admissionno,'grade':stgrade,'subjects':getdic}
            stulist.append(l)
    return stulist




#***********************************************************Treating mid term broad sheet ***********************
def mid_term_bsheetforj(term,session,klass):
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
    stulist = []
    subavg = {}
    gavglist = []
    stuinfo = Student.objects.filter(admitted_session = session,admitted_class = klass,gone = False)
    submid = 0
    for uuu in Subject.objects.all():
        submid = uuu.ca
        submiddiv = int(submid)/2#divide total CA by 2 e.g if ca = 30 we need 15 
    for j in stuinfo:
            acaderec = StudentAcademicRecord.objects.filter(student = j,session = session,term = term)
            getdic = {}
            totscore = 0
            tosub = 0
            for js in sublist:
                if SubjectScore.objects.filter(academic_rec = acaderec,klass = klass,session = session,subject = js).count() == 0:
                    u = {js:0}
                else:
                    totsubject = SubjectScore.objects.get(academic_rec = acaderec,klass = klass,session = session,subject = js)
                    score = totsubject.first_ca
                    totalperc1 = score/submiddiv
                    totalperc = totalperc1 * 100
                    u = {js:locale.format("%.2f",totalperc,grouping=True)}
                    totscore += totalperc
                    tosub += 1
                getdic.update(u)
            if tosub == 0:
                avgscore = 0
            else:
                avgscore = totscore/tosub
            l ={'stname':j.fullname,'admno':j.admissionno,'totalscore':locale.format("%.2f",totscore,grouping=True),'avgscore':avgscore,'subjects':getdic}
            stulist.append(l)
            ka = {avgscore:avgscore}
            subavg.update(ka)
            gavglist.append(avgscore)
    avglist = subavg.keys()
    avglist.sort(reverse=True)
    n = 1
    finallist = []
    for d in avglist:
        pos = ordinal(n)
        for stl in stulist:
            if stl['avgscore'] == d:
                jl = {'studentlist':stl,'pos':pos}
                finallist.append(jl)
        j = gavglist.count(d)
        n += j
    return finallist


def mid_term_bsheetforja(term,session,klass,arm):
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
    stulist = []
    subavg = {}
    gavglist = []
    stuinfo = Student.objects.filter(admitted_session = session,admitted_class = klass,gone = False)
    submid = 0
    for uuu in Subject.objects.all():
        submid = uuu.ca
        submiddiv = int(submid)/2#divide total CA by 2 e.g if ca = 30 we need 15 
    for j in stuinfo:
            acaderec = StudentAcademicRecord.objects.filter(student = j,session = session,term = term)
            getdic = {}
            totscore = 0
            tosub = 0
            for js in sublist:
                if SubjectScore.objects.filter(academic_rec = acaderec,klass = klass,session = session,subject = js).count() == 0:
                    u = {js:0}
                else:
                    totsubject = SubjectScore.objects.get(academic_rec = acaderec,klass = klass,session = session,subject = js)
                    score = totsubject.first_ca
                    totalperc1 = score/submiddiv
                    totalperc = totalperc1 * 100
                    u = {js:locale.format("%.2f",totalperc,grouping=True)}
                    totscore += totalperc
                    tosub += 1
                getdic.update(u)
            if tosub == 0:
                avgscore = 0
            else:
                avgscore = totscore/tosub
            l ={'stname':j.fullname,'admno':j.admissionno,'totalscore':locale.format("%.2f",totscore,grouping=True),'avgscore':avgscore,'subjects':getdic}
            stulist.append(l)
            ka = {avgscore:avgscore}
            subavg.update(ka)
            gavglist.append(avgscore)
    avglist = subavg.keys()
    avglist.sort(reverse=True)
    n = 1
    finallist = []
    for d in avglist:
        pos = ordinal(n)
        for stl in stulist:
            if stl['avgscore'] == d:
                jl = {'studentlist':stl,'pos':pos}
                finallist.append(jl)
        j = gavglist.count(d)
        n += j
    return finallist



def mid_term_bsheetfors(term,session,klass):
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
    stulist = []
    stuinfo = Student.objects.filter(admitted_session = session,admitted_class = klass,gone = False)
    submid = 0
    for uuu in Subject.objects.all():
        submid = uuu.ca
        submiddiv = int(submid)/2#divide total CA by 2 e.g if ca = 30 we need 15 
    for j in stuinfo:
            acaderec = StudentAcademicRecord.objects.filter(student = j,session = session,term = term)
            getdic = {}
            da = 0
            db = 0
            dc = 0
            dd = 0
            de = 0
            df = 0
            stgrade = ''
            for js in sublist:
                if SubjectScore.objects.filter(academic_rec = acaderec,klass = klass,session = session,subject = js).count() == 0:
                    u = {js:0}
                else:
                    totsubject = SubjectScore.objects.get(academic_rec = acaderec,klass = klass,session = session,subject = js)
                    score = totsubject.first_ca
                    totalperc1 = score/submiddiv
                    totalperc = totalperc1 * 100
                    u = {js:locale.format("%.2f",totalperc,grouping=True)}
                    gr = seniorgrade(totalperc)
                    g = gr['grade']
                    if g == "":
                        df +=1
                    else:
                        if g[0] == 'A':
                            da += 1
                        elif g[0] == 'B':
                            db += 1
                        elif  g[0] == 'C':
                            dc += 1
                        elif g[0] == 'D':
                            dd += 1
                        elif  g[0] == 'E':
                            de += 1
                        else:
                            df +=1
                stgrade = str(da) +'A,'+str(db)+'B,'+str(dc)+'C,'+str(dd)+'D,'+str(de)+'E,'+str(df)+'F'
                getdic.update(u)
            l ={'stname':j.fullname,'admno':j.admissionno,'grade':stgrade,'subjects':getdic}
            stulist.append(l)
    return stulist


def mid_term_bsheetforsa(term,session,klass,arm):
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
    stulist = []
    stuinfo = Student.objects.filter(admitted_session = session,admitted_class = klass,gone = False)
    submid = 0
    for uuu in Subject.objects.all():
        submid = uuu.ca
        submiddiv = int(submid)/2#divide total CA by 2 e.g if ca = 30 we need 15 
    for j in stuinfo:
            acaderec = StudentAcademicRecord.objects.filter(student = j,session = session,term = term)
            getdic = {}
            da = 0
            db = 0
            dc = 0
            dd = 0
            de = 0
            df = 0
            stgrade = ''
            for js in sublist:
                if SubjectScore.objects.filter(academic_rec = acaderec,klass = klass,session = session,subject = js).count() == 0:
                    u = {js:0}
                else:
                    totsubject = SubjectScore.objects.get(academic_rec = acaderec,klass = klass,session = session,subject = js)
                    score = totsubject.first_ca
                    totalperc1 = score/submiddiv
                    totalperc = totalperc1 * 100
                    u = {js:locale.format("%.2f",totalperc,grouping=True)}
                    gr = seniorgrade(totalperc)
                    g = gr['grade']
                    if g == "":
                        df +=1
                    else:
                        if g[0] == 'A':
                            da += 1
                        elif g[0] == 'B':
                            db += 1
                        elif  g[0] == 'C':
                            dc += 1
                        elif g[0] == 'D':
                            dd += 1
                        elif  g[0] == 'E':
                            de += 1
                        else:
                            df +=1
                stgrade = str(da) +'A,'+str(db)+'B,'+str(dc)+'C,'+str(dd)+'D,'+str(de)+'E,'+str(df)+'F'
                getdic.update(u)
            l ={'stname':j.fullname,'admno':j.admissionno,'grade':stgrade,'subjects':getdic}
            stulist.append(l)
    return stulist


