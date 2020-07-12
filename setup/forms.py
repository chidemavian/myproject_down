from django import forms
from myproject.setup.models import * #Role, Class, Arm, Department, House, Subject, School
import os

subject_category = (
    ('NONE', 'NONE'),('KG', 'KG'), ('Nursery', 'Nursery'),('YEAR', 'YEAR'),('JS', 'JS'), ('Primary', 'Primary'), ('Art', 'Art'), ('Science', 'Science'), ('Commercial', 'Commercial'))

IMPORT_FILE_TYPES = ['.xls', ]

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class

    def clean_rclass(self):
        klass = self.cleaned_data.get('klass', '').upper()

        if Class.objects.filter(klass=klass):
            raise forms.ValidationError('Class Already Exists!')
        return klass


class ArmForm(forms.ModelForm):
    class Meta:
        model = Arm

    def clean_arm(self):
        arm = self.cleaned_data.get('arm', '').upper()
        if Arm.objects.filter(arm=arm):
            raise forms.ValidationError('Arm Already Exists!')
        return arm


class subject_groupForm(forms.ModelForm):
    class Meta:
        model = Subject_group

    def clean_arm(self):
        Subject_group = self.cleaned_data.get('subject_group', '').upper()
        if Subject_group.objects.filter(subject_group= subject_group):
            raise forms.ValidationError('subject group Already Exists!')
        return subject_group


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        exclude = ['num','ca','exam' ]

    def clean_subject(self):
        subject = self.cleaned_data.get('subject', '')
        category = self.cleaned_data.get('category', '')
        if Subject.objects.filter(subject=subject, category=category):
            raise forms.ValidationError('Subject Already Exists!')
        return subject

class SelectClassForm(forms.Form):
    klass = forms.ChoiceField(choices=subject_category, label='Select Category')


class HouseForm(forms.ModelForm):
    class Meta:
        model = House

class XlsInputForm(forms.Form):
    input_excel = forms.FileField(required= True, label= u"Upload the Excel file to import to the system.")

    def clean_input_excel(self):
        input_excel = self.cleaned_data['input_excel'].name
        extension = os.path.splitext( input_excel)[1]
        if not (extension in IMPORT_FILE_TYPES):
            raise forms.ValidationError( u'%s is not a valid excel file. Please make sure your input file is an excel file (Excel 2007 is NOT supported.' % extension )
        else:
            return input_excel
