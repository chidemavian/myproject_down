from myproject.sysadmin.models import *
from myproject.assignment.forms import *
from django.shortcuts import render_to_response, get_object_or_404
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from myproject.assignment.models import *
import datetime
from datetime import date
today=datetime.date.today()

def choose(request):
    if 'userid' in request.session:
        varuser=request.session['userid']
        user=userprofile.objects.get(username=varuser)
        uenter=user.curriculum
        if uenter is False:
            return HttpResponseRedirect('/welcome/')
        return render_to_response('assignment/choose.html',{'varuser':varuser})

    else:
        return HttpResponseRedirect('/login/')

def assignment(request):
    if 'userid' in request.session:
        varuser=request.session['userid']
        user=userprofile.objects.get(username=varuser)
        uenter=user.curriculum
        if uenter is False:
            return HttpResponseRedirect('/welcome/')
        varerr='Class Assignment'
        if request.method =='POST':
            form = assignform(request.POST)

     # handling non-form elements  
     
            assignment= request.POST['assignment']
            comment= request.POST['comment']

            rfile=request.FILES['datafile']

            if rfile is None:

                datafile='ax/sand_and_foam.docx'
            else:
                datafile=request.FILES['datafile']

            if form.is_valid():
                session=form.cleaned_data['session']
                klass=form.cleaned_data['klass']
                arm=form.cleaned_data['arm']
                term=form.cleaned_data['term']
                subject=form.cleaned_data['subject']
                mydate=form.cleaned_data['mydate']
                caldate2 = mydate.split('-')
                transdate = date(int(caldate2[2]),int(caldate2[1]),int(caldate2[0]))

                tblassignment(teacher=varuser,
                    subject=subject,
                    klass=klass,
                    arm=arm,
                    ass_file=datafile,
                    term=term,
                    session=session,
                    posted_on=today,
                    submit_on=transdate,
                    comment=comment,
                    assignment=assignment).save()
                return render_to_response('assignment/success.html',{'form':form,'varuser':varuser})
            else:
                varerr='select appropriate date'
                return render_to_response('assignment/assign.html',{'form':form,'varuser':varuser,'varerr':varerr})

        else:
            form=assignform()
        return render_to_response('assignment/assign.html',{'form':form,'varuser':varuser,'varerr':varerr})

    else:
        return HttpResponseRedirect('/login/')

def studassign(request):
    if 'userid' in request.session:
        return render_to_response('assignment/error.html')
    else:
        return HttpResponseRedirect('/welcome/')
        
