from django.db import models
from django.db.utils import DatabaseError
from django.db.models import Avg
from django.core.exceptions import FieldError
from myproject.utils import SchoolSessionValidator
from myproject.student.models import Student
from myproject.setup.models import Subject
from myproject.sysadmin.models import *
from myproject.academics.utils import *
from decimal import *

# Create your models here.
terms_list = (('First', 'First Term'), ('Second', 'Second Term'), ('Third', 'Third Term'))


class StudentAcademicRecord(models.Model):
    student = models.ForeignKey(Student, related_name='academic_record')
    klass = models.CharField('Class', max_length=20, default='')
    arm = models.CharField('Arm', max_length=10, default='')
    term = models.CharField('Term', max_length=20, choices=terms_list, null=True)
    session = models.CharField('Session', max_length=20, default='', validators=[SchoolSessionValidator])
    
    days_open = models.IntegerField('No. of Days School Opened', default=0)
    days_present = models.IntegerField('Days Present', default=0)
    days_absent = models.IntegerField('Days Absent', default=0)
    next_term_start = models.DateField('Next Term Begins', null=True,blank=True,default='2000-01-01')

    position = models.CharField('Class Position', max_length=10, default='N/A')
    position1 = models.CharField('Class Room Position', max_length = 10, default = 'N/A')
    
    
    stu_ave1 = models.DecimalField('Student Average Mid term', decimal_places=2, max_digits=5, default=0)
    stu_ave2 = models.DecimalField('Student Average End term', decimal_places=2, max_digits=5, default=0)
    class_ave1  = models.DecimalField('Class Average Mid term', decimal_places=2, max_digits=5, default=0)
    class_ave2 = models.DecimalField('Class Average End term', decimal_places=2, max_digits=5, default=0)
    classAve = models.DecimalField('Class Average', decimal_places=2, max_digits=5, default=0)
    percentage = models.DecimalField('Percentage', decimal_places=2, max_digits=5, default=0)


    com1  = models.CharField('Mid term Comment',max_length=8000, default='')
    class_teacher_comment = models.CharField("Class Teacher's Comment", max_length=8000, default='')
    
    com2 = models.CharField('midterm principal term Comment',  max_length =9000, default='')
    principal_comment = models.CharField("End term  Principal's Comment", max_length=8000, default='')



    def __unicode__(self):
        return  u'classave: %s,Name: %s, Admission No: %s , Class: %s, Arm: %s,Session: %s' %(self.classAve, self.student.fullname,self.student.admissionno,self.klass,self.arm,self.session)
    
    class Meta:
        ordering = ['student']
        verbose_name_plural = 'Student Academic'

    def __get_subjects(self):
        if self.student.subclass.startswith('J'):
            try:
                return [(s.subject, s.num) for s in Subject.objects.filter(category='JS')]
            except DatabaseError:
                return []
        elif self.student.subclass.startswith('A'):
            try:
                return [(s.subject, s.num) for s in Subject.objects.filter(category='Art')]
            except DatabaseError:
                return []
        elif self.student.subclass.startswith('S'):
            try:
                return [(s.subject, s.num) for s in Subject.objects.filter(category='Science')]
            except DatabaseError:
                return []
        elif self.student.subclass.startswith('C'):
            try:
                return [(s.subject, s.num) for s in Subject.objects.filter(category='Commercial')]
            except DatabaseError:
                return []

        else:
            try:
              return [(s.subject, s.num) for s in Subject.objects.exclude(category='Year')]
            except DatabaseError:
               return []



score = (('A', 'A - Exceptionally Exhibited'), ('B', 'B - Appreciably Demonstrated'),
        ('C', 'C - Satisfactorily Displayed'), ('D', 'D - Needs Improvement'),
        ('N/A', 'Not Available'))


class AffectiveSkill(models.Model):
    academic_rec = models.OneToOneField(StudentAcademicRecord, related_name='affective_domain')
    punctuality = models.CharField('Punctuality', max_length=3, choices=score, default='A')
    neatness = models.CharField('Neatness', max_length=3, choices=score, default='A')
    honesty = models.CharField('Honesty', max_length=3, choices=score, default='A')
    initiative = models.CharField('Initiative', max_length=3, choices=score, default='A')
    self_control = models.CharField('Self Control', max_length=3, choices=score, default='A')
    reliability = models.CharField('Reliability', max_length=3, choices=score, default='A')
    perseverance = models.CharField('Perseverance', max_length=3, choices=score, default='A')
    politeness = models.CharField('Politeness', max_length=3, choices=score, default='A')
    attentiveness = models.CharField('Attentiveness', max_length=3, choices=score, default='A')
    rel_with_people = models.CharField('Relationship with People', max_length=3, choices=score, default='A')
    cooperation = models.CharField('Co-operation', max_length=3, choices=score, default='A')
    organizational_ability = models.CharField('Organizational Ability', max_length=3, choices=score, default='A')

    def __unicode__(self):
        return u'Name :%s,Admission No : %s,Class : %s,Arm %s:Session %s' %(self.academic_rec.student.fullname,self.academic_rec.student.admissionno,self.academic_rec.klass,self.academic_rec.arm,self.academic_rec.session)


class PsychomotorSkill(models.Model):
    academic_rec = models.OneToOneField(StudentAcademicRecord, related_name='psychomotor_domain')
    attendance = models.CharField('Attendance and Punctuality', max_length=3, choices=score, default=0)
    social_behaviour = models.CharField('Social Behaviour', max_length=3, choices=score, default=0)
    motivation= models.CharField('Motivation', max_length=3, choices=score, default=0)
    contribution = models.CharField('Contribution', max_length=3, choices=score, default=0)

    def __unicode__(self):
        return u'Name :%s,Admission No : %s,Class : %s,Arm %s: ,Session %s' %(self.academic_rec.student.fullname,self.academic_rec.student.admissionno,self.academic_rec.klass,self.academic_rec.arm,self.academic_rec.session)

grading = (('A', 'A (80 - 100)'), ('B', 'B (65 - 79)'), ('C', 'C (55 - 64)'),
           ('P', 'P (45 - 54)'), ('F', 'F (0 - 4)'))


class SubjectScore(models.Model):
    academic_rec = models.ForeignKey(StudentAcademicRecord, related_name='subject_scores')
    subject = models.CharField('Subject', max_length=125, default=0)
    subject_group = models.CharField('Subject Group', max_length=125, default='ALL')
    num = models.IntegerField(editable=False)
    term = models.CharField('Term', max_length=20, choices=terms_list)
    session = models.CharField('Session', max_length=20)
    klass = models.CharField('Class', max_length=20)
    arm = models.CharField('Arm', max_length=10)

    first_ca = models.CharField('First CA', max_length=2, default=0)
    second_ca = models.CharField('Second CA', max_length=2, default=0)
    third_ca = models.CharField('Third CA',max_length=2, default=0)
    fourth_ca = models.CharField('Fourth CA', max_length=2, default=0)
    fifth_ca = models.CharField('Fifth CA', max_length=2, default=0)
    sixth_ca = models.CharField('Sixth CA', max_length=2, default=0)

    mid_term_score = models.DecimalField('Midterm', decimal_places=2, max_digits=4, default=0)
    end_term_score = models.DecimalField('Term Score', decimal_places=2, max_digits=4, default=0)
    
    grade = models.CharField('Grade', max_length=3, default= 'F')
    subject_avg = models.DecimalField(decimal_places=2, max_digits=4, default=0, editable=False)

    subposition = models.CharField('Position', max_length=10, default='N/A')
    remark = models.CharField('Remark', max_length=60)
    
    subject_teacher = models.CharField('Subject Teacher', max_length=200,null=True, default=models.NOT_PROVIDED)
    annual_avg = models.DecimalField(decimal_places=2, max_digits=4, default=0, editable=False)
    remarks = models.CharField('Subject - Grade conversion', max_length=5, default='No entry')


    def __unicode__(self):
        return u'%s %s-%s-%s-%s-%s-%s-%s-%s-%s-%s-%s-%s-%s-%s' %(self.remarks, self.academic_rec.student.subclass, self.term,self.academic_rec.student.fullname,self.academic_rec.student.admissionno,self.academic_rec.klass,self.academic_rec.arm,self.academic_rec.session,self.subject,self.first_ca,self.second_ca,self.sixth_ca,self.end_term_score,self.remark,self.annual_avg)
    class Meta:
        ordering = ['academic_rec']
        verbose_name_plural = 'Student Academic Scores Table'


    def save(self, **kwargs):    
      self.mid_term_score = (self.first_ca  + self.second_ca + self.third_ca)
      self.end_term_score = int(self.first_ca)  + int(self.second_ca) + int(self.third_ca) + int(self.fourth_ca)  + int(self.fifth_ca) + int(self.sixth_ca)

      if self.term.startswith('T'):
          if self.klass.startswith('J'):
             if (self.annual_avg >=80) and (self.annual_avg <= 100):
                 self.grade = 'A'
                 self.remark = 'Excellent'
             elif (self.annual_avg >=65) and (self.annual_avg <= 79.99):
                 self.grade = 'B'
                 self.remark = 'Very Good'
             elif (self.annual_avg >=55) and (self.annual_avg <= 64.99):
                 self.grade = 'C'
                 self.remark = 'Good'
             elif (self.annual_avg >=45) and (self.annual_avg <= 54.99):
                 self.grade = 'P'
                 self.remark = 'Fair'
             elif (self.annual_avg >=0) and (self.annual_avg <= 44.99):
                  self.grade = 'F'
                  self.remark = 'Needs Academic Assistance'
             else:
                 raise FieldError('Term score cannot exceed 100 or be less than 0!')
             super(SubjectScore, self).save(**kwargs)
          elif self.klass.startswith('S'):
              if (self.annual_avg >=80) and (self.annual_avg <= 100):
                  self.grade = 'A1'
                  self.remark = 'Excellent'
              elif (self.annual_avg >=75) and (self.annual_avg <= 79.99):
                  self.grade = 'B2'
                  self.remark = 'Commendable'
              elif (self.annual_avg >=70) and (self.annual_avg <= 74.99):
                   self.grade = 'B3'
                   self.remark = 'Commendable'
              elif (self.annual_avg >=65) and (self.annual_avg <= 69.99):
                   self.grade = 'C4'
                   self.remark = 'Very Good'
              elif (self.annual_avg >=60) and (self.annual_avg <= 64.99):
                   self.grade = 'C5'
                   self.remark = 'Very Good'
              elif (self.annual_avg >=55) and (self.annual_avg <= 59.99):
                    self.grade = 'C6'
                    self.remark = 'Good'
              elif (self.annual_avg >=50) and (self.annual_avg <= 54.99):
                   self.grade = 'D7'
                   self.remark = 'Average'
              elif (self.annual_avg >=45) and (self.annual_avg <= 49.99):
                    self.grade = 'E8'
                    self.remark = 'Below Average'
              elif (self.annual_avg >=0) and (self.annual_avg <= 44.99):
                   self.grade = 'F9'
                   self.remark = 'Need Academic Support'
              else:
                  raise FieldError('Term score cannot exceed 100 or be less than 0!')
              super(SubjectScore, self).save(**kwargs)
          else:
              if (self.annual_avg >=95) and (self.annual_avg <= 101):
                  self.grade = 'A+'
                  self.remark = 'Excellent'
              elif (self.annual_avg >=90) and (self.annual_avg <= 94.99):
                  self.grade = 'A'
                  self.remark = 'Excellent'
              elif (self.annual_avg >=85) and (self.annual_avg <= 89.99):
                  self.grade = 'B'
                  self.remark = 'Very Good'
              elif (self.annual_avg >=80) and (self.annual_avg <= 84.99):
                  self.grade = 'B+'
                  self.remark = 'Very Good'
              elif (self.annual_avg >=75) and (self.annual_avg <= 79.99):
                  self.grade = 'B'
                  self.remark = 'Good'
              elif (self.annual_avg >=70) and (self.annual_avg <= 74.99):
                  self.grade = 'B-'
                  self.remark = 'Good'
              elif (self.annual_avg >=65) and (self.annual_avg <= 69.99):
                  self.grade = 'C+'
                  self.remark = 'Average'
              elif (self.annual_avg >=60) and (self.annual_avg <= 64.99):
                  self.grade = 'C'
                  self.remark = 'Below Average'
              elif (self.annual_avg >=55) and (self.annual_avg <= 59.99):
                  self.grade = 'C-'
                  self.remark = 'Below Average'
              elif (self.annual_avg >=50) and (self.annual_avg <= 54.99):
                  self.grade = 'D'
                  self.remark = 'Fair'
              elif (self.annual_avg >=45) and (self.annual_avg <= 49.99):
                  self.grade = 'D-'
                  self.remark = 'Poor'
              elif (self.annual_avg >=40) and (self.annual_avg <= 44.99):
                  self.grade = 'E'
                  self.remark = 'Very Poor'
              elif (self.annual_avg >=0) and (self.annual_avg <= 39.99):
                  self.grade = 'F'
                  self.remark = 'Fail'
              else:
                  raise FieldError('Term score cannot exceed 100 or be less than 0!')
              super(SubjectScore, self).save(**kwargs)

      else:
         if self.klass.startswith('J'):
            if (self.end_term_score >=90) and (self.end_term_score <= 100):
                 self.grade = 'A*'
                 self.remarks = 'DISTINCTION'
            elif (self.end_term_score >=80) and (self.end_term_score <=89.99 ):
                 self.grade = 'A'
                 self.remarks = 'EXCELLENT'
            elif (self.end_term_score >=70) and (self.end_term_score <= 79.99):
                 self.grade = 'B'
                 self.remarks = 'VERY GOOD'
            elif (self.end_term_score >=60) and (self.end_term_score <= 69.99):
                  self.grade = 'C'
                  self.remarks = 'GOOD'
            elif (self.end_term_score >=50) and (self.end_term_score <= 59.99):
                 self.grade = 'P'
                 self.remarks = 'PASS'
            elif (self.end_term_score >=45) and (self.end_term_score <= 49.99):
                 self.grade = 'P'
                 self.remarks = 'FAIR'
            elif (self.end_term_score >=40) and (self.end_term_score <= 44.99):
                 self.grade = 'P'
                 self.remarks = 'POOR'
            elif (self.end_term_score >= 0) and (self.end_term_score <= 39.99):
                 self.grade = 'F'
                 self.remarks = 'FAIL'
            else:
                raise FieldError('Term score 5546 cannot exceed 100 or be less than 0!')
            super(SubjectScore, self).save(**kwargs)
            
         elif self.klass.startswith('S'):
            if (self.end_term_score >=90) and (self.end_term_score <= 100):
                self.grade = 'A1'
                self.remark = 5
            elif (self.end_term_score >=80) and (self.end_term_score <= 89.99):
                 self.grade = 'B2'
                 self.remark = 5
            elif (self.end_term_score >=70) and (self.end_term_score <= 79.99):
                 self.grade = 'B3'
                 self.remark = 4
            elif (self.end_term_score >=65) and (self.end_term_score <= 69.99):  
                 self.grade = 'C4'
                 self.remark = 4
            elif (self.end_term_score >=60) and (self.end_term_score <= 64.9):
                 self.grade = 'C5'
                 self.remark = 3
            elif (self.end_term_score >=55) and (self.end_term_score <= 59.99):
                self.grade = 'C6'
                self.remark = 3
            elif (self.end_term_score >=50) and (self.end_term_score <= 54.99):
                 self.grade = 'D7'
                 self.remark = 2
            elif (self.end_term_score >=45) and (self.end_term_score <= 49.99):
                self.grade = 'E8'
                self.remark = 2
            elif (self.end_term_score >=0) and (self.end_term_score <= 44.99):
                 self.grade = 'F9'
                 self.remark = 1
            else:
                raise FieldError('Term score cannot exceed 100 or be less than 0!')
            super(SubjectScore, self).save(**kwargs)
