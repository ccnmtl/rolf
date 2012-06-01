# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Deployment.deprecated'
        db.add_column('rolf_main_deployment', 'deprecated', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Deployment.deprecated'
        db.delete_column('rolf_main_deployment', 'deprecated')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'rolf_main.application': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Application'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rolf_main.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'rolf_main.category': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'rolf_main.deployment': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Deployment'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rolf_main.Application']"}),
            'deprecated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'prod'", 'max_length': "'256'"})
        },
        'rolf_main.flag': {
            'Meta': {'object_name': 'Flag'},
            'boolean': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'default': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'deployment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rolf_main.Deployment']"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'varname': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'rolf_main.flagvalue': {
            'Meta': {'object_name': 'FlagValue'},
            'flag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rolf_main.Flag']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'push': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rolf_main.Push']"}),
            'value': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'})
        },
        'rolf_main.log': {
            'Meta': {'object_name': 'Log'},
            'command': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pushstage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rolf_main.PushStage']"}),
            'stderr': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'stdout': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'rolf_main.permission': {
            'Meta': {'object_name': 'Permission'},
            'capability': ('django.db.models.fields.CharField', [], {'default': "'view'", 'max_length': '16'}),
            'deployment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rolf_main.Deployment']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'rolf_main.push': {
            'Meta': {'ordering': "('-start_time',)", 'object_name': 'Push'},
            'comment': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'deployment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rolf_main.Deployment']"}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rollback_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'inprogress'", 'max_length': '256'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'rolf_main.pushstage': {
            'Meta': {'object_name': 'PushStage'},
            'end_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'push': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rolf_main.Push']"}),
            'stage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rolf_main.Stage']"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'inprogress'", 'max_length': '256'})
        },
        'rolf_main.recipe': {
            'Meta': {'ordering': "['name']", 'object_name': 'Recipe'},
            'code': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'python'", 'max_length': '256'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'})
        },
        'rolf_main.setting': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Setting'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'deployment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rolf_main.Deployment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'value': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'rolf_main.stage': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Stage'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'deployment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rolf_main.Deployment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rolf_main.Recipe']"})
        }
    }

    complete_apps = ['rolf_main']
