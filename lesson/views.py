from django.shortcuts import render_to_response
from myproject.lesson.forms import *
from myproject.setup.models import *
from myproject.sysadmin.models import *
from myproject.student.models import *
from myproject.lesson.models import *
from assessment.views import sublists
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from django.core.serializers.json import json
import datetime
import os
from myproject import settings

def wel(request):
    if  "userid" in request.session:
        varuser=request.session['userid']
        return render_to_response('lesson/success.html',{'varuser':varuser})
    else:
        return HttpResponseRedirect('/login/')

def settopic(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr = ''
        if request.method == 'POST':
            form = settopicForm(request.POST)
            if form.is_valid():
                 klass = form.cleaned_data['klass']
                 session = form.cleaned_data['session']
                 term = form.cleaned_data['term']
                 subject= form.cleaned_data['subject']
                 topic=form.cleaned_data['topic']
                 top = topic.upper()
                 tab = 'FALSE'
                 if tbltopic.objects.filter(topic=top, term = term):
                     varerr = 'TOPIC ALREADY ENTERED'
                     tab = 'TRUE'
                 if tab =='FALSE':                       
                     less = tbltopic(term = term,klass = klass,topic = top,subject=subject).save()
                     form=  settopicForm()
                     varerr = 'TOPIC ENTERED SUCCESSFULLY'
            else:
                varerr = 'topic not entered'
        else:
            form = settopicForm()
        return render_to_response('lesson/setup.html',{'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')


def topajax(request):
    if "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varerr = ""
                varuser = request.session['userid']
                post = request.POST.copy()
                accode = post['userid']
                subject,klass,term = accode.split(':') #order must follow that in the autopost script in html
                sett = tbltopic.objects.filter(klass = klass,term = term, subject = subject)
                return render_to_response('lesson/topajax.html',{'sett':sett,'varerr':varerr, 'term':term,'klass':klass,'subject':subject})
            else:
                sett = ""
            return render_to_response ('lesson/topajax.html',{'sett':sett})
        else:
            sett = ""
            return render_to_response ('lesson/topajax.html',{'sett':sett})


def deletetopiccode(request, sid):
    if "userid" in request.session:
        varuser = request.session['userid']
        getdetails= tbltopic.objects.get(id = sid)
        con=tblcontents.objects.filter(content=getdetails)
        ir=tblir.objects.filter(topic=getdetails)
        for c in con and ir:
            c.delete()
        getdetails.delete()
        return HttpResponseRedirect('/lesson/set_up/')
    else:
        return HttpResponseRedirect('/login/')

def getsubajax(request):
    if "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                post = request.POST.copy()
                accode = post['userid']
                subject,klass,term = accode.split(':') #order must follow that in the autopost script in html
                sett = tbltopic.objects.filter(klass = klass,term = term, subject = subject)
                return render_to_response('lesson/setsub.html',{'sett':sett})
            else:
                sett = ""
            return render_to_response ('lesson/setsub.html',{'sett':sett})
        else:
            sett = ""
            return render_to_response ('lesson/setsub.html',{'sett':sett})


def setsub(request):
    if "userid" in request.session:
        varuser = request.session['userid']
        varerr = ""
        form = setobjForm()
        return render_to_response('lesson/subt.html',{'form':form,'varuser':varuser})
    else:
        return HttpResponseRedirect('/login/')


def entercont(request):
        if  "userid" in request.session:
            if request.is_ajax():
                if request.method == 'POST':
                    varuser = request.session['userid']
                    varerr =""
                    post = request.POST.copy()
                    acccode = post['userid']
                    state=acccode
                    getdetails = tbltopic.objects.get(id = state)
                    return render_to_response('lesson/entersub.html',{'getdetails':getdetails,'state':acccode})
                else:
                    gdata = ""
                    return render_to_response('index.html',{'gdata':gdata})
            else:

                getdetails = tblcontents.objects.filter(topic=id)
                return render_to_response('lesson/entersub.html',{'gdata':getdetails})
        else:
            return HttpResponseRedirect('/login/')


def obj(request):
        if  "userid" in request.session:
            if request.is_ajax():
                if request.method == 'POST':
                    varuser = request.session['userid']
                    varerr =""
                    post = request.POST.copy()
                    acccode = post['userid']
                    state=acccode
                    getdetails = tblcontents.objects.get(id = state)
                    return render_to_response('lesson/enterobj.html',{'getdetails':getdetails,'state':acccode})
        else:
            return HttpResponseRedirect('/login/')


def enterobj(request,vid):
    if "userid" in request.session:
        varuser = request.session['userid']
        varerr = ''
        if request.method=='POST':
            objectives=request.POST['objectives']
            objectives= objectives.lower()
            tr= tblcontents.objects.get(id = vid)
            c=tblobjectives.objects.filter(content=tr)
            for k in c:
                if k.objectives== objectives:
                    return HttpResponseRedirect('/lesson/set_up/obj')
            tblobjectives(objectives=objectives, content=tr).save()
            return HttpResponseRedirect('/lesson/set_up/obj')
    else:
        return HttpResponseRedirect('/login/')    


def cont(request,vid):
    if "userid" in request.session:
        varuser = request.session['userid']
        varerr = ''
        if request.method=='POST':
            content=request.POST['content']
            content= content.lower()
            tr= tbltopic.objects.get(id = vid)
            c=tblcontents.objects.filter(topic=tr)
            for k in c:
                if k.content == content:
                    return HttpResponseRedirect('/lesson/setup_sub/')
            tblcontents(content=content,topic=tr).save()
            return HttpResponseRedirect('/lesson/setup_sub/')
    else:
        return HttpResponseRedirect('/login/')



def filsubtop(request):
    if "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varerr = ""
                varuser = request.session['userid']
                post = request.POST.copy()
                accode=post['userid']
                state=accode
                sublist=[]
                subject,klass,term=state.split(':')
                # subject,klass,term=accode.split(':')
                sott = tbltopic.objects.filter(subject=subject,klass=klass,term=term).order_by('id')
#********** obtain topic id ***********************#
                if tbltopic.objects.filter(subject=subject,klass=klass,term=term).order_by('id').count() < 1:
                    varerr = 'NO TOPICS ENTERED FOR  ' + subject +', '+ term + ' term'
                    return render_to_response('lesson/subtajax.html',{'varerr':varerr,'subject':subject })
                else:                       
                    for j in sott:
                        k = tblcontents.objects.filter(topic=j)
                        cont = {'topic':j, 'content':k}
                        sublist.append(cont)
                return render_to_response('lesson/subtajax.html',{'subject':subject,'term':term,'sublist':sublist,'klass':klass,})
    else:
        return HttpResponseRedirect('/login/')

def deletecon(request, sid):
    if "userid" in request.session:
        varuser = request.session['userid']
        getdetails= tblcontents.objects.get(id = sid)
        ir=tblobjectives.objects.filter(content =getdetails)
        eva = tblevaluation.objects.filter(content=getdetails)
        for c in ir and eva:
            c.delete()
        getdetails.delete()
        return HttpResponseRedirect('/lesson/setup_sub/')
    else:
        return HttpResponseRedirect('/login/')


def setobj(request):
    if "userid" in request.session:
        varuser = request.session['userid']
        varerr = ""
        form = setobjForm
        return render_to_response('lesson/subobj.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')


def filobj(request):
    if "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varerr = ""
                varuser = request.session['userid']
                post = request.POST.copy()
                accode=post['userid']
                state=accode
                sublist=[]
                oblist=[]
                subject,klass,term=accode.split(':')
                sott = tbltopic.objects.filter(subject=subject,klass=klass,term=term).order_by('id')
#********** obtain topic id ***********************#
                if tbltopic.objects.filter(subject=subject,klass=klass,term=term).order_by('id').count() < 1:
                    varerr = 'NO TOPICS ENTERED FOR  ' + klass+ ' '+ term + '  term'+ ' '+ subject
                    return render_to_response('lesson/subtajax.html',{'varerr':varerr,'subject':subject })
                else:                       
                    for j in sott:
                        k = tblcontents.objects.filter(topic =j)
                        for h in k:
                            ob = tblobjectives.objects.filter(content=h)
                            obj ={'objectives':ob,'content':h}
                            oblist.append(obj)


                return render_to_response('lesson/subobjajax.html',{'subject':subject,'term':term,'sublist':sublist,'klass':klass,'oblist':oblist})
    else:
        return HttpResponseRedirect('/login/')

def deleteobj(request, sid):
    if "userid" in request.session:
        varuser = request.session['userid']
        getdetails= tblobjectives.objects.get(id = sid)
        ir=tblteachersActivities.objects.filter(objectives =getdetails)
        for c in ir:
            c.delete()
        getdetails.delete()
        return HttpResponseRedirect('/lesson/set_up/obj/')
    else:
        return HttpResponseRedirect('/login/')
 

def setresource(request):
    if "userid" in request.session:
        varuser = request.session['userid']
        varerr = ""
        form = setobjForm
        return render_to_response('lesson/setir.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')




def resajax(request):
    if "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varerr = ""
                varuser = request.session['userid']
                post = request.POST.copy()
                accode=post['userid']
                state=accode
                sublist=[]
                subject,klass,term=accode.split(':')
                sott = tbltopic.objects.filter(subject=subject,klass=klass,term=term).order_by('id')
#********** obtain topic id ***********************#
                if tbltopic.objects.filter(subject=subject,klass=klass,term=term).order_by('id').count() < 1:
                    varerr = 'NO TOPICS ENTERED FOR  ' + subject +', '+ term + ' term'
                    return render_to_response('lesson/subtajax.html',{'varerr':varerr,'subject':subject })
                else:                       
                    for j in sott:
                        k = tblir.objects.filter(topic =j)
                        cont = {'topic':j, 'ir':k}
                        sublist.append(cont)
                return render_to_response('lesson/irajax.html',{'subject':subject,'sublist':sublist})
    else:
        return HttpResponseRedirect('/login/')

def enterir(request):
        if  "userid" in request.session:
            if request.is_ajax():
                if request.method == 'POST':
                    varuser = request.session['userid']
                    varerr =""
                    post = request.POST.copy()
                    acccode = post['userid']
                    state=acccode
                    getdetails = tbltopic.objects.get(id = state)
                    return render_to_response('lesson/enterir.html',{'getdetails':getdetails,'state':acccode})
                else:
                    gdata = ""
                    return render_to_response('index.html',{'gdata':gdata})
            else:

                getdetails = tblcontents.objects.filter(topic=id)
                return render_to_response('lesson/entersub.html',{'gdata':getdetails})
        else:
            return HttpResponseRedirect('/login/')


def irajax(request,vid):
    if "userid" in request.session:
        varuser = request.session['userid']
        varerr = ''
        if request.method=='POST':
            ir=request.POST['ir']
            ir= ir.lower()
            ex=request.POST['examples']
            ex= ex.lower()
            tr= tbltopic.objects.get(id = vid)
            c=tblir.objects.filter(topic=tr)
            for k in c:
                if k.resource== ir:
                    return HttpResponseRedirect('/lesson/set_up/resources')
            tblir(resource=ir, example=ex,topic=tr).save()
            return HttpResponseRedirect('/lesson/set_up/resources')
    else:
        return HttpResponseRedirect('/login/')


def deleteir(request, sid):
    if "userid" in request.session:
        varuser = request.session['userid']
        getdetails= tblir.objects.get(id = sid).delete()
        #getdetails.delete()
        return HttpResponseRedirect('/lesson/set_up/resources/')
    else:
        return HttpResponseRedirect('/login/')



def tactivities(request):
    if "userid" in request.session:
        varuser = request.session['userid']
        varerr = ""
        form = setobjForm
        return render_to_response('lesson/ta.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def tajax(request):
    if "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varerr = ""
                varuser = request.session['userid']
                post = request.POST.copy()
                accode=post['userid']
                state=accode
                oblist=[]
                subject,klass,term=accode.split(':')
                sott = tbltopic.objects.filter(subject=subject,klass=klass,term=term).order_by('id')
#********** obtain topic id ***********************#
                if tbltopic.objects.filter(subject=subject,klass=klass,term=term).order_by('id').count() < 1:
                    varerr = 'NO TOPICS ENTERED FOR  ' + klass+ ' '+ term + '  term'+ ' '+ subject
                    return render_to_response('lesson/subtajax.html',{'varerr':varerr,'subject':subject })
                else:                       
                    for j in sott:
                        k = tblcontents.objects.filter(topic =j)
                        for h in k:
                            ob = tblobjectives.objects.filter(content=h)
                            for t in ob:
                                ta=tblteachersActivities.objects.filter(objectives=t)
                                obj ={'ta':ta,'obj':t}
                                oblist.append(obj)
                return render_to_response('lesson/taview.html',{'subject':subject,'oblist':oblist})
                
    else:
        return HttpResponseRedirect('/login/')


def entajax(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':                
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
                getdetails = tblobjectives.objects.get(id = state)
                return render_to_response('lesson/entajax.html',{'getdetails':getdetails,'state':acccode})
    else:
        return HttpResponseRedirect('/login/')


def saveta(request,vid):
    if "userid" in request.session:
        varuser = request.session['userid']
        varerr = ''
        if request.method=='POST':
            ta=request.POST['ta']
            ta= ta.lower()
            tr= tblobjectives.objects.get(id = vid)
            c=tblteachersActivities.objects.filter(objectives=tr)
            for k in c:
                if k.teacherActivities== ta:
                    return HttpResponseRedirect('/lesson/set_up/teacher_activities/')
            tblteachersActivities(objectives=tr, teacherActivities=ta).save()
            return HttpResponseRedirect('/lesson/set_up/teacher_activities/')
    else:
        return HttpResponseRedirect('/login/')


def deleteta(request, sid):
    if "userid" in request.session:
        varuser = request.session['userid']
        getdetails= tblteachersActivities.objects.get(id = sid)
        ir=tblstudentActivities.objects.filter(teacher_activities =getdetails)
        for c in ir:
            c.delete()
        getdetails.delete()
        return HttpResponseRedirect('/lesson/set_up/teacher_activities/')
    else:
        return HttpResponseRedirect('/login/')

def sactivities(request):
    if "userid" in request.session:
        varuser = request.session['userid']
        varerr = ""
        form = setobjForm
        return render_to_response('lesson/sa.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def sajax(request):
    if "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varerr = ""
                varuser = request.session['userid']
                post = request.POST.copy()
                accode=post['userid']
                state=accode
                oblist=[]
                subject,klass,term=accode.split(':')
                sott = tbltopic.objects.filter(subject=subject,klass=klass,term=term).order_by('id')
#********** obtain topic id ***********************#
                if tbltopic.objects.filter(subject=subject,klass=klass,term=term).order_by('id').count() < 1:
                    varerr = 'NO TOPICS ENTERED FOR  ' + klass+ ' '+ term + '  term'+ ' '+ subject
                    return render_to_response('lesson/subtajax.html',{'varerr':varerr,'subject':subject })
                else:                       
                    for j in sott:
                        k = tblcontents.objects.filter(topic =j)
                        for h in k:
                            ob = tblobjectives.objects.filter(content=h)
                            for o in ob:
                                ta=tblteachersActivities.objects.filter(objectives=o)
                                for t in ta:
                                    sa = tblstudentActivities.objects.filter(teacher_activities=t)                                        
                                    obj ={'ta':t,'sa':sa}
                                    oblist.append(obj)
                return render_to_response('lesson/saview.html',{'subject':subject,'oblist':oblist,'term':term, 'klass':klass})
                
    else:
        return HttpResponseRedirect('/login/')

def ensajax(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':                
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state=acccode
                getdetails = tblteachersActivities.objects.get(id = state)
                return render_to_response('lesson/ensajax.html',{'getdetails':getdetails,'state':acccode})
    else:
        return HttpResponseRedirect('/login/')

def savesa(request,vid):
    if "userid" in request.session:
        varuser = request.session['userid']
        varerr = ''
        if request.method=='POST':
            sa=request.POST['sa']
            sa= sa.lower()
            tr= tblteachersActivities.objects.get(id = vid)
            c=tblstudentActivities.objects.filter(teacher_activities=tr)
            for k in c:
                if k.studentActivities== sa:
                    return HttpResponseRedirect('/lesson/set_up/teacher_activities/')
            tblstudentActivities(teacher_activities=tr, studentActivities=sa).save()
            return HttpResponseRedirect('/lesson/set_up/students_activities/')
    else:
        return HttpResponseRedirect('/login/')

def deletesa(request, sid):
    if "userid" in request.session:
        varuser = request.session['userid']
        getdetails= tblstudentActivities.objects.get(id = sid)
        getdetails.delete()
        return HttpResponseRedirect('/lesson/set_up/students_activities/')
    else:
        return HttpResponseRedirect('/login/')


def seteva(request):
    if "userid" in request.session:
        varuser = request.session['userid']
        varerr = ""
        form = setobjForm
        return render_to_response('lesson/eva.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def fileva(request):
    if "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varerr = ""
                varuser = request.session['userid']
                post = request.POST.copy()
                accode=post['userid']
                state=accode
                sublist=[]
                oblist=[]
                subject,klass,term=accode.split(':')
                sott = tbltopic.objects.filter(subject=subject,klass=klass,term=term).order_by('id')
#********** obtain topic id ***********************#
                if tbltopic.objects.filter(subject=subject,klass=klass,term=term).order_by('id').count() < 1:
                    varerr = 'NO TOPICS ENTERED FOR  ' + klass+ ' '+ term + '  term'+ ' '+ subject
                    return render_to_response('lesson/subtajax.html',{'varerr':varerr,'subject':subject })
                else:                       
                    for j in sott:
                        k = tblcontents.objects.filter(topic =j)
                        for h in k:
                            eva = tblevaluation.objects.filter(content=h)
                            obj ={'eva':eva,'content':h}
                            oblist.append(obj)
                return render_to_response('lesson/evaajax.html',{'subject':subject,'oblist':oblist})
    else:
        return HttpResponseRedirect('/login/')

def eva(request):
        if  "userid" in request.session:
            if request.is_ajax():
                if request.method == 'POST':
                    varuser = request.session['userid']
                    varerr =""
                    post = request.POST.copy()
                    acccode = post['userid']
                    state=acccode
                    getdetails = tblcontents.objects.get(id = state)
                    return render_to_response('lesson/entereva.html',{'getdetails':getdetails,'state':acccode})
        else:
            return HttpResponseRedirect('/login/')

def entereva(request,vid):
    if "userid" in request.session:
        varuser = request.session['userid']
        varerr = ''
        if request.method=='POST':
            eva=request.POST['eva']
            eva= eva.lower()
            tr= tblcontents.objects.get(id = vid)
            c=tblevaluation.objects.filter(content=tr)
            for k in c:
                if k.evaluation== eva:
                    return HttpResponseRedirect('/lesson/set_up/evaluation')
            tblevaluation(evaluation=eva, content=tr).save()
            return HttpResponseRedirect('/lesson/set_up/evaluation')
    else:
        return HttpResponseRedirect('/login/') 


def deleteva(request, sid):
    if "userid" in request.session:
        varuser = request.session['userid']
        getdetails= tblevaluation.objects.get(id = sid)
        getdetails.delete()
        return HttpResponseRedirect('/lesson/set_up/evaluation/')
    else:
        return HttpResponseRedirect('/login/')


def setupmynote(request):
    if  "userid" in request.session:
        form = mynotes()
        return render_to_response('lesson/lessonnote.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def notajax(request):
    if "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varerr = ""
                varuser = request.session['userid']
                post = request.POST.copy()
                accode = post['userid']
                subject,klass,term = accode.split(':') #order must follow that in the autopost script in html
                sett = tbltopic.objects.filter(klass = klass,term = term, subject = subject).order_by('id')
                myintr=[]
                for j in sett:
                    idy=j.id
                    sub=j.subject
                    topic=j.topic
                    j=str(j.lessonnote)
                    j=j.split('/')[-1]
                    j=j.split('.')[0]
                    intr ={'file':j,'sub':sub,'topic':topic,'id':idy,'klass':klass,'term':term}#,'klass':sett.klass,'term':sett.term,'subject':sett.subject}
                    myintr.append(intr)

                return render_to_response('lesson/notajax.html',{'myintr':myintr,'term':term,'klass':klass,'subject':subject})
                    # {'sett':sett,
                    # 'varerr':varerr, 
                    # 
                    # 
                    # 'j':j,
                    # 'myintr':myintr,
                    # 'subject':subject}
                    # )
    else:
        return HttpResponseRedirect('/login/')

def uploadnote(request, sid):
    if "userid" in request.session:
        varuser = request.session['userid']  
        try:
            if request.method=='POST' and request.FILES['datafile']:          
                datafile= request.FILES['datafile']                 
                getdetails= tbltopic.objects.get(id = sid)
                object_reference= getdetails.lessonnote
                object_name = os.path.basename(object_reference.file.name)                   
                getdetails.lessonnote=datafile
                getdetails.save()
                return render_to_response('lesson/lessonnote.html',{'form':form})
        except:
            return HttpResponseRedirect('/lesson/note/')
    else:
        return HttpResponseRedirect('/login/')


def viewnote(request, vid):
    if 'userid' in request.session:            
            note = tbltopic.objects.get(id = vid)
            object_name= note.lessonnote
            filename = os.path.basename(object_name.file.name)
            response = HttpResponse(object_name.file)
            response['Content-Disposition'] = 'attachment, filename=%s' % filename
            return response 

            #render_to_response('lesson/wa.html',{'form':mynotes,'varerr':filename})
            #note = "C:/Windows/www/SchApp/myproject/static/notes/invoice.docx"
           # filename = note #'<path to your file>'
           # data = open(filename,'rb').read()
           # response = HttpResponse(data, content_type='application/ms-word')
           # response['Content-Disposition'] = 'attachment, filename=myname.docx'
           # return response
    else:
        return HttpResponseRedirect('/login/')

def reviewnote(request, vid):
    if 'userid' in request.session:            
            note = tbltopic.objects.get(id = vid)
            object_name= note.lessonnote
            filename = os.path.basename(object_name.file.name)
            response = HttpResponse(object_name.file)
            response['Content-Disposition'] = 'attachment, filename=%s' % filename
            return response 
    else:
        return HttpResponseRedirect('/login/')

def lesscount(request):
    if "userid" in request.session:
        varuser = request.session['userid']
        varerr=''
        if request.method=='POST':
            form=waform(request.POST)
            if form.is_valid():
                subject= form.cleaned_data['subject']
                klass = form.cleaned_data['klass']
                wa= form.cleaned_data['wa']
                try:                    
                     varwa = tblwa.objects.get(subject=subject,klass= klass)
                     varwa= varwa.wa
                     if varwa :
                        varerr ='Click the edit button to change value'
                     else:
                        if wa.isnumeric():
                            varwa= wa
                            varwa.save()
                            varerr= "WA entered successfully"
                except:
                    if wa.isnumeric():
                        tblwa(subject=subject,klass= klass,wa=wa).save()
            else:
                varerr= "enter a valid figure for W.A"
        else:
            form = waform()
        return render_to_response('lesson/wa.html',{'form':form,'varerr':varerr})
    else:
        HttpResponseRedirect('/login/')

def enterwa(request):
        if  "userid" in request.session:
            if request.is_ajax():
                if request.method == 'POST':
                    varuser = request.session['userid']
                    varerr =""
                    post = request.POST.copy()
                    acccode = post['userid']
                    state=acccode
                    getdetails = tblwa.objects.get(id = state)
                    return render_to_response('lesson/enterwa.html',{'getdetails':getdetails,'state':acccode})
        else:
            return HttpResponseRedirect('/login/')

def editwa(request,vid):
    if "userid" in request.session:
        varuser = request.session['userid']
        if request.method=='POST':
            wa=request.POST['wa']
            if wa == '':
                pass
            else:
                if wa.isnumeric():
                    tr=tblwa.objects.get(id = vid)
                    tr.wa=wa
                    tr.save()
            return HttpResponseRedirect('/lesson/set_up/lesson_count')
    else:
        return HttpResponseRedirect('/login/') 

def wajax(request):
    if "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varerr = ""
                varuser = request.session['userid']
                post = request.POST.copy()
                accode = post['userid']
                subject,klass = accode.split(':') #order must follow that in the autopost script in html
                sett = tblwa.objects.filter(klass = klass, subject = subject)
                return render_to_response('lesson/wajax.html',{'sett':sett,'varerr':varerr,'klass':klass,'subject':subject})
            else:
                sett = ""
            return render_to_response ('lesson/wajax.html',{'sett':sett})
        else:
            sett = ""
            return render_to_response ('lesson/wajax.html',{'sett':sett})
    else:
        return HttpResponseRedirect('/login/')


def setupmyplan(request):
    if  "userid" in request.session:
        if request.method == 'POST':
            form = lessonplanform(request.POST)
            if form.is_valid():
                klass = request.POST['klass']
                session = request.POST['session']
                term = request.POST['term']
                subject= request.POST['subject']
                top=tbltopic.objects.filter( klass=klass, subject=subject,term=term).order_by('id')
                cont=0
                ct=0
                for t in top:
                    cont = tblcontents.objects.filter(topic=t).count()
                    ct=cont+ct
                wl = tblwa.objects.get(klass=klass,subject=subject)
                wl=wl.wa
                tb = tblcalendar.objects.get(session=session, term=term)
                tb=str(tb.end)

                return render_to_response('lesson/lessonp.html',{'form':form,'cont':tb})
        else:
            form = lessonplanform()
        return render_to_response('lesson/lessonp.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def examquests(request):
    if  "userid" in request.session:
        try:
            if request.method=='POST' and request.FILES['datafile']:
                form = mynotes(request.POST)
                session=request.POST['session']
                klass=request.POST['klass']
                term=request.POST['term']
                subject=request.POST['subject']
                datafile=request.FILES['datafile']

                quest=int(tblquest.objects.filter(session=session,
                    klass=klass,
                    term=term,
                    subject=subject).count())
                if quest==1:
                    pass
                else:
                    quest=tblquest(question=datafile,session=session,klass=klass,term=term,subject=subject).save()
            else:      
                form = mynotes()
            return render_to_response('lesson/quest.html',{'form':form})
        except:
            return HttpResponseRedirect('/lesson/ExamQuest/')
    else:
        return HttpResponseRedirect('/login/')

def getexamquest(request):
    if "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                post = request.POST.copy()
                accode = post['userid']
                session,subject,klass,term = accode.split(':') #order must follow that in the autopost script in html
                quest = tblquest.objects.filter(session=session,klass=klass,term=term,subject=subject)

                myintr=[]
                for j in quest:
                    sub=j.subject
                    session=j.session
                    j=str(j.question)
                    j=j.split('/')[-1]
                    j=j.split('.')[0]
                    intr ={'file':j,'sub':sub,'session':session,'klass':klass,'term':term}#,'klass':sett.klass,'term':sett.term,'subject':sett.subject}
                    myintr.append(intr)               

                return render_to_response('lesson/questajax.html', 
                    {'myintr':myintr,
                    # 'sett':quest,
                    # 'term':term,
                    # 'klass':klass,
                    # 'session':session,
                    # 'subject':subject
                    }
                    )
    else:
        return HttpResponseRedirect('/login/')
        
def downquest(request, vid):
    if 'userid' in request.session:            
            note = tblquest.objects.get(id = vid)
            object_ref= note.question
            filename = os.path.basename(object_ref.file.name)
            response = HttpResponse(object_ref.file)
            response['Content-Disposition'] = 'attachment, filename=%s' % filename
            return response 
    else:
        return HttpResponseRedirect('/login/')

def upquest(request, sid):
    if "userid" in request.session:
        varuser = request.session['userid']
        try:
            if request.method=='POST' and request.FILES['datafile']:              
                datafile= request.FILES['datafile']                 
                getdetails= tblquest.objects.get(id = sid)
                object_reference= getdetails.question                 
                getdetails.question=datafile
                getdetails.save()
                return render_to_response('lesson/questajax.html',{'form':form})
        except:
            return HttpResponseRedirect('/lesson/ExamQuest/')
    else:
        return HttpResponseRedirect('/login/')

def upquestnew(request):
    if 'userid' in request.session:
        varuser = request.session['userid']              
        if request.method=='POST':                  
          #  try:
                if request.FILES['datafile']:
                    datafile=request.FILES['datafile']
                    quest = tblquest(session= session,klass=  klass, term=term, subject=subject,question=datafile).save()
                    return HttpResponseRedirect('/lesson/ExamQuest/')
         #   except:
          #      return HttpResponseRedirect('/lesson/note/')
    else:
        return HttpResponseRedirect('/login/')


def json_view(func):
    def wrap(req, *args, **kwargs):
        resp = func(req, *args, **kwargs)
        if isinstance(resp, HttpResponse):
            return resp
        return HttpResponse(json.dumps(resp), mimetype="application/json")

    return wrap
