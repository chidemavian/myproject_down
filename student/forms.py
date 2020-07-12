from django import forms
from myproject.student.models import Student
from myproject.setup.models import *
from myproject.sysadmin.models import *
import os

states = [(state, state) for state in sorted(['Abia', 'Federal Capital Territory', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi', 'Bayelsa', 'Benue',
                                              'Borno', 'Cross River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu', 'Gombe', 'Imo',
                                              'Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Kogi', 'Kwara', 'Lagos', 'Nassarawa',
                                              'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo', 'Plateau', 'Rivers', 'Sokoto', 'Taraba', 'Yobe',
                                              'Zamfara','Non-Nigeria'])]


getlg = [(lga,lga) for lga in LGA.objects.all().order_by('lga')]

def sess():
    return currentsession.objects.get(id = 1)
currse = currentsession.objects.get(id = 1)

IMPORT_FILE_TYPES = ['.jpeg','.jpg','.png' ]

class StudentRegistrationForm(forms.Form):
    birth_date = forms.CharField(max_length=12, label='Date Of Birth', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    admitted_session = forms.CharField(max_length=12, label='Admitted Session', widget=forms.TextInput(attrs={'readonly': 'readonly'}),initial=sess)
    firstname = forms.CharField(label='First Name', max_length=75)
    surname = forms.CharField(label= 'Surname', max_length=75)
    othername = forms.CharField(label= 'Other Names', max_length=75,required=False)
    address = forms.CharField(label= 'Address', max_length=200,widget=forms.Textarea(attrs={'cols':'30','rows':'1'}))
    sex = forms.ChoiceField(label= 'Gender', choices=(('Male', 'Male'),('Female', 'Female')))
    birth_place = forms.CharField(label= 'Place of Birth', max_length=75)
    state_of_origin = forms.ChoiceField(label= 'State of Origin', choices=states)
    lga = forms.ChoiceField(label='L.G.A.', choices = [(lgaa,lgaa) for lgaa in LGA.objects.all().order_by('lga')])
    studentpicture = forms.ImageField(required=False,widget=forms.FileInput(attrs={'size':'5'}),label='Student Picture')
    fathername = forms.CharField(label= "Name", max_length=275)
    fatheraddress = forms.CharField(label= 'Address', max_length=200)
    fathernumber = forms.CharField(label= 'Phone Number', max_length=35,required=False)#validators=[PhoneNumberValidator]s
    fatheroccupation = forms.CharField(label= 'Occupation', max_length=175)
    fatheremail = forms.CharField(label= 'Father E-mail', max_length=200,required=False)
    prev_school = forms.CharField(label= 'Former School', max_length=200, required=False)
    prev_class = forms.CharField(label= 'Former Class', max_length=25, required=False)
    admitted_class = forms.ChoiceField(label= 'Admitted Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    admitted_arm = forms.ChoiceField(label= 'Arm', choices = [(a.arm, a.arm) for a in Arm.objects.all()])
    admissionno = forms.CharField(label= 'Admission Number', max_length=25)
    house = forms.ChoiceField(label= 'House',choices = [(house,house) for house in House.objects.all().order_by('house')])
    dayboarding = forms.ChoiceField(label='Day/Boarding', choices=(('Day', 'Day'), ('Boarding', 'Boarding')))
    subclass = forms.ChoiceField(label= 'Sub Class Admitted',choices=(('Nil', 'Nil'), ('JS', 'JS'), ('Science', 'Science'),('Art', 'Art'),('Commercial', 'Commercial')))
    
    class Meta:
        model = Student
        widgets = {'lga': forms.Select,
                   'admitted_arm': forms.Select(choices=[(a.arm, a.arm) for a in Arm.objects.all()]),
                   'admitted_class': forms.Select(choices=[(c.klass, c.klass) for c in Class.objects.all()]),
                   'house': forms.Select(choices=[(h.house, h.house) for h in House.objects.all()])}

    def __init__(self, *args):
        super(StudentRegistrationForm, self).__init__(*args)
        self.fields['admitted_arm'].choices = [(a.arm, a.arm) for a in Arm.objects.all()]
        self.fields['admitted_arm'].initial = Arm.objects.all()
        self.fields['admitted_class'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['admitted_class'].initial = Class.objects.all()
        self.fields['house'].choices = [(house,house) for house in House.objects.all().order_by('house')]
        self.fields['house'].initial = House.objects.all()
        self.fields['lga'].choices = [(lgaa,lgaa) for lgaa in LGA.objects.all().order_by('lga')]
        self.fields['lga'].initial = LGA.objects.all()
        self.fields['birth_date'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['admitted_session'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['firstname'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['surname'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['othername'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['address'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['fathername'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['birth_place'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['fatheraddress'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['fathernumber'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['fatheroccupation'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['fatheremail'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['prev_school'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['prev_class'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['admissionno'].widget.attrs['class'] = 'loginTxtbox'

    def clean_rfile(self):
        rfile = self.cleaned_data['studentpicture']
        if rfile is None:
            pass
            #print "OK"
        else:
            #print rfile
            rrfile = self.cleaned_data['studentpicture'].name
            extension = os.path.splitext(rrfile)[1]
            if not (extension.lower() in IMPORT_FILE_TYPES):
                raise forms.ValidationError( u'%s is not a valid Image file.' % extension )
            else:
                return rfile


#class ReturningStudentForm(forms.Form):
 #   student = forms.ModelChoiceField(Student.objects.filter(gone=True), widget=forms.HiddenInput)

class StudentWithdrawalForm(forms.Form):
    pk = forms.IntegerField(widget=forms.HiddenInput)
    reason = forms.CharField(max_length=200, label='Reason for Withdrawal', widget=forms.Textarea(attrs={'style': 'height: 40px;'}))
    date_withdrawn = forms.DateField(label='Date of Withdrawal')

class StudentSearchForm(forms.Form):
    studentname = forms.ChoiceField(choices = [(c.fullname, c.fullname) for c in Student.objects.filter(admitted_session = currse)], label="Student's Name")
    admitted_class1 = forms.ChoiceField(label= 'Admitted Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    admitted_arm1 = forms.ChoiceField(label= 'Arm', choices = [(a.arm, a.arm) for a in Arm.objects.all()])

    def __init__(self, *args):
        super(StudentSearchForm, self).__init__(*args)
        self.fields['admitted_arm1'].choices = [(a.arm, a.arm) for a in Arm.objects.all()]
        self.fields['admitted_arm1'].initial = Arm.objects.all()
        self.fields['admitted_class1'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['admitted_class1'].initial = Class.objects.all()
        self.fields['studentname'].choices = [(c.fullname, c.fullname) for c in Student.objects.filter(admitted_session = currse)]
        self.fields['studentname'].initial = Student.objects.filter(admitted_session = currse)

class studentreportform(forms.Form):
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':'10'}),initial=currse)
    klass = forms.ChoiceField(label= 'Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    arm = forms.ChoiceField(label= 'Arm', choices = [(a.arm, a.arm) for a in Arm.objects.all()])
    dayboarding = forms.ChoiceField(label='Day/Boarding', choices=(('Day', 'Day'), ('Boarding', 'Boarding')))
    filtermethod = forms.ChoiceField(label='Sort by', choices=(('Class', 'Class'), ('Classroom', 'Classroom'),('Day/Boarding', 'Day/Boarding')))
    excelfile = forms.BooleanField(label='Excel',required=False)

    def __init__(self, *args):
         super(studentreportform, self).__init__(*args)
         self.fields['arm'].choices = [(a.arm, a.arm) for a in Arm.objects.all()]
         self.fields['arm'].initial = Arm.objects.all()
         self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
         self.fields['klass'].initial = Class.objects.all()
         self.fields['session'].widget.attrs['class'] = 'loginTxtbox'

class withdrawnreportform(forms.Form):
      withdrawsession = forms.CharField(label='Session',max_length=9,initial= currse)
      excelfile = forms.BooleanField(label='Download In Excel',required=False)
      def __init__(self, *args):
          super(withdrawnreportform, self).__init__(*args)
          self.fields['withdrawsession'].widget.attrs['class'] = 'loginTxtbox'


class SearchForm(forms.Form):
    studentname = forms.CharField(label='Student Name',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':'45'}))

    def __init__(self, *args):
        super(SearchForm, self).__init__(*args)
        self.fields['studentname'].widget.attrs['class'] = 'loginTxtbox'




