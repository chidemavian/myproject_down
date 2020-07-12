
from django import forms
from myproject.setup.models import *
import os

IMPORT_FILE_TYPES = ['.xls', ]

class accsearch(forms.Form):
    accname = forms.CharField(max_length=42, label='Account Name', widget=forms.TextInput(attrs={'size': '35'}))
    def __init__(self, *args):
        super(accsearch, self).__init__(*args)
        self.fields['accname'].widget.attrs['class'] = 'loginTxtbox'

class XlsInputForm(forms.Form):
    input_excel = forms.FileField(required= True, label= u"Upload the Excel file to import to the system.")

    def clean_input_excel(self):
        input_excel = self.cleaned_data['input_excel'].name
        extension = os.path.splitext( input_excel)[1]
        if not (extension in IMPORT_FILE_TYPES):
            raise forms.ValidationError( u'%s is not a valid excel file. Please make sure your input file is an excel file (Excel 2007 is NOT supported.' % extension )
        else:
            return input_excel
class newaccount(forms.Form):
    oldacc = forms.CharField(max_length=42, label='OLD Account No', widget=forms.TextInput(attrs={'size': '35'}))
    newacc = forms.CharField(max_length=42, label='NEW Account No', widget=forms.TextInput(attrs={'size': '35'}))
    def __init__(self, *args):
        super(newaccount, self).__init__(*args)
        self.fields['oldacc'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['newacc'].widget.attrs['class'] = 'loginTxtbox'

class dateformpl(forms.Form):
    startdate = forms.CharField(label = "TransDate (M/D/Y)",max_length = 280,required = True,widget = forms.TextInput(attrs={'size':'15'}))#forms.DateField()#forms.DateField()
    enddate = forms.CharField(label = "TransDate (M/D/Y)",max_length = 280,required = True,widget = forms.TextInput(attrs={'size':'15'}))#forms.DateField()#forms.DateField()
    def __init__(self, *args, **kwargs):
        super(dateformpl, self).__init__(*args, **kwargs)
        self.fields['enddate'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['startdate'].widget.attrs['class'] = 'loginTxtbox'

class promotionform(forms.Form):
    oldclass = forms.ChoiceField(label= 'Admitted Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    newclass = forms.ChoiceField(label= 'Admitted Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    session = forms.CharField(label= 'Session', max_length=25,initial='2013/2014')
    def __init__(self, *args):
        super(promotionform, self).__init__(*args)
        self.fields['oldclass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['newclass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['oldclass'].initial = Class.objects.all()
        self.fields['newclass'].initial = Class.objects.all()
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'

class updateassform(forms.Form):
    oldclass = forms.ChoiceField(label= 'Admitted Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    arm = forms.ChoiceField(label= 'Arm',choices = [(a.arm, a.arm) for a in Arm.objects.all()])
    session = forms.CharField(label= 'Session', max_length=25,initial='2012/2013')
    def __init__(self, *args):
        super(updateassform, self).__init__(*args)
        self.fields['oldclass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['oldclass'].initial = Class.objects.all()
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'





