from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=256)
    
class Application(models.Model):
    name = models.CharField(max_length=256)
    category = models.ForeignKey(Category)
    
    class Meta:
        order_with_respect_to = "category"

class Deployment(models.Model):
    name = models.CharField(max_length="256",default="prod")
    application = models.ForeignKey(Application)
    
    class Meta:
        order_with_respect_to = "application"

class Setting(models.Model):
    deployment = models.ForeignKey(Deployment)
    name = models.CharField(max_length=256)
    value = models.TextField(blank=True,default="")

    class Meta:
        order_with_respect_to = "deployment"

class Recipe(models.Model):
    name = models.CharField(max_length=256,blank=True,default="")
    code = models.TextField(blank=True,default="")
    language = models.CharField(max_length=256,default="python")
    description = models.TextField(blank=True,default="")
    
class Stage(models.Model):
    name = models.CharField(max_length=256)
    deployment = models.ForeignKey(Deployment)
    recipe = models.ForeignKey(Recipe)
    
    class Meta:
        order_with_respect_to = "deployment"

class Push(models.Model):
    user = models.ForeignKey(User)
    deployment = models.ForeignKey(Deployment)
    comment = models.TextField(blank=True,default="")
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=256,default="inprogress")
    rollback_url = models.CharField(max_length=256,blank=True,default="")

    class Meta:
        ordering = ('-start_time',)

class PushStage(models.Model):
    push = models.ForeignKey(Push)
    stage = models.ForeignKey(Stage)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=256,default="inprogress")

class Log(models.Model):
    pushstage = models.ForeignKey(PushStage)
    command = models.TextField(blank=True,default="")
    stdout = models.TextField(blank=True,default="")
    stderr = models.TextField(blank=True,default="")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    

