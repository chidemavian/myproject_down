# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'tblcbtsubject.exam_type'
        db.add_column(u'CBT_tblcbtsubject', 'exam_type',
                      self.gf('django.db.models.fields.CharField')(default='N/A', max_length=75),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'tblcbtsubject.exam_type'
        db.delete_column(u'CBT_tblcbtsubject', 'exam_type')


    models = {
        u'CBT.cbtcurrentquestion': {
            'Meta': {'object_name': 'cbtcurrentquestion'},
            'exam_type': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '375'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'max_length': '75', 'to': u"orm['student.Student']", 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'CBT.cbtold': {
            'Meta': {'object_name': 'cbtold'},
            'exam_type': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'klass': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'qstcode': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '10'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'default': "'INACTIVE'", 'to': u"orm['CBT.tblquestion']"}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '375'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'max_length': '75', 'to': u"orm['student.Student']", 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'CBT.cbttrans': {
            'Meta': {'object_name': 'cbttrans'},
            'exam_type': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mark': ('django.db.models.fields.files.ImageField', [], {'default': "'studentpix/user.png'", 'max_length': '100'}),
            'no': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '10'}),
            'qstcode': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '10'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'default': "'INACTIVE'", 'to': u"orm['CBT.tblquestion']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '375'}),
            'status': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '10'}),
            'stu_ans': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'max_length': '75', 'to': u"orm['student.Student']", 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'CBT.donesubjects': {
            'Meta': {'object_name': 'donesubjects'},
            'exam_type': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '375'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'max_length': '75', 'to': u"orm['student.Student']", 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'CBT.scheduled': {
            'Meta': {'object_name': 'scheduled'},
            'assessment': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '375'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'max_length': '75', 'to': u"orm['student.Student']", 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'CBT.tblans': {
            'Meta': {'object_name': 'tblans'},
            'ans': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '7500'}),
            'qstn': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Transaction'", 'to': u"orm['CBT.tblquestion']"})
        },
        u'CBT.tblcbtexams': {
            'Meta': {'object_name': 'tblcbtexams'},
            'exam_type': ('django.db.models.fields.CharField', [], {'max_length': '375'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '75'})
        },
        u'CBT.tblcbtsubject': {
            'Meta': {'object_name': 'tblcbtsubject'},
            'duration': ('django.db.models.fields.CharField', [], {'max_length': '375'}),
            'exam_type': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'klass': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'INACTIVE'", 'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'CBT.tblcbtuser': {
            'Meta': {'object_name': 'tblcbtuser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'klass': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '375', 'null': 'True', 'blank': 'True'})
        },
        u'CBT.tbloptioni': {
            'Meta': {'object_name': 'tbloptioni'},
            'a': ('django.db.models.fields.files.ImageField', [], {'default': "'questions/user.png'", 'max_length': '100'}),
            'b': ('django.db.models.fields.files.ImageField', [], {'default': "'questions/user.png'", 'max_length': '100'}),
            'c': ('django.db.models.fields.files.ImageField', [], {'default': "'questions/user.png'", 'max_length': '100'}),
            'd': ('django.db.models.fields.files.ImageField', [], {'default': "'questions/user.png'", 'max_length': '100'}),
            'e': ('django.db.models.fields.files.ImageField', [], {'default': "'questions/user.png'", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'qstn': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Optioni'", 'to': u"orm['CBT.tblquestion']"})
        },
        u'CBT.tbloptions': {
            'Meta': {'object_name': 'tbloptions'},
            'a': ('django.db.models.fields.CharField', [], {'max_length': '7500'}),
            'b': ('django.db.models.fields.CharField', [], {'max_length': '7500'}),
            'c': ('django.db.models.fields.CharField', [], {'max_length': '7500'}),
            'd': ('django.db.models.fields.CharField', [], {'max_length': '7500'}),
            'e': ('django.db.models.fields.CharField', [], {'max_length': '7500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'qstn': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Options'", 'to': u"orm['CBT.tblquestion']"})
        },
        u'CBT.tblquestion': {
            'Meta': {'object_name': 'tblquestion'},
            'exam_type': ('django.db.models.fields.CharField', [], {'max_length': '375'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "'studentpix/user.png'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'instruction_from': ('django.db.models.fields.CharField', [], {'max_length': '975'}),
            'instruction_to': ('django.db.models.fields.CharField', [], {'max_length': '975'}),
            'klass': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'qstn': ('django.db.models.fields.CharField', [], {'max_length': '975'}),
            'section': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '20'}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'})
        },
        u'CBT.tbltheory': {
            'Meta': {'object_name': 'tbltheory'},
            'exam_type': ('django.db.models.fields.CharField', [], {'max_length': '375'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "'questions/user.png'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'instruction_from': ('django.db.models.fields.CharField', [], {'max_length': '975'}),
            'instruction_to': ('django.db.models.fields.CharField', [], {'max_length': '975'}),
            'klass': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '375', 'null': 'True', 'blank': 'True'})
        },
        u'student.student': {
            'Meta': {'ordering': "['fullname']", 'object_name': 'Student'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'admissionno': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'admitted_arm': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'admitted_class': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'admitted_session': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'default': "'2000-01-01'", 'null': 'True', 'blank': 'True'}),
            'birth_place': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'dayboarding': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'fatheraddress': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'fatheremail': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'fathername': ('django.db.models.fields.CharField', [], {'max_length': '275'}),
            'fathernumber': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'fatheroccupation': ('django.db.models.fields.CharField', [], {'max_length': '175'}),
            'first_term': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'gone': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'house': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lga': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'othername': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'prev_class': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'prev_school': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'second_term': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'state_of_origin': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'studentpicture': ('django.db.models.fields.files.ImageField', [], {'default': "'studentpix/user.png'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'subclass': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'third_term': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'userid': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['CBT']