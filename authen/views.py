from myproject.authen.forms import *
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from myproject.authen.models import *


def signup(request):
	if request.method=='POST':
		form = signupform(request.POST)
		if form.is_valid():
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']
			exam=form.cleaned_data['exam']
			email=form.cleaned_data['email']

			userid = userprofile.objects.filter(username=username).count()
			if userid==0:
				userprofile(username=username,email=email,password=password,exam=exam).save()
				return render_to_response('authen/success.html')

			else:		
				msg = 'username already exist'
				return HttpResponseRedirect('/authen/signup/new/')
		
		else:
			form=signupform()
			return render_to_response('authen/signup.html',{'form':form})
	
	else:
		form = signupform()
	return render_to_response('authen/signup.html',{'form':form})


def studentlogin(request):
	if request.method=='POST':
		form=loginform(request.POST)
		if form.is_valid():
			email=form.cleaned_data['email']
			password=form.cleaned_data['password']
		else:
			msg = 'enter all details'
			return render_to_response('loginstu.html')
		
		try:
			k = userprofile.objects.get(email=email,password=password)
		except:
			return HttpResponseRedirect('/login/')
		try:
			j=tblpayment.objects.get(email=email,stream='Stream 1', exam='JAMB PREP')
			
		except:
			return HttpResponseRedirect('/authen/activate/user/')

		# except:
		# 	return HttpResponseRedirect('/loginstu/')


	else:
		form=loginform()
	return render_to_response('loginstu.html',{'form':form})
		


		
def activate(request):
	if request.method=='POST':
		pass
	else:
		return render_to_response('authen/activate.html')
