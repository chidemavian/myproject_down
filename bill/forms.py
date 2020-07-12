from django import forms
from myproject.setup.models import *
from myproject.bill.models import *
from myproject.sysadmin.models import *
from myproject.student.models import *

def sessi():
    if billsession.objects.all().count() == 0:
       currse = currentsession.objects.get(id = 1)
    else:
       currse = billsession.objects.get(id = 1)
    return currse

class expensesForm(forms.Form):
    expenses = forms.CharField(label="Bill Name",max_length= 150,widget=forms.TextInput(attrs={'size':'35'}))

class billForm(forms.Form):
    klass = forms.ChoiceField(label= 'Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    desc = forms.ChoiceField(label= 'Bill Description',choices = [(c.name, c.name) for c in tblexpenses.objects.all()])
    billamount = forms.DecimalField( label='Bill Amount',decimal_places= 2,required=True,max_digits= 15)
    acccode = forms.CharField(label='G/L Account Code',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':35}))
    dayboarding = forms.ChoiceField(label='Day/Boarding',choices= (('Day', 'Day'), ('Boarding', 'Boarding')))
    term = forms.ChoiceField(label='Term',choices=[(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')])
   # term = forms.ChoiceField(label='Term',choices=(('First', 'First'), ('Second', 'Second'), ('Third', 'Third')))
    def __init__(self, *args):
        super(billForm, self).__init__(*args)
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['desc'].choices = [(c.name, c.name) for c in tblexpenses.objects.all()]
        self.fields['desc'].initial = tblexpenses.objects.all()
        self.fields['acccode'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]

class additionalbillform(forms.Form):
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':10}),initial=sessi)
    admissionno = forms.CharField(label='Admission Number',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':15,'readonly':'readonly'}))
    name = forms.CharField(label='Student Name',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':35}))
    klass = forms.CharField(label='Class',max_length= 20,required=True,widget= forms.TextInput(attrs ={'size':10,'readonly':'readonly'}))
    arm = forms.CharField(label='Arm',max_length= 20,required=True,widget= forms.TextInput(attrs ={'size':10,'readonly':'readonly'}))
    term = forms.ChoiceField(label='Term',choices=[(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')])
    #term = forms.ChoiceField(label='Term',choices=(('First', 'First'), ('Second', 'Second'), ('Third', 'Third')))
    billamount = forms.DecimalField( label='Bill Amount',decimal_places= 2,required=True,max_digits= 15)
    desc = forms.ChoiceField(label= 'Bill Description',choices = [(c.name, c.name) for c in tblexpenses.objects.all()])
    acccode = forms.CharField(label='G/L Account Code',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':35}))

    def __init__(self, *args):
        super(additionalbillform, self).__init__(*args)
        self.fields['desc'].choices = [(c.name, c.name) for c in tblexpenses.objects.all()]
        self.fields['desc'].initial = tblexpenses.objects.all()
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['admissionno'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['name'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['billamount'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['acccode'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]

class printbillform(forms.Form):
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':10}),initial=sessi)
    name = forms.ChoiceField(label='Student Name',choices = [(c.fullname, c.fullname) for c in Student.objects.all()])
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    term = forms.ChoiceField(label='Term',choices=(('First', 'First'), ('Second', 'Second'), ('Third', 'Third')))
    excelfile = forms.BooleanField(label='By Class',required=False)
    pdffile = forms.BooleanField(label='PDF',required=False)

    def __init__(self, *args):
        super(printbillform, self).__init__(*args)
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['name'].choices = [(c.fullname, c.fullname) for c in Student.objects.all()]
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]

class billscheduleform(forms.Form):
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':10}),initial=sessi)
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    term = forms.ChoiceField(label='Term',choices=(('First', 'First'), ('Second', 'Second'), ('Third', 'Third')))
    def __init__(self, *args):
        super(billscheduleform, self).__init__(*args)
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]

class printoldbillform(forms.Form):
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':10}),initial=sessi)
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    term = forms.ChoiceField(label='Term',choices=(('First', 'First'), ('Second', 'Second'), ('Third', 'Third')))
    studentname = forms.ChoiceField(choices = [(c.fullname, c.fullname) for c in Student.objects.all()], label="Student's Name")
    def __init__(self, *args):
        super(printoldbillform, self).__init__(*args)
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['studentname'].choices = [(c.fullname, c.fullname) for c in Student.objects.all()]
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'
