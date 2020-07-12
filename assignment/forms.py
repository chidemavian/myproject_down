from myproject.sysadmin.models import *
from django import forms
from myproject.setup.models import *

def sess():
    return currentsession.objects.get(id = 1)
currse = currentsession.objects.get(id = 1)

class assignform(forms.Form):
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':'10','readonly':'readonly'}),initial=sess())
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    term = forms.ChoiceField(label='Term',choices=[(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')])
    arm = forms.ChoiceField(label= 'Arm', choices = [(a.arm, a.arm) for a in Arm.objects.all()])
    subject = forms.ChoiceField(label= 'Subject', choices = [(a.subject, a.subject) for a in Subject.objects.all()])
    mydate = forms.CharField(label = "Date",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))

    def __init__(self, *args):
        super(assignform, self).__init__(*args)
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['arm'].choices = [(a.arm, a.arm) for a in Arm.objects.all()]
        self.fields['subject'].choices = [(a.subject, a.subject) for a in Subject.objects.all()]
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]
        self.fields['mydate'].widget.attrs['class'] = 'loginTxtbox'