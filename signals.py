from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save, post_delete
from myproject.student.models import Student
from myproject.academics.models import *

#@receiver(post_save, sender=Student, dispatch_uid='saved new student record')
def prepare_student_academic_record(sender, **kwargs):
    '''available kwargs: sender (model class), instance (actual instance of the model class), raw, created, using'''

    student, created = kwargs.get('instance'), kwargs.get('created')
    if created:
        for term in ['First', 'Second', 'Third']:
            academic_record = StudentAcademicRecord(student=student, klass=student.admitted_class,
                arm=student.admitted_arm, term=term, session=student.admitted_session)
            academic_record.save()
            aff =  AffectiveSkill(academic_rec=academic_record)
            aff.save()
            psyco = PsychomotorSkill(academic_rec=academic_record)
            psyco.save()
            j = student.subclass.count('/')
            if student.subclass.startswith('J'):
              try:
                k= [(s.subject, s.num) for s in Subject.objects.filter(category='JS')]
              except DatabaseError:
                  return []
            elif student.subclass.startswith('A'):
                try:
                   k = [(s.subject, s.num) for s in Subject.objects.filter(category='Art')]
                except DatabaseError:
                    return []
            elif student.subclass.startswith('S') and j == 0:
                try:
                   k = [(s.subject, s.num) for s in Subject.objects.filter(category='Science')]
                except DatabaseError:
                    return []
            elif student.subclass.startswith('S') and j == 1:
                try:
                    k = [(s.subject, s.num) for s in Subject.objects.filter(category='Science/Math')]
                except DatabaseError:
                    return []

            elif student.subclass.startswith('C'):
                try:
                  k = [(s.subject, s.num) for s in Subject.objects.filter(category='Commercial')]
                except DatabaseError:
                  return []

            elif student.subclass.startswith('T'):
                try:
                    k = [(s.subject, s.num) for s in Subject.objects.filter(category='Technology')]
                except DatabaseError:
                    return []
            elif student.subclass.startswith('H'):
                try:
                    k = [(s.subject, s.num) for s in Subject.objects.filter(category='Humanities')]
                except DatabaseError:
                    return []

            elif student.subclass.startswith('B'):
                try:
                    k = [(s.subject, s.num) for s in Subject.objects.filter(category='Business')]
                except DatabaseError:
                    return []

            elif student.subclass.startswith('Y'):
                try:
                    k = [(s.subject, s.num) for s in Subject.objects.filter(category='Year')]
                except DatabaseError:
                    return []
            else:
                try:
                 # k = [(s.subject, s.num) for s in Subject.objects.exclude(category='YEAR')]
                  k = []
                except DatabaseError:
                 return []
            for subject in k:
                SubjectScore(subject=subject[0], academic_rec=academic_record, num=subject[1], term=term,
                    session=student.admitted_session, klass=student.admitted_class, arm=student.admitted_arm).save()



