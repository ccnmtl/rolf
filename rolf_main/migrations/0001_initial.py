# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Category'
        db.create_table('rolf_main_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('rolf_main', ['Category'])

        # Adding model 'Application'
        db.create_table('rolf_main_application', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rolf_main.Category'])),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('rolf_main', ['Application'])

        # Adding model 'Deployment'
        db.create_table('rolf_main_deployment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='prod', max_length='256')),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rolf_main.Application'])),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('rolf_main', ['Deployment'])

        # Adding model 'Permission'
        db.create_table('rolf_main_permission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deployment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rolf_main.Deployment'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'])),
            ('capability', self.gf('django.db.models.fields.CharField')(default='view', max_length=16)),
        ))
        db.send_create_signal('rolf_main', ['Permission'])

        # Adding model 'Setting'
        db.create_table('rolf_main_setting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deployment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rolf_main.Deployment'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('value', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('rolf_main', ['Setting'])

        # Adding model 'Recipe'
        db.create_table('rolf_main_recipe', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=256, blank=True)),
            ('code', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='python', max_length=256)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('rolf_main', ['Recipe'])

        # Adding model 'Stage'
        db.create_table('rolf_main_stage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('deployment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rolf_main.Deployment'])),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rolf_main.Recipe'])),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('rolf_main', ['Stage'])

        # Adding model 'Push'
        db.create_table('rolf_main_push', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('deployment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rolf_main.Deployment'])),
            ('comment', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='inprogress', max_length=256)),
            ('rollback_url', self.gf('django.db.models.fields.CharField')(default='', max_length=256, blank=True)),
        ))
        db.send_create_signal('rolf_main', ['Push'])

        # Adding model 'PushStage'
        db.create_table('rolf_main_pushstage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('push', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rolf_main.Push'])),
            ('stage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rolf_main.Stage'])),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='inprogress', max_length=256)),
        ))
        db.send_create_signal('rolf_main', ['PushStage'])

        # Adding model 'Log'
        db.create_table('rolf_main_log', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pushstage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rolf_main.PushStage'])),
            ('command', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('stdout', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('stderr', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('rolf_main', ['Log'])

        # Adding model 'Flag'
        db.create_table('rolf_main_flag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deployment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rolf_main.Deployment'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('varname', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('default', self.gf('django.db.models.fields.CharField')(default='', max_length=256, blank=True)),
            ('boolean', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('rolf_main', ['Flag'])

        # Adding model 'FlagValue'
        db.create_table('rolf_main_flagvalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('flag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rolf_main.Flag'])),
            ('push', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rolf_main.Push'])),
            ('value', self.gf('django.db.models.fields.CharField')(default='', max_length=256)),
        ))
        db.send_create_signal('rolf_main', ['FlagValue'])


    def backwards(self, orm):
        
        # Deleting model 'Category'
        db.delete_table('rolf_main_category')

        # Deleting model 'Application'
        db.delete_table('rolf_main_application')

        # Deleting model 'Deployment'
        db.delete_table('rolf_main_deployment')

        # Deleting model 'Permission'
        db.delete_table('rolf_main_permission')

        # Deleting model 'Setting'
        db.delete_table('rolf_main_setting')

        # Deleting model 'Recipe'
        db.delete_table('rolf_main_recipe')

        # Deleting model 'Stage'
        db.delete_table('rolf_main_stage')

        # Deleting model 'Push'
        db.delete_table('rolf_main_push')

        # Deleting model 'PushStage'
        db.delete_table('rolf_main_pushstage')

        # Deleting model 'Log'
        db.delete_table('rolf_main_log')

        # Deleting model 'Flag'
        db.delete_table('rolf_main_flag')

        # Deleting model 'FlagValue'
        db.delete_table('rolf_main_flagvalue')


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
