from django.db import models



class tbltopic(models.Model):
    klass = models.CharField('Class', max_length= 120)
    subject = models.CharField("Subject",max_length= 230)
    term = models.CharField("Term", max_length= 130)
    topic = models.CharField("Topic", max_length= 2000)
    session = models.CharField('session',max_length=50)
    lessonnote= models.FileField('Note', upload_to='notes', null=True,blank=True,default='notes/sand and foam.docx')

    def __unicode__(self):
        return  u'klass: %s, subject: %s,term: %s, topic: %s, session: %s,id:%s' %(self.klass, self.subject,self.term, self.topic, self.session,self.id)

    
    
    class Meta:
        ordering = ['klass']
        verbose_name_plural = 'Topic Table'

class tblcontents(models.Model):
    topic = models.ForeignKey(tbltopic, related_name='topic id')
    content = models.CharField("Content",max_length= 5000,default = '')

    def __unicode__(self):
         return  u'topic: %s,content: %s,  klass:%s,term:%s,session:%s,id:%s' %(self.topic.topic,self.content,  self.topic.klass, self.topic.term, self.topic.session,self.id)

    class Meta:
        ordering = ['topic']
        verbose_name_plural = 'Contents Table'


class tblir(models.Model):
    topic = models.ForeignKey(tbltopic, related_name='instructional resource')
    resource = models.CharField("Resource",max_length= 5000,default = '')
    example = models.CharField("Example",max_length= 5000,default = '')

    def __unicode__(self):
        return  u'resource: %s,example: %s' %(self.resource, self.example)
        
    class Meta:
        ordering = ['topic']
        verbose_name_plural = 'Instructional resources Table'

class tblobjectives(models.Model):
    content = models.ForeignKey(tblcontents, related_name = 'objectives')
    objectives = models.CharField('objectives', max_length= 130)

    def __unicode__(self):
        return u'content: %s, objectives: %s' %(self.content.content, self.objectives)

class tblteachersActivities(models.Model):
    objectives = models.ForeignKey(tblobjectives, related_name ="teacher's activity")
    teacherActivities = models.CharField("Teacher's Activities", max_length = 500)

    def __unicode__(self):
         return u'teacherActivities: %s' %(self.teacherActivities)


class tblstudentActivities(models.Model):
    teacher_activities = models.ForeignKey(tblteachersActivities, related_name ="teacher's activity")
    studentActivities = models.CharField("Teacher's Activities", max_length = 500)

    def __unicode__(self):
         return u'studentActivities: %s' %(self.studentActivities)


class tblevaluation(models.Model):
    content = models.ForeignKey(tblcontents, related_name='evaluation')
    evaluation = models.CharField('Evaluation Guide',max_length = 500)

    def __unicode__(self):
        return u'content: %s, evaluation: %s ' %(self.content.content, self.evaluation)

class tblwa(models.Model):
    klass = models.CharField('Class',max_length = 50)
    subject= models.CharField('subject',max_length = 50)
    wa = models.CharField('Evaluation Guide',max_length = 5)

    def __unicode__(self):
        return u'wa: %s' %(self.wa)


class tblcalendar(models.Model):
    session = models.CharField('Session',max_length = 500)
    term= models.CharField('Term',max_length = 500)
    st = models.DateField('Start Date',max_length = 15,default='05/09/17')
    end= models.DateField('End Date',max_length = 15)


    def __unicode__(self):
        return u'st: %s, end:%s' %(self.st, self.end)

class tblquest(models.Model):
    session = models.CharField('Session',max_length = 500)
    term= models.CharField('Term',max_length = 500)
    klass= models.CharField('Class',max_length = 500)
    subject = models.CharField('Subject',max_length = 500)
    question= models.FileField('Questions', upload_to='questions',blank=True,default='questions/sand and foam.docx')


    def __unicode__(self):
        return u'questions: %s, session:%s' %(self.questions, self.session)
    
    def det():
        session=session