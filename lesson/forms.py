from django import forms
from myproject.setup.models import *
from myproject.sysadmin.models import *
from myproject.student.models import *
from myproject.lesson.models import *


def sess():
    return currentsession.objects.get(id = 1)

currse = currentsession.objects.get(id = 1)



class settopicForm(forms.Form):
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':'10','readonly':'readonly'}),initial=sess())
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    term = forms.ChoiceField(label='Term',choices=[(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')])
    subject = forms.ChoiceField(label= 'Subject', choices = [(a.subject, a.subject) for a in Subject.objects.all()])
    topic = forms.CharField(label='Topic',max_length= 200,required=True,widget=forms.Textarea(attrs={'size':'30'}))


    def __init__(self, *args):
        super(settopicForm, self).__init__(*args)
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['subject'].choices = [(a.subject, a.subject) for a in Subject.objects.all()]
        self.fields['subject'].initial = Subject.objects.all()
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]
        self.fields['term'].initial = tblterm.objects.filter(status = 'ACTIVE')

class setobjForm(forms.Form):
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':'10','readonly':'readonly'}),initial=sess())
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    term = forms.ChoiceField(label='Term',choices=[(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')])
    subject = forms.ChoiceField(label= 'Subject', choices = [(a.subject, a.subject) for a in Subject.objects.all()])


    def __init__(self, *args):
        super(setobjForm, self).__init__(*args)
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['subject'].choices = [(a.subject, a.subject) for a in Subject.objects.all()]
        self.fields['subject'].initial = Subject.objects.all()
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]
        self.fields['term'].initial = tblterm.objects.filter(status = 'ACTIVE')



class lesc(forms.Form):
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':'8','readonly':'readonly'}),initial=sess())
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    term = forms.ChoiceField(label='Term',choices=[(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')])
    wl = forms.CharField(label= 'No. Lesson/ Week', widget= forms.TextInput(attrs ={'size':'8'}))

    def __init__(self, *args):
        super(lesc, self).__init__(*args)
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]
        self.fields['term'].initial = tblterm.objects.filter(status = 'ACTIVE')

class lessonplanform(forms.Form):
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':'10','readonly':'readonly'}),initial=sess())
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    term = forms.ChoiceField(label='Term',choices=[(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')])
    subject = forms.ChoiceField(label= 'Subject', choices = [(a.subject, a.subject) for a in Subject.objects.all()])

    def __init__(self, *args):
        super(lessonplanform, self).__init__(*args)
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['subject'].choices = [(a.subject, a.subject) for a in Subject.objects.all()]
        self.fields['subject'].initial = Subject.objects.all()
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]
        self.fields['term'].initial = tblterm.objects.filter(status = 'ACTIVE')


class waform(forms.Form):
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':'10','readonly':'readonly'}),initial=sess())
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    subject = forms.ChoiceField(label= 'Subject', choices = [(a.subject, a.subject) for a in Subject.objects.all()])
    wa = forms.CharField(label='WA',required=True,widget= forms.TextInput(attrs ={'size':'10'}))
    
    def __init__(self, *args):
        super(waform, self).__init__(*args)
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['subject'].choices = [(a.subject, a.subject) for a in Subject.objects.all()]
        self.fields['subject'].initial = Subject.objects.all()
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'

class mynotes(forms.Form):
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':'10','readonly':'readonly'}),initial=sess())
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    term = forms.ChoiceField(label='Term',choices=[(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')])
    subject = forms.ChoiceField(label= 'Subject', choices = [(a.subject, a.subject) for a in Subject.objects.all()])

    def __init__(self, *args):
        super(mynotes, self).__init__(*args)
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['subject'].choices = [(a.subject, a.subject) for a in Subject.objects.all()]
        self.fields['subject'].initial = Subject.objects.all()
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]
        self.fields['term'].initial = tblterm.objects.filter(status = 'ACTIVE')

