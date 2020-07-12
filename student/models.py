from django.db import models
from myproject.setup.models import *
from myproject.utils import PhoneNumberValidator, SchoolSessionValidator

# Create your models here.
terms_list = (('First', 'First Term'), ('Second', 'Second Term'), ('Third', 'Third Term'))

states = [(state, state) for state in sorted(['Abia', 'Federal Capital Territory', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi', 'Bayelsa', 'Benue',
              'Borno', 'Cross River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu', 'Gombe', 'Imo',
              'Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Kogi', 'Kwara', 'Lagos', 'Nassarawa',
              'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo', 'Plateau', 'Rivers', 'Sokoto', 'Taraba', 'Yobe',
              'Zamfara','Non-Nigeria'])]


class Student(models.Model):
    firstname = models.CharField('First Name', max_length=75)
    surname = models.CharField('Surname', max_length=75)
    othername = models.CharField('Other Names', max_length=75, null=True, blank=True)
    address = models.CharField('Address', max_length=200)
    sex = models.CharField('Sex',max_length=10, choices=(('Male', 'Male'),('Female', 'Female')))
    birth_date = models.DateField('Date of Birth',null=True,blank=True,default='2000-01-01')
    birth_place = models.CharField('Place of Birth', max_length=75)
    state_of_origin = models.CharField('State of Origin', max_length=75, choices=states)
    lga = models.CharField('L.G.A.', max_length=75)
    studentpicture = models.ImageField('Passport', upload_to='studentpix', null=True,blank=True,default='studentpix/user.png')
    fathername = models.CharField("Name", max_length=275)
    fatheraddress = models.CharField('Address', max_length=200)
    fathernumber = models.CharField('Phone Number', max_length=35, null=True,blank=True )#validators=[PhoneNumberValidator]s
    fatheroccupation = models.CharField('Occupation', max_length=175)
    fatheremail = models.CharField('Father E-mail', max_length=200,null=True,blank=True)
    prev_school = models.CharField('Former School', max_length=200, null=True, blank=True)
    prev_class = models.CharField('Former Class', max_length=25, null=True, blank=True)
    admitted_class = models.CharField('Admitted Class', max_length=25)
    admitted_arm = models.CharField('Arm', max_length=25)
    admitted_session = models.CharField('Session Admitted', max_length=25, null=True, blank=True, validators=[SchoolSessionValidator])
    fullname = models.CharField('Full Name', max_length=100, editable=False)
    admissionno = models.CharField('Admission Number', max_length=25)
    house = models.CharField('House', max_length=75 )
    dayboarding = models.CharField('Day/Boarding', max_length=25, choices=(('Day', 'Day'), ('Boarding', 'Boarding')))
    gone = models.BooleanField('Gone', default=False, editable=True)
    userid = models.CharField('User Id',max_length=200,editable=False)
    subclass = models.CharField('Sub Class Admitted', max_length=25)
    first_term = models.BooleanField('First Term', default=False, editable=True, )
    second_term = models.BooleanField('Second Term', default=False, editable=True )
    third_term = models.BooleanField('Third Term', default=False, editable=True )
    def get_full_name(self):
        if self.othername:
            fullname = "%s %s %s" % (self.surname,self.firstname, self.othername)
        else: fullname = "%s %s" % (self.surname,self.firstname)
        return fullname.upper()
    def get_image_url(self):
        illegal_chars = [';', '.', ':', '/', '?', '<', '>', ',', "'", '"', '\\',
                         '{', '}', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
                         '_', '+', '=', '-']
        url = self.admissionno
        for char in illegal_chars:
            url = url.replace(char, '')
        return url
    def __unicode__(self):
        return u'%s %s %s %s %s %s'%(self.get_full_name(),self.admissionno,self.admitted_class,self.admitted_arm,self.admitted_session,self.gone)
    class Meta:
        ordering = ['fullname']
        verbose_name_plural = 'Student Information'

    #def save(self, **kwargs):
      #  self.fullname = self.get_full_name()
       # super(Student, self).save(**kwargs)

    def save(self, size=(100, 100), **kwargs):
        """
	Save Photo after ensuring it is not blank. Resize as needed.
	"""
        self.fullname = self.get_full_name()

        if not self.id and not self.studentpicture:
            return

        super(Student, self).save(**kwargs)

        filename = self.studentpicture.path
        image = Image.open(filename)

        image.thumbnail(size, Image.ANTIALIAS)
        image.save(filename)

    class Meta:
        ordering = ['fullname']
        verbose_name_plural = 'Student Information'



class WithdrawnStudent(models.Model):
    student = models.CharField("Student Full Name",max_length=300)
    klass = models.CharField("Student Class",max_length=15)
    arm = models.CharField("Arm",max_length=25)
    admissionno = models.CharField("Admission Number",max_length= 25)
    reason = models.TextField('Reason for Withdrawal')
    date_withdrawn = models.DateField('Date of Withdrawal')
    admitted_session = models.CharField('Withdrwal Session',max_length=15)
    userid = models.CharField("User Id",max_length= 250)

    def __unicode__(self):
        return u'%s - %s - %s - %s' %(self.admissionno,self.student,self.reason,self.userid)
