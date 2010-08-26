from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
import os.path
admin.autodiscover()
from rolf_main.models import Category, Application, Deployment, Push, Recipe, Stage

category_info_dict = {
    'queryset': Category.objects.all(),
    'template_name' : 'rolf/category_detail.html',
}

application_info_dict = {
    'queryset': Application.objects.all(),
    'template_name' : 'rolf/application_detail.html',
}

deployment_info_dict = {
    'queryset': Deployment.objects.all(),
    'template_name' : 'rolf/deployment_detail.html',
}

push_info_dict = {
    'queryset': Push.objects.all(),
    'template_name' : 'rolf/push_detail.html',
}

recipe_info_dict = {
    'queryset': Recipe.objects.all(),
    'template_name' : 'rolf/recipe_detail.html',
}

stage_info_dict = {
    'queryset': Stage.objects.all(),
    'template_name' : 'rolf/stage_detail.html',
}


site_media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
                       (r'^$','rolf_main.views.index'),
                       (r'category/add/','rolf_main.views.add_category'),
                       (r'category/(?P<object_id>\d+)/$','django.views.generic.list_detail.object_detail',category_info_dict),
                       (r'category/(?P<object_id>\d+)/add_application/$','rolf_main.views.add_application'),
                       (r'category/(?P<object_id>\d+)/delete/$','django.views.generic.create_update.delete_object',dict(model=Category,post_delete_redirect="/")),

                       (r'application/(?P<object_id>\d+)/$','django.views.generic.list_detail.object_detail',application_info_dict),
                       (r'application/(?P<object_id>\d+)/add_deployment/$','rolf_main.views.add_deployment'),
                       (r'application/(?P<object_id>\d+)/delete/$','django.views.generic.create_update.delete_object',dict(model=Application,post_delete_redirect="/")),

                       (r'deployment/(?P<object_id>\d+)/$','django.views.generic.list_detail.object_detail',deployment_info_dict),
                       (r'deployment/(?P<object_id>\d+)/add_setting/$','rolf_main.views.add_setting'),
                       (r'deployment/(?P<object_id>\d+)/edit_settings/$','rolf_main.views.edit_settings'),
                       (r'deployment/(?P<object_id>\d+)/add_stage/$','rolf_main.views.add_stage'),
                       (r'deployment/(?P<object_id>\d+)/clone/$','rolf_main.views.clone_deployment'),
                       (r'deployment/(?P<object_id>\d+)/push/$','rolf_main.views.push'),
                       (r'deployment/(?P<object_id>\d+)/rollback/$','rolf_main.views.rollback'),
                       (r'deployment/(?P<object_id>\d+)/reorder_stages/$','rolf_main.views.reorder_stages'),
                       (r'deployment/(?P<object_id>\d+)/delete/$','django.views.generic.create_update.delete_object',dict(model=Deployment,post_delete_redirect="/")),

                       (r'push/(?P<object_id>\d+)/$','django.views.generic.list_detail.object_detail',push_info_dict),
                       (r'push/(?P<object_id>\d+)/stage/$','rolf_main.views.stage'),
                       (r'push/(?P<object_id>\d+)/delete/$','django.views.generic.create_update.delete_object',dict(model=Push,post_delete_redirect="/")),

                       (r'cookbook/$','rolf_main.views.cookbook'),
                       (r'cookbook/(?P<object_id>\d+)/$','django.views.generic.list_detail.object_detail',recipe_info_dict),
                       (r'cookbook/(?P<object_id>\d+)/edit/$','rolf_main.views.edit_recipe'),
                       (r'cookbook/(?P<object_id>\d+)/delete/$','django.views.generic.create_update.delete_object',dict(model=Recipe,post_delete_redirect="/cookbook/")),
                       (r'cookbook/add/$','rolf_main.views.add_cookbook_recipe'),

                       (r'stage/(?P<object_id>\d+)/$','django.views.generic.list_detail.object_detail',stage_info_dict),
                       (r'stage/(?P<object_id>\d+)/edit/$','rolf_main.views.edit_stage'),
                       (r'stage/(?P<object_id>\d+)/delete/$','django.views.generic.create_update.delete_object',dict(model=Stage,post_delete_redirect="/")),

                       ('^accounts/',include('djangowind.urls')),
                       (r'^admin/(.*)', admin.site.root),
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media_root}),
                       (r'^uploads/(?P<path>.*)$','django.views.static.serve',{'document_root' : settings.MEDIA_ROOT}),
) 

