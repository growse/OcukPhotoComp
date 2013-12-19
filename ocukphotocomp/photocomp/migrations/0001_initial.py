# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table(u'people', (
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'photocomp', ['Person'])

        # Adding model 'Season'
        db.create_table(u'seasons', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('complete', self.gf('django.db.models.fields.BooleanField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'photocomp', ['Season'])

        # Adding model 'Round'
        db.create_table(u'rounds', (
            ('theme', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['photocomp.Season'], db_column='season')),
        ))
        db.send_create_signal(u'photocomp', ['Round'])

        # Adding model 'Entry'
        db.create_table(u'entries', (
            ('technical_score', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('theme_score', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('impact_score', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('total_score', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['photocomp.Person'], db_column='person')),
            ('round', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['photocomp.Round'], db_column='round')),
            ('comments', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'photocomp', ['Entry'])


    def backwards(self, orm):
        # Deleting model 'Person'
        db.delete_table(u'people')

        # Deleting model 'Season'
        db.delete_table(u'seasons')

        # Deleting model 'Round'
        db.delete_table(u'rounds')

        # Deleting model 'Entry'
        db.delete_table(u'entries')


    models = {
        u'photocomp.entry': {
            'Meta': {'object_name': 'Entry', 'db_table': "u'entries'"},
            'comments': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impact_score': ('django.db.models.fields.SmallIntegerField', [], {}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['photocomp.Person']", 'db_column': "'person'"}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['photocomp.Round']", 'db_column': "'round'"}),
            'technical_score': ('django.db.models.fields.SmallIntegerField', [], {}),
            'theme_score': ('django.db.models.fields.SmallIntegerField', [], {}),
            'total_score': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        u'photocomp.person': {
            'Meta': {'object_name': 'Person', 'db_table': "u'people'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'photocomp.round': {
            'Meta': {'object_name': 'Round', 'db_table': "u'rounds'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['photocomp.Season']", 'db_column': "'season'"}),
            'theme': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'photocomp.season': {
            'Meta': {'object_name': 'Season', 'db_table': "u'seasons'"},
            'complete': ('django.db.models.fields.BooleanField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['photocomp']