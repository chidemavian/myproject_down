from django.db import models
from setup.models import *
#from myproject.utils import PhoneNumberValidator
from PIL import Image

subject_category = (('PRY', 'PRY'),('JS', 'JS'),('Science', 'Science'), ('Commercial', 'Commercial'),('Art','Art'))

subject_category2 = (('Compulsory', 'Compulsory'), ('Optional', 'Optional'))
status = (('FROZEN', 'FROZEN'), ('FROZEN', 'FROZEN'))

states = [(state, state) for state in sorted(['Abia', 'Abuja FCT', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi', 'Bayelsa', 'Benue',
              'Borno', 'Cross River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu', 'Gombe', 'Imo',
              'Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Kogi', 'Kwara', 'Lagos', 'Nassarawa',
              'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo', 'Plateau', 'Rivers', 'Sokoto', 'Taraba', 'Yobe',
              'Zamfara'])]

class Subject(models.Model):
    category = models.CharField('Group', max_length=25, choices=subject_category)
    subject = models.CharField('Subject', max_length=75)
    ca = models.FloatField('CA')
    exam = models.FloatField('Exam')
    num = models.IntegerField()
    category2 = models.CharField('Category', max_length=25, choices=subject_category2)
    status = models.CharField('Status', null= True, max_length=25, choices=status, default='INACTIVE')
    

    def __unicode__(self):
        return  u' Category : %s ,Subject : %s , CA : %s , Exam  : %s, Number %s ' % (self.category,self.subject,self.ca,self.exam,self.num)

    class Meta:
        ordering = ['category', 'subject']


   # def save(self, *args, **kwargs):
    #    numDict = {"ENGLISH LANGUAGE": 1, "MATHEMATICS": 2, "UNDEFINED": -1}
     #   self.subject = self.subject.upper()

      #  self.num = numDict[self.subject if self.subject in numDict.keys() else "UNDEFINED"]
       # super(Subject, self).save(*args, **kwargs)

class Class(models.Model):
    klass = models.CharField('Class', max_length=25, unique=True)

    def __unicode__(self):
        return u'%s' %self.klass

    def save(self, *args, **kwargs):
        self.klass = self.klass.upper()
        super(Class, self).save(*args, **kwargs)

    class Meta:
        ordering = ['klass']
        verbose_name_plural = 'Classes'

class Arm(models.Model):
    arm = models.CharField('Arm', max_length=25, unique=True)

    def __unicode__(self):
        return '%s'% self.arm

    def save(self, *args, **kwargs):
        self.arm = self.arm.upper()
        super(Arm, self).save(*args, **kwargs)

    class Meta:
        ordering = ['arm']
        verbose_name_plural = 'Arms'


class Subject_group(models.Model):
    subject_group = models.CharField('Subject Group', max_length=50, unique=True)

    def __unicode__(self):
        return '%s'% self.subject_group

    def save(self, *args, **kwargs):
        self.subject_group = self.subject_group.upper()
        super(Subject_group, self).save(*args, **kwargs)

    class Meta:
        ordering = ['subject_group']
        verbose_name_plural = 'subject_group'



class Role(models.Model):
    role = models.CharField('Role', max_length=75, unique=True)

class Department(models.Model):
    department = models.CharField('Department', max_length=75, unique=True)

class House(models.Model):
    house = models.CharField('House', max_length=75, unique=True)
    def __unicode__(self):
        return  u'%s' %self.house

class School(models.Model):
    name = models.CharField('Name', max_length=75)
    address = models.CharField('Address', max_length=200)
   # city = models.CharField('City', max_length=25)
   # state = models.CharField('State', max_length=25, choices=states)validators=[PhoneNumberValidator]
    phonenumber = models.CharField('Telephone', max_length=65,null=True,blank=True)
    email = models.EmailField('Email', max_length=75,null=True,blank=True)
    website = models.CharField('Website', max_length=200,null=True,blank=True)
    logo = models.ImageField('School Logo', upload_to='school-logo', null=True,blank=True,default='img/noimage.jpeg')
   # principals_name = models.CharField("Principal's Name", max_length=75)
    def __unicode__(self):
        return  u'%s  ::-  %s ' % (self.name,self.address)

    def save(self, size=(100, 120), **kwargs):
        """
    Save Photo after ensuring it is not blank. Resize as needed.
    """

        if not self.id and not self.logo:
            return

        super(School, self).save(**kwargs)

        filename = self.logo.path
        image = Image.open(filename)

        image.thumbnail(size, Image.ANTIALIAS)
        image.save(filename)

    class Meta:
        ordering =['id']
        verbose_name_plural = "School Informarion"

class LGA(models.Model):
    state = models.CharField('State', max_length=25, choices=states)
    lga = models.CharField('L.G.A.', max_length=25)

    class Meta:
        ordering = ['state', 'lga']
        verbose_name_plural = 'Local Government Areas'

    def __unicode__(self):
        return  u'%s' % self.lga

class subclass(models.Model):
      subcode = models.CharField('Sub Code',max_length= 10)
      classsub = models.CharField('Sub Class',max_length=100,choices=(('JS', 'JS'), ('Science', 'Science'),('Art', 'Art'),('Commercial', 'Commercial'),('Year', 'Year'),('Primary', 'Primary'),('Basic', 'Basic'),('Science/Math','Science/Math'),('Technology','Technology'),('Humanities','Humanities'),('Business','Business')))

      class Meta:

          verbose_name_plural = 'Sub Class'

      def __unicode__(self):
         return  u'%s' % self.classsub

class gradingsys(models.Model):
    classsub = models.CharField('Sub Class',max_length=100,choices=(('JS', 'JS'), ('SS', 'SS'),('Year', 'Year'),('Primary', 'Primary'),('Basic', 'Basic')))
    grade = models.CharField('Grade e.g 80-100',max_length= 10)
    remark = models.CharField('Remark e.g A+',max_length= 10)

    class Meta:
        ordering = ['classsub','id']
        verbose_name_plural = 'Grading System'
    def __unicode__(self):
        return  u'%s %s %s' % (self.classsub,self.grade,self.remark)

class appused(models.Model):
    primary = models.BooleanField('Primary')
    secondary = models.BooleanField('Secondary')
    class Meta:
        verbose_name_plural = 'App In Use'

    def __unicode__(self):
        return  u'%s %s' % (self.primary,self.secondary)
