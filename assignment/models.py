from django.db import models
#from django.contrib.admin.models import User

class tblassignment(models.Model):
	teacher = models.CharField('Teacher', max_length=75)
	subject = models.CharField('Subject', max_length=75)
	klass = models.CharField('class', max_length=75)
	arm = models.CharField('Arm', max_length=75)
	term = models.CharField('Term', max_length=75)
	session = models.CharField('Session', max_length=75)
	assignment = models.CharField('Assignment', max_length=5000)
	comment = models.CharField('Comment', max_length=5000)
	posted_on = models.DateField('Posted Date')
	submit_on = models.DateField('Submission Date')
	ass_file= models.FileField('Assignment File', upload_to='ax', null=True,blank=True)



	def __unicode__(self):
		return u' teacher : %s ,Subject : %s , assignment : %s , posted_on  : %s' % (self.teacher,self.subject,self.assignment,self.posted_on)



class tblspec(models.Model):
	teacher = models.CharField('Teacher', max_length=75)
	subject = models.CharField('Subject', max_length=75)
	name = models.CharField('Name', max_length=75)
	session = models.CharField('Session', max_length=75)
	assignment = models.CharField('Assignment', max_length=5000)
	comment = models.CharField('Comment', max_length=5000)
	posted_on = models.DateField('Posted Date')
	submit_on = models.DateField('Submission Date')

	def __unicode__(self):
		return u' teacher : %s ,Subject : %s , name : %s , posted_on  : %s' % (self.teacher,self.subject,self.name,self.posted_on)		
