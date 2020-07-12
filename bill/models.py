from django.db import models

# Create your models here.
class tblexpenses(models.Model):
    name = models.CharField('name', max_length=160)

    def __unicode__(self):
        return  u'%s' % self.name


    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Bill Creation'

class tblbill(models.Model):
    klass = models.CharField(max_length= 130)
    desc = models.CharField(max_length= 300)
    billamount = models.DecimalField(decimal_places=2,max_length=65,max_digits=65)
    acccode = models.CharField(max_length= 300)
    dayboarding = models.CharField(max_length= 50)
    term = models.CharField(max_length= 50)
    userid = models.CharField(max_length= 150)
    def __unicode__(self):
        return  u'%s - %s - %s - %s - %s - %s - %s' % (self.klass,self.desc,self.billamount,self.acccode,self.dayboarding,self.term,self.userid)
    class Meta:
        ordering = ['klass','id']
        verbose_name_plural = 'Bill SetUp'

class tbladditionalbill(models.Model):
    session = models.CharField(max_length= 130)
    admissionno = models.CharField(max_length= 130)
    name = models.CharField(max_length= 230)
    klass = models.CharField(max_length= 130)
    arm = models.CharField(max_length= 130)
    term = models.CharField(max_length= 130)
    billamount = models.DecimalField(decimal_places=2,max_length=65,max_digits=65)
    desc = models.CharField(max_length= 130)
    acccode = models.CharField(max_length= 130)
    userid = models.CharField(max_length= 150)

    def __unicode__(self):
        return  u'%s - %s - %s - %s - %s - %s - %s -%s -%s' % (self.session,self.admissionno,self.name,self.klass,self.arm,self.term,self.billamount,self.acccode,self.desc)

    class Meta:
        ordering = ['klass','id']
        verbose_name_plural = 'Additional Bill'

class postedbill(models.Model):
    session = models.CharField(max_length= 130)
    klass = models.CharField(max_length= 130)
    term = models.CharField(max_length= 130)
    userid = models.CharField(max_length= 150)
    dateposted = models.DateTimeField(auto_now_add=True, blank=True)
    def __unicode__(self):
        return  u'%s - %s - %s - %s -%s' % (self.session,self.klass,self.term,self.userid,self.dateposted)

    class Meta:
        ordering = ['klass','id']
        verbose_name_plural = 'Posted Bill'

class oldbill(models.Model):
    session = models.CharField(max_length= 130)
    admissionno = models.CharField(max_length= 130)
    name = models.CharField(max_length= 230)
    klass = models.CharField(max_length= 130)
    arm = models.CharField(max_length= 130)
    term = models.CharField(max_length= 130)
    billamount = models.DecimalField(decimal_places=2,max_length=65,max_digits=65)
    desc = models.CharField(max_length= 130)
    acccode = models.CharField(max_length= 130)
    userid = models.CharField(max_length= 150)
    def __unicode__(self):
        return  u'%s - %s - %s - %s - %s - %s - %s -%s -%s' % (self.session,self.admissionno,self.name,self.klass,self.arm,self.term,self.billamount,self.acccode,self.desc)

    class Meta:
        ordering = ['admissionno','id']
        verbose_name_plural = 'Old Bill'

class billsession(models.Model):
    session = models.CharField('Current Session',max_length= 25)

    def __unicode__(self):
        return "%s" %self.session
    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Bill Calendar Year'





