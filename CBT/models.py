from django.db import models


from student.models import Student





state = terms_list = (('ACTIVE', 'ACTIVE'), ('INACTIVE', 'INACTIVE'))

# Create your models here.


class tblquestion(models.Model):
    exam_type = models.CharField('Exam Type', max_length=375)
    subject = models.CharField('Subject', max_length=75)
    session = models.CharField('Session', max_length=75, null=True, blank=True)
    klass = models.CharField('Class', max_length=20)
    term = models.CharField('Term',max_length=10)
    topic = models.CharField('Topic',max_length=1000, null=False,blank=True)
    instruction_from = models.CharField('From', max_length=975)
    instruction_to = models.CharField('From', max_length=975)
    qstn = models.CharField('Question', max_length=975)
    image = models.ImageField('Image', upload_to='questions', null=True,blank=True,default='studentpix/user.png')
    section = models.CharField('Section', max_length=20,default=0)


    def __unicode__(self):
        return '%s %s %s'%(self.exam_type,self.subject,self.qstn)



class tblcbtexams(models.Model):
    exam_type = models.CharField('Exam Type', max_length=375)
    status = models.CharField('Status', max_length=75, null=False, blank=False)
    # term = models.CharField('Term',max_length=10)


    def __unicode__(self):
        return '%s %s'%(self.exam_type,self.status)
        #ession,self.term)



class tbloptions(models.Model):
    qstn = models.ForeignKey(tblquestion, related_name='Options')
    a = models.CharField('Option A', max_length=7500)
    b = models.CharField('Option B', max_length=7500)
    c = models.CharField('Option C', max_length=7500)
    d = models.CharField('Option D', max_length=7500)
    e = models.CharField('Option E', max_length=7500)


    def __unicode__(self):
        return u'%s %s %s %s'%(self.a,self.b,self.c,self.d)    
  


class tbloptioni(models.Model):
    qstn = models.ForeignKey(tblquestion, related_name='Optioni')
    a = models.ImageField('Image', upload_to='questions',default='questions/user.png')
    b = models.ImageField('Image', upload_to='questions', default='questions/user.png')
    c = models.ImageField('Image', upload_to='questions', default='questions/user.png')
    d = models.ImageField('Image', upload_to='questions',default='questions/user.png')
    e = models.ImageField('Image', upload_to='questions',default='questions/user.png')


    def __unicode__(self):
        return u'%s %s %s %s'%(self.a,self.b,self.c,self.d)



class tblans(models.Model):
    qstn = models.ForeignKey(tblquestion, related_name='Transaction')
    ans = models.CharField('Answer', max_length=75)
    option = models.CharField('Option', max_length=7500,default=0)

    def __unicode__(self):
        return u' a : %s, b:  %s ' % (self.ans, self.option)


class tbltheory(models.Model):
	exam_type = models.CharField('Exam Type', max_length=375)
	subject = models.CharField('Subject', max_length=75)
	session = models.CharField('Session', max_length=75, null=True, blank=True)
	klass = models.CharField('Class', max_length=20)
	term = models.CharField('Term',max_length=10)
	topic = models.CharField('Topic',max_length=375,null=True,blank=True)
	instruction_to = models.CharField('From', max_length=975)
	instruction_from = models.CharField('From', max_length=975)
	image = models.ImageField('Image', upload_to='questions', null=True,blank=True,default='questions/user.png')


	def __unicode__(self):
		return u' exam_type : %s ,subject : %s , term : %s , to  : %s' % (self.exam_type,self.subject,self.term,self.instruction_from)


class tblcbtuser(models.Model):
    session = models.CharField('Session', max_length=75, null=True, blank=True)
    klass = models.CharField('Class', max_length=20)
    subject = models.CharField('Subject',max_length=10)
    user = models.CharField('User',max_length=375,null=True,blank=True)


    def __unicode__(self):
    	return u' exam : %s ,subject : %s , term : %s , d  : %s' % (self.exam_type,self.subject,self.c,self.term)



class tblcbtsubject(models.Model):
    duration = models.CharField('Duration', max_length=375)
    subject = models.CharField('Subject', max_length=75)
    session = models.CharField('Session', max_length=75, null=True, blank=True)
    klass = models.CharField('Class', max_length=20)
    term = models.CharField('Term',max_length=10)
    exam_type = models.CharField('Exam_type', max_length=75)
    status = models.CharField('Status',null=True,blank=True,max_length=60,default='INACTIVE')
  


    def __unicode__(self):

    	return u'%s-%s' % (self.subject,self.term)


class cbttrans(models.Model):
    session = models.CharField('Session', max_length=375)
    exam_type = models.CharField('Exam_type', max_length=75)
    student = models.ForeignKey(Student, max_length=75, null=True, blank=True)
    subject = models.CharField('Subject', max_length=20)
    term = models.CharField('Term',max_length=10)
    question = models.ForeignKey(tblquestion,null=False,blank=False,choices=state,default='INACTIVE')
    stu_ans = models.CharField('Answer',max_length=10)
    score = models.IntegerField('Score', default=0)
    qstcode = models.CharField('Question ID',default=0,max_length=10)
    status = models.CharField('Status',default=0,max_length=10)
    no = models.CharField('Count',default=0,max_length=10)
    mark = models.ImageField('Mark', upload_to='studentpix', null=False,blank=False,default='studentpix/user.png')

    def __unicode__(self):
        return u'%s-%s-%s' %(self.exam_type,self.subject,self.score)



class scheduled(models.Model):
    session = models.CharField('Session', max_length=375)
    assessment = models.CharField('Exam_type', max_length=75)
    student = models.ForeignKey(Student, max_length=75, null=True, blank=True)
    subject = models.CharField('Subject', max_length=20)
    term = models.CharField('Term',max_length=10)
   
    def __unicode__(self):
        return u'%s-%s-%s' %(self.assessment,self.subject,self.term)




class donesubjects(models.Model):
    session = models.CharField('Session', max_length=375)
    exam_type = models.CharField('Exam_type', max_length=75)
    student = models.ForeignKey(Student, max_length=75, null=True, blank=True)
    subject = models.CharField('Subject', max_length=20)
    term = models.CharField('Term',max_length=10)


    def __unicode__(self):
        return u'%s-%s-%s' %(self.exam_type,self.subject,self.term)



class cbtcurrentquestion(models.Model):
    session = models.CharField('Session', max_length=375)
    exam_type = models.CharField('Exam_type', max_length=75)
    student = models.ForeignKey(Student, max_length=75, null=True, blank=True)
    subject = models.CharField('Subject', max_length=20)
    term = models.CharField('Term',max_length=10)
    number = models.CharField('number',max_length=10)

    def __unicode__(self):
        return u'%s-%s-%s-%s' %(self.exam_type,self.subject,self.student,self.number)



class cbtold(models.Model):
    session = models.CharField('Session', max_length=375)
    exam_type = models.CharField('Exam_type', max_length=75)
    student = models.ForeignKey(Student, max_length=75, null=True, blank=True)
    subject = models.CharField('Subject', max_length=20)
    term = models.CharField('Term',max_length=10)
    question = models.ForeignKey(tblquestion,null=False,blank=False,choices=state,default='INACTIVE')
    klass = models.CharField('Class',max_length=10)
    qstcode = models.CharField('Question ID',default=0, max_length=10)

    def __unicode__(self):

        return  u'%s %s %s %s' % (self.qstcode,self.subject)


        # return u' code : %s ,subject : %s , term : %s' % (self.qstcode,self.subject,self.term)
        