from django.db import models

class userprofile(models.Model):
    exam = models.CharField('Exam Type', max_length=375)
    username = models.CharField('Username', max_length=375,default=0)
    surname = models.CharField('Surname', max_length=75)
    firstname = models.CharField('Firstame', max_length=75)
    email = models.EmailField('E-mail', max_length=75)
    klass = models.CharField('Class', max_length=20,default=0)
    password = models.CharField('Password',max_length=10)
    pix = models.ImageField('Image', upload_to='studentpix', null=True,blank=True,default='studentpix/user.png')



    def __unicode__(self):
        return '%s %s %s'%(self.exam,self.surname,self.email)


class tblpayment(models.Model):
    exam = models.CharField('Exam Type', max_length=375)
    username = models.CharField('Username', max_length=375,default=0)
    surname = models.CharField('Surname', max_length=75)
    firstname = models.CharField('Firstame', max_length=75)
    email = models.EmailField('E-mail', max_length=75)
    klass = models.CharField('Class', max_length=20,default=0)
    stream = models.CharField('Stream',max_length=10)
    # pix = models.ImageField('Image', upload_to='studentpix', null=True,blank=True,default='studentpix/user.png')



    def __unicode__(self):
        return '%s %s %s'%(self.exam,self.surname,self.email)