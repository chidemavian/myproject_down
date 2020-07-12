
from django import forms
from myproject.setup.models import *
from myproject.sysadmin.models import *
from myproject.student.models import *

currse = currentsession.objects.get(id = 1)

class caform(forms.Form):
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':'10','readonly':'readonly'}),initial=currse)
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    term = forms.ChoiceField(label='Term',choices=( ('First', 'First'), ('Second', 'Second'), ('Third', 'Third')))
    arm = forms.ChoiceField(label= 'Arm', choices = [(a.arm, a.arm) for a in Arm.objects.all()])
    subject = forms.ChoiceField(label= 'Subject', choices = [(a.subject, a.subject) for a in Subject.objects.all()])

    def __init__(self, *args):
        super(caform, self).__init__(*args)
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['arm'].choices = [(a.arm, a.arm) for a in Arm.objects.all()]
        self.fields['arm'].initial = Arm.objects.all()
        self.fields['subject'].choices = [(a.subject, a.subject) for a in Subject.objects.all()]
        self.fields['subject'].initial = Subject.objects.all()
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'

class addsubjectform(forms.Form):
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':'10','readonly':'readonly'}),initial=currse)
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    term = forms.ChoiceField(label='Term',choices=( ('First', 'First'), ('Second', 'Second'), ('Third', 'Third')))
    arm = forms.ChoiceField(label= 'Arm', choices = [(a.arm, a.arm) for a in Arm.objects.all()])
    student = forms.ChoiceField(label= 'Student', choices = [(a.fullname, a.fullname) for a in Student.objects.filter(admitted_session =currse)])

    def __init__(self, *args):
        super(addsubjectform, self).__init__(*args)
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['arm'].choices = [(a.arm, a.arm) for a in Arm.objects.all()]
        self.fields['arm'].initial = Arm.objects.all()
        self.fields['student'].choices = [(a.fullname, a.fullname) for a in Student.objects.filter(admitted_session =currse)]
        self.fields['student'].initial = Student.objects.filter(admitted_session =currse)
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'

class reportsheetform(forms.Form):
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':'10'}),initial=currse)
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    term = forms.ChoiceField(label='Term',choices=(('First', 'First'), ('Second', 'Second'), ('Third', 'Third')))
    arm = forms.ChoiceField(label= 'Arm', choices = [(a.arm, a.arm) for a in Arm.objects.all()])
    pdffile = forms.BooleanField(label='Download In PDF',required=False)
    def __init__(self, *args):
        super(reportsheetform, self).__init__(*args)
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['arm'].choices = [(a.arm, a.arm) for a in Arm.objects.all()]
        self.fields['arm'].initial = Arm.objects.all()
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'

class broadsheetform(forms.Form):
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':'10'}),initial=currse)
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    term = forms.ChoiceField(label='Term',choices=(('First', 'First'), ('Second', 'Second'), ('Third', 'Third')))
    def __init__(self, *args):
        super(broadsheetform, self).__init__(*args)
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'

