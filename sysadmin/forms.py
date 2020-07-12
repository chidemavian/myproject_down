from django import forms
from myproject.sysadmin.models import *
from myproject.student.models import *
from myproject.setup.models import *
from myproject.bill.models import *


cat_choices=(('JS', 'JS'), ('SS', 'SS'))
filterss=(('ACTIVE', 'ACTIVE'), ('INACTIVE', 'SS'))
cas= (('Mid Term', 'Mid Term'), ('End Term', 'End term'))
ta= ( ('First', 'First'), ('Second', 'Second'), ('Third', 'Third'))
def sess():
    return currentsession.objects.get(id = 1)


if currentsession.objects.all().count()==0:
    currentsession(session='2018/2019').save()
if billsession.objects.all().count()==0:
    billsession(session='2018/2019').save()

currse = currentsession.objects.get(id = 1)
cur = billsession.objects.get(id = 1)

x,y = str(currse).split('/')
x,y = str(cur).split('/')
k = int(x) + 1
n = int(y) + 1
ok = int(x) - 1
on = int(y) - 1
newsession = str(k)+'/'+str(n)
newsession1 = str(k)+'/'+str(n)
oldsession = str(ok)+'/'+str(on)
allsub = []
sdic ={}
vsub = Subject.objects.all()
for j in vsub:
    sj = {j.subject:j.subject}
    sdic.update(sj)
slist = sdic.keys()

class loginform(forms.Form):
      username = forms.CharField(label="UserName",required = True)
      password = forms.CharField(label="Password",widget=forms.PasswordInput,required = True)

      def __init__(self, *args, **kwargs):
         super(loginform, self).__init__(*args, **kwargs)
         self.fields['username'].widget.attrs['class'] = 'loginTxtbox'
         self.fields['password'].widget.attrs['class'] = 'loginTxtbox'




class dateform(forms.Form):
    mydate = forms.CharField(label = "Date",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))
    # birth_date = forms.CharField(max_length=12, label='Date Of Birth', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    def __init__(self, *args):
        super(dateform, self).__init__(*args)
        self.fields['mydate'].widget.attrs['class'] = 'loginTxtbox'




class resetuserform(forms.Form):
    username = forms.CharField(label = "Username",max_length = 20,required = True)
    def __init__(self, *args, **kwargs):
        super(resetuserform, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'loginTxtbox'

class useraccform(forms.Form):
    username = forms.CharField(required = True)
    password = forms.CharField("Password",widget=forms.PasswordInput,required = True)
    def __init__(self, *args, **kwargs):
        super(useraccform, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['password'].widget.attrs['class'] = 'loginTxtbox'

class changepassform(forms.Form):
    oldpassword = forms.CharField("Password",widget=forms.PasswordInput,required = True)
    password = forms.CharField("Password",widget=forms.PasswordInput,required = True)
    password2 = forms.CharField("Password",widget=forms.PasswordInput,required = True)
    def __init__(self, *args, **kwargs):
        super(changepassform, self).__init__(*args, **kwargs)
        self.fields['oldpassword'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['password'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['password2'].widget.attrs['class'] = 'loginTxtbox'

class userloginform(forms.Form):
    email = forms.EmailField(label="Enter Your E-mail",required=True,widget = forms.TextInput(attrs={'size':'40'}))
    def __init__(self, *args, **kwargs):
        super(userloginform, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'loginTxtbox'

class creatuserform(forms.Form):
    username = forms.CharField(label = "Username",max_length = 20,required = True,widget = forms.TextInput(attrs={'size':'40'}))
    staffname = forms.CharField(label = "Full Name",max_length = 220,required = True,widget = forms.TextInput(attrs={'size':'40'}))
    # Filters = forms.ChoiceField(label= 'Sort By', choices=( ('-----', '-----'), ('ACTIVE', 'ACTIVE'), ('INACTIVE', 'INACTIVE')))


    def __init__(self, *args, **kwargs):
        super(creatuserform, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['staffname'].widget.attrs['class'] = 'loginTxtbox'

class classteacher(forms.Form):
    teachername = forms.CharField(label = "Teacher Name",max_length = 120,required = True,widget = forms.TextInput(attrs={'size':'13'}))
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    arm = forms.ChoiceField(label= 'Arm', choices = [(a.arm, a.arm) for a in Arm.objects.all()])

    def __init__(self, *args, **kwargs):
        super(classteacher, self).__init__(*args, **kwargs)
        self.fields['teachername'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['arm'].choices = [(a.arm, a.arm) for a in Arm.objects.all()]
        self.fields['arm'].initial = Arm.objects.all()



class autorunform(forms.Form):
    ca = forms.ChoiceField(label= 'Run Auto comment for', choices=cas)
    session = forms.CharField(label= 'Session', max_length=13,initial=sess(),widget = forms.TextInput(attrs={'size':'10','readonly':'readonly'}))
    term = forms.ChoiceField(label='Term',choices= ta)
    def __init__(self, *args):
        super(autorunform, self).__init__(*args)
        self.fields['ca'].choices=cas
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'


class cfform(forms.Form):
    date = forms.CharField(label = "Date",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))
    session = forms.CharField(label= 'Session', max_length=13,initial=sess(),widget = forms.TextInput(attrs={'size':'10','readonly':'readonly'}))
    term = forms.ChoiceField(label='Term',choices=[(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')])
   
    def __init__(self, *args):
        super(cfform, self).__init__(*args)
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['date'].widget.attrs['class'] = 'loginTxtbox'
        # self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]

class autocomform(forms.Form):
    comment = forms.CharField(label = "Comment",max_length = 5000,required = True)
    krang = forms.ChoiceField(label='Range',choices = [(c.grade, c.grade) for c in gradingsys.objects.all()])
    category = forms.ChoiceField(label= 'Category', choices = cat_choices)

    def __init__(self, *args, **kwargs):
        super(autocomform, self).__init__(*args, **kwargs)
        self.fields['krang'].choices = [(c.grade, c.grade) for c in gradingsys.objects.all()]
        self.fields['krang'].initial = Class.objects.all()
        self.fields['category'].choices = cat_choices
       # self.fields['category'].initial = Arm.objects.all()

class cocoform(forms.Form):
    teachername = forms.CharField(label = "Teacher Name",max_length = 120,required = True,widget = forms.TextInput(attrs={'size':'23'}))
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])

    def __init__(self, *args, **kwargs):
        super(cocoform, self).__init__(*args, **kwargs)
        self.fields['teachername'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()

class suteacher(forms.Form):
    teachername = forms.CharField(label = "Teacher Name",max_length = 120,required = True,widget = forms.TextInput(attrs={'size':'12'}))
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    arm = forms.ChoiceField(label= 'Arm', choices = [(a.arm, a.arm) for a in Arm.objects.all()])
    subclass = forms.ChoiceField(label = 'Subclass')
    subject = forms.ChoiceField(label= 'Subject', choices = [(a,a) for a in slist])

    def __init__(self, *args, **kwargs):
        super(suteacher, self).__init__(*args, **kwargs)
        self.fields['teachername'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['arm'].choices = [(a.arm, a.arm) for a in Arm.objects.all()]
        self.fields['arm'].initial = Arm.objects.all()
        self.fields['subject'].choices = [(a,a) for a in slist]
        self.fields['subclass'].choices=[(a.category, a.category) for a in Subject.objects.all()]


class grpteacher(forms.Form):
    teachername = forms.CharField(label = "Teacher Name",max_length = 120,required = True,widget = forms.TextInput(attrs={'size':'12'}))
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    grp = forms.ChoiceField(label= 'Subject group', choices = [(a.subject_group, a.subject_group) for a in Subject_group.objects.all()])
    subclass = forms.ChoiceField(label = 'Subclass')
    subject = forms.ChoiceField(label= 'Subject', choices = [(a,a) for a in slist])

    def __init__(self, *args, **kwargs):
        super(grpteacher, self).__init__(*args, **kwargs)
        self.fields['teachername'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['grp'].choices = [(a.subject_group, a.subject_group) for a in Subject_group.objects.all()]
        self.fields['grp'].initial = Subject_group.objects.all()
        self.fields['subject'].choices = [(a,a) for a in slist]
        self.fields['subclass'].choices=[(a.category, a.category) for a in Subject.objects.all()]


class principalform(forms.Form):
    teachername = forms.CharField(label = "Teacher Name",max_length = 120,required = True,widget = forms.TextInput(attrs={'size':'25'}))
    def __init__(self, *args, **kwargs):
        super(principalform, self).__init__(*args, **kwargs)
        self.fields['teachername'].widget.attrs['class'] = 'loginTxtbox'

class unlockform(forms.Form):
    pin = forms.CharField(label = " Enter PIN",max_length = 12,widget= forms.PasswordInput(attrs ={'size':'12'}))
    def __init__(self, *args):
        super(unlockform, self).__init__(*args)
        self.fields['pin'].widget.attrs['class'] = 'loginTxtbox'

class paybillform(forms.Form):
    year = forms.IntegerField(label = " Enters Year",min_value=2000,max_value=9999,widget= forms.TextInput(attrs ={'size':'12'}))
    def __init__(self, *args):
        super(paybillform, self).__init__(*args)
        self.fields['year'].widget.attrs['class'] = 'loginTxtbox'

class teacherenableform(forms.Form):
    term = forms.ChoiceField(label='Term',choices=( ('First', 'First'), ('Second', 'Second'), ('Third', 'Third')))
    status = forms.ChoiceField(label='Status',choices=( ('ACTIVE', 'ACTIVE'), ('INACTIVE', 'INACTIVE')))

class reportsheetform(forms.Form):
    report = forms.ChoiceField(label='Term',choices = [(a.reportsheet, a.reportsheet) for a in tblreportsheet.objects.all()])
    status = forms.ChoiceField(label='Status',choices= ( ('ACTIVE', 'ACTIVE'), ('INACTIVE', 'INACTIVE')))




class promotion_form(forms.Form):
    oldclass = forms.ChoiceField(label= 'Admitted Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    newclass = forms.ChoiceField(label= 'Admitted Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    session = forms.CharField(label= 'Session', max_length=13,initial=sess(),widget = forms.TextInput(attrs={'size':'10','readonly':'readonly'}))
    subclass = forms.ChoiceField(label= 'SubClass',choices=(('---', '---'),('Nursery', 'Nursery'),('Primary', 'Primary'), ('JS', 'JS')))
    def __init__(self, *args):
        super(promotion_form, self).__init__(*args)
        self.fields['oldclass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['newclass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['oldclass'].initial = Class.objects.all()
        self.fields['newclass'].initial = Class.objects.all()
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'

class calendar_form(forms.Form):
    session = forms.CharField(label= 'Current Session', max_length=25,initial=cur,widget = forms.TextInput(attrs={'size':'12','readonly':'readonly'}))
    sessionnew = forms.CharField(label= 'Next Session', max_length=25,initial=newsession1,widget = forms.TextInput(attrs={'size':'12','readonly':'readonly'}))
    def __init__(self, *args):
        super(calendar_form, self).__init__(*args)
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['sessionnew'].widget.attrs['class'] = 'loginTxtbox'

#********************for Online Upload *************
class online_result_form(forms.Form):
    term = forms.ChoiceField(label='Term',choices=[(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')])
    newclass = forms.ChoiceField(label= 'Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    session = forms.CharField(label= 'Session', max_length=25,initial=currse,widget = forms.TextInput(attrs={'size':'12'}))
    def __init__(self, *args):
        super(online_result_form, self).__init__(*args)
        self.fields['newclass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['newclass'].initial = Class.objects.all()
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'
#*************************************************************************************
class statement_form(forms.Form):
    session = forms.CharField(label= 'Session', max_length=25,initial=sess(),widget = forms.TextInput(attrs={'size':'25','readonly':'readonly'}))
    def __init__(self, *args):
        super(statement_form, self).__init__(*args)
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'
  

#*******************************************SUBJECT REPORT***********************************
class subject_report_form(forms.Form):
    term = forms.ChoiceField(label='Term',choices=[(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')])
    subject = forms.ChoiceField(label= 'Subject', choices = [(a,a) for a in slist])
    session = forms.CharField(label= 'Session', max_length=25,initial=sess(),widget = forms.TextInput(attrs={'size':'12','readonly':'readonly'}))
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    subclass = forms.ChoiceField(label = 'Subclass')
    def __init__(self, *args):
        super(subject_report_form, self).__init__(*args)
        self.fields['subject'].choices = [(a,a) for a in slist]
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]
        self.fields['subclass'].choices=[(a.category, a.category) for a in Subject.objects.all()]
