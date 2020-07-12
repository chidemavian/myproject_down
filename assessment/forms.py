
from django import forms
from myproject.setup.models import *
from myproject.sysadmin.models import *
from myproject.student.models import *
ca_choices= (('----','-----'),('1st CA', '1st CA'),('2nd CA', '2nd CA'),('Half Term', 'Half Term'))

# cacom_choices= (('Mid term', 'Mid term'),('End term', 'End term'))


def sess():
    return currentsession.objects.get(id = 1)
currse = currentsession.objects.get(id = 1)


class cfform(forms.Form):
    term = forms.ChoiceField(label='Term',choices=[(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')])

    def __init__(self, *args):
        super(cfform, self).__init__(*args)
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]
        self.fields['term'].initial = tblterm.objects.filter(status = 'ACTIVE')


class stuform(forms.Form):#note that is this CA term that need to come from back end
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':'10','readonly':'readonly'}),initial=sess)
    term = forms.ChoiceField(label='Term',choices=[(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')])

    def __init__(self, *args):
        super(stuform, self).__init__(*args)
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]
        self.fields['term'].initial = tblterm.objects.filter(status = 'ACTIVE')



class casform(forms.Form):#note that is this CA term that need to come from back end
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':'10','readonly':'readonly'}),initial=sess())
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    term = forms.ChoiceField(label='Term',choices=[(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')])
    arm = forms.ChoiceField(label= 'Arm', choices = [(a.arm, a.arm) for a in Arm.objects.all()])
    subject = forms.ChoiceField(label= 'Subject', choices = [(a.subject, a.subject) for a in Subject.objects.all()])
    checkbox = forms.BooleanField(label='Download In PDF',required=False)

    def __init__(self, *args):
        super(casform, self).__init__(*args)
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['arm'].choices = [(a.arm, a.arm) for a in Arm.objects.all()]
        self.fields['arm'].initial = Arm.objects.all()
        self.fields['subject'].choices = [(a.subject, a.subject) for a in Subject.objects.all()]
        self.fields['subject'].initial = Subject.objects.all()
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]
        self.fields['term'].initial = tblterm.objects.filter(status = 'ACTIVE')

class caform(forms.Form):#note that is this CA term that need to come from back end
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':'10','readonly':'readonly'}),initial=sess())
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    term = forms.ChoiceField(label='Term',choices=[(a.term, a.term) for a in tblterm.objects.all()])
    arm = forms.ChoiceField(label= 'Arm', choices = [(a.arm, a.arm) for a in Arm.objects.all()])
    subject = forms.ChoiceField(label= 'Subject', choices = [(a.subject, a.subject) for a in Subject.objects.all()])
    reporttype = forms.ChoiceField(label= 'Type', choices = [(r.reportsheet, r.reportsheet) for r in tblreportsheet.objects.filter(status = 'ACTIVE')])

    def __init__(self, *args):
        super(caform, self).__init__(*args)
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['arm'].choices = [(a.arm, a.arm) for a in Arm.objects.all()]
        self.fields['arm'].initial = Arm.objects.all()
        self.fields['subject'].choices = [(a.subject, a.subject) for a in Subject.objects.all()]
        self.fields['subject'].initial = Subject.objects.all()
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]
        self.fields['reporttype'].choices = [(a.reportsheet, a.reportsheet) for a in tblreportsheet.objects.filter(status = 'ACTIVE')]

class addsubjectform(forms.Form):#note that is this CA term that need to come from back end
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':'10','readonly':'readonly'}),initial=sess())
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    term = forms.ChoiceField(label='Term',choices=[(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')])
    arm = forms.ChoiceField(label= 'Arm', choices = [(a.arm, a.arm) for a in Arm.objects.all()])
    student = forms.ChoiceField(label= "Names:", choices = [(a.fullname, a.fullname) for a in Student.objects.filter(admitted_session =currse)])

    def __init__(self, *args):
        super(addsubjectform, self).__init__(*args)
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['arm'].choices = [(a.arm, a.arm) for a in Arm.objects.all()]
        self.fields['arm'].initial = Arm.objects.all()
        self.fields['student'].choices = [(a.fullname, a.fullname) for a in Student.objects.filter(admitted_session =currse)]
        self.fields['student'].initial = Student.objects.filter(admitted_session =currse)
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]
        self.fields['term'].initial = tblterm.objects.filter(status = 'ACTIVE')


class studentform(forms.Form):#note that is this CA term that need to come from back end
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':'10','readonly':'readonly'}),initial=sess())
    term = forms.ChoiceField(label='Term',choices=[(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')])
    ca = forms.ChoiceField(label='Ca',choices=(('----', '----'), ('1st Ca', '1st Ca'), ('2nd Ca', '2nd Ca')))

    def __init__(self, *args):
        super(studentform, self).__init__(*args)
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]
        self.fields['term'].initial = tblterm.objects.filter(status = 'ACTIVE')

class myform(forms.Form):#note that is this CA term that need to come from back end
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':'10','readonly':'readonly'}),initial=sess())
    term = forms.ChoiceField(label='Term',choices=[(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')])
    subject = forms.ChoiceField(label= 'Subject', choices = [(a.subject, a.subject) for a in Subject.objects.all()])

    def __init__(self, *args):
        super(myform, self).__init__(*args)
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]
        self.fields['term'].initial = tblterm.objects.filter(status = 'ACTIVE')

class mypqform(forms.Form):#note that is this CA term that need to come from back end
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':'10','readonly':'readonly'}),initial=sess())
    term = forms.ChoiceField(label='Term',choices=[(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')])
    subject = forms.ChoiceField(label= 'Subject', choices = [(a.subject, a.subject) for a in Subject.objects.all()])
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])

    def __init__(self, *args):
        super(mypqform, self).__init__(*args)
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]
        self.fields['term'].initial = tblterm.objects.filter(status = 'ACTIVE')




class reportsheetform(forms.Form):
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':'10'}),initial=sess())
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    term = forms.ChoiceField(label='Term',choices=[(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')])
    arm = forms.ChoiceField(label= 'Arm', choices = [(a.arm, a.arm) for a in Arm.objects.all()])
    def __init__(self, *args):
        super(reportsheetform, self).__init__(*args)
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['arm'].choices = [(a.arm, a.arm) for a in Arm.objects.all()]
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'

class reportsheetmidform(forms.Form):
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':'10'}),initial=sess())
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    term = forms.ChoiceField(label='Term',choices=[(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')])
    arm = forms.ChoiceField(label= 'Arm', choices = [(a.arm, a.arm) for a in Arm.objects.all()])
    ca = forms.ChoiceField(label='C.A',choices = ca_choices)
   
    def __init__(self, *args):
        super(reportsheetmidform, self).__init__(*args)
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['arm'].choices = [(a.arm, a.arm) for a in Arm.objects.all()]
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]
        self.fields['ca'].initial = Arm.objects.all()
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'


class cacomform(forms.Form):
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':'10'}),initial=sess())
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    term = forms.ChoiceField(label='Term',choices=[(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')])
    arm = forms.ChoiceField(label= 'Arm', choices = [(a.arm, a.arm) for a in Arm.objects.all()])
    ca = forms.ChoiceField(label='C.A',choices=[(a.reportsheet, a.reportsheet) for a in tblreportsheet.objects.filter(status = 'ACTIVE')])
    def __init__(self, *args):
        super(cacomform, self).__init__(*args)
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['arm'].choices = [(a.arm, a.arm) for a in Arm.objects.all()]
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]
        self.fields['ca'].choices = [(a.reportsheet, a.reportsheet) for a in tblreportsheet.objects.filter(status = 'ACTIVE')]
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'



class indreportform(forms.Form):
    session = forms.CharField(label='Session', max_length=12,widget= forms.TextInput(attrs ={'size':'15'}),initial=sess())
    Pin= forms.CharField(label='Pin',max_length= 20,widget=forms.TextInput(attrs={'size':'15'}))
    admno= forms.CharField(label='Admission No',max_length= 20,widget=forms.TextInput(attrs={'size':'15'}))
    term = forms.ChoiceField(label='Term',choices=[(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')])
    def __init__(self,*args):
        super(indreportform,self).__init__(*args)
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]
        self.fields['Pin'].widget.attrs['class'] ='loginTxtbox'
        self.fields['admno'].widget.attrs['class'] ='loginTxtbox'



class broadsheetform(forms.Form):
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':'10'}),initial=sess())
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    term = forms.ChoiceField(label='Term',choices=[(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')])
    arm = forms.ChoiceField(label= 'Arm', choices = [(a.arm, a.arm) for a in Arm.objects.all()])
    def __init__(self, *args):
        super(broadsheetform, self).__init__(*args)
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['arm'].choices = [(a.arm, a.arm) for a in Arm.objects.all()]
        self.fields['arm'].initial = Arm.objects.all()

