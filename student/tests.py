"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from myproject.student.models import Student, WithdrawnStudent
from myproject.signals import *
from datetime import datetime

class StudentModelsTest(TestCase):
    def setUp(self):

        student = Student.objects.create(firstname='John',
            surname='Doe', othername='Baxter', address='100 Lincoln Boulevard, Washington DC,',
            sex='M', birth_date=datetime(1980, 1, 1), birth_place='Phoenix', state_of_origin='Nebraska',
            lga='Lincoln', studentpicture='/jdoe.jpg', fathername='Johnny D. Ringo',
            fatheraddress='Omaha, Nebraska', fathernumber='2568291093', fatheroccupation='Engineer',
            mothername='Jane Doe', motheraddress="Same as father's", mothernumber='2779928747',
            motheroccupation='Gold Digger', next_of_kin_name='Jack Bauer', next_of_kin_address='Manhattan NY',
            next_of_kin_number='8747737829', next_of_kin_occupation='CTU', next_of_kin_relationship='Doppelganger',
            prev_school='Harvard University, Cambridge MA', prev_class='Senior', admitted_class='JS 1',
            admitted_arm='A', admitted_session='2012/2013', admitted_term='First', admissionno='2938/378HHSA',
            house='Buckingham Palace', dayboarding='Day')

    def test_student_withdrawal_return(self):
        student = Student.objects.get(pk=1)
        allgone = WithdrawnStudent.objects.all()

        self.assertFalse(student.gone)
        self.assertEqual(allgone.count(), 0)

        student.withdraw_student('Graduated', datetime.now())

        self.assertTrue(student.gone)
        allgone = WithdrawnStudent.objects.all()
        self.assertEqual(allgone.count(), 1)

        student.return_student()

        self.assertFalse(student.gone)
        allgone = WithdrawnStudent.objects.all()
        self.assertEqual(allgone.count(), 0)

    def test_student_academic_records_exists(self):
        student = Student.objects.get(pk=1)
        self.assertEquals(student.academic_record.select_related().count(), 1)