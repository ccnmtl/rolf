# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Deployment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'prod', max_length=b'256')),
                ('deprecated', models.BooleanField(default=False, help_text=b"Check this box if you don't want this deployment to show up by default.")),
                ('application', models.ForeignKey(to='rolf_main.Application')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Flag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('varname', models.CharField(help_text=b'Bash/Python variable name. UPPERCASE_AND_UNDERSCORES recommended', max_length=256)),
                ('default', models.CharField(default=b'', help_text=b'leave empty for False on boolean fields', max_length=256, blank=True)),
                ('boolean', models.BooleanField(default=False, help_text=b'make it a checkbox')),
                ('description', models.TextField(default=b'', blank=True)),
                ('deployment', models.ForeignKey(to='rolf_main.Deployment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FlagValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(default=b'', max_length=256)),
                ('flag', models.ForeignKey(to='rolf_main.Flag')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('command', models.TextField(default=b'', blank=True)),
                ('stdout', models.TextField(default=b'', blank=True)),
                ('stderr', models.TextField(default=b'', blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('capability', models.CharField(default=b'view', max_length=16, choices=[(b'view', b'View'), (b'push', b'Push'), (b'edit', b'Edit')])),
                ('deployment', models.ForeignKey(to='rolf_main.Deployment')),
                ('group', models.ForeignKey(to='auth.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Push',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField(default=b'', blank=True)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default=b'inprogress', max_length=256)),
                ('rollback_url', models.CharField(default=b'', max_length=256, blank=True)),
                ('deployment', models.ForeignKey(to='rolf_main.Deployment')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-start_time',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PushStage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default=b'inprogress', max_length=256)),
                ('push', models.ForeignKey(to='rolf_main.Push')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=256, blank=True)),
                ('code', models.TextField(default=b'', blank=True)),
                ('language', models.CharField(default=b'python', max_length=256)),
                ('description', models.TextField(default=b'', blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('value', models.TextField(default=b'', blank=True)),
                ('deployment', models.ForeignKey(to='rolf_main.Deployment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('deployment', models.ForeignKey(to='rolf_main.Deployment')),
                ('recipe', models.ForeignKey(to='rolf_main.Recipe')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterOrderWithRespectTo(
            name='stage',
            order_with_respect_to='deployment',
        ),
        migrations.AlterOrderWithRespectTo(
            name='setting',
            order_with_respect_to='deployment',
        ),
        migrations.AddField(
            model_name='pushstage',
            name='stage',
            field=models.ForeignKey(to='rolf_main.Stage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='log',
            name='pushstage',
            field=models.ForeignKey(to='rolf_main.PushStage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='flagvalue',
            name='push',
            field=models.ForeignKey(to='rolf_main.Push'),
            preserve_default=True,
        ),
        migrations.AlterOrderWithRespectTo(
            name='deployment',
            order_with_respect_to='application',
        ),
        migrations.AddField(
            model_name='application',
            name='category',
            field=models.ForeignKey(to='rolf_main.Category'),
            preserve_default=True,
        ),
        migrations.AlterOrderWithRespectTo(
            name='application',
            order_with_respect_to='category',
        ),
    ]
