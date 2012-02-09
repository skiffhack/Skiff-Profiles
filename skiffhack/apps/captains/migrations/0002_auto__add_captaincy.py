# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Captaincy'
        db.create_table('captains_captaincy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('starts_on', self.gf('django.db.models.fields.DateField')()),
            ('hash', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('captains', ['Captaincy'])


    def backwards(self, orm):
        
        # Deleting model 'Captaincy'
        db.delete_table('captains_captaincy')


    models = {
        'captains.captaincy': {
            'Meta': {'object_name': 'Captaincy'},
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'starts_on': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['captains']
