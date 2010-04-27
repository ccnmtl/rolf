from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
import os.path
admin.autodiscover()
import staticmedia
from rolf_main.models import Category, Application, Deployment, Push, Recipe

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


site_media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
                       (r'^$','rolf_main.views.index'),
                       (r'category/add/','rolf_main.views.add_category'),
                       (r'category/(?P<object_id>\d+)/$','django.views.generic.list_detail.object_detail',category_info_dict),
                       (r'category/(?P<object_id>\d+)/add_application/$','rolf_main.views.add_application'),
                       (r'application/(?P<object_id>\d+)/$','django.views.generic.list_detail.object_detail',application_info_dict),
                       (r'application/(?P<object_id>\d+)/add_deployment/$','rolf_main.views.add_deployment'),
                       (r'deployment/(?P<object_id>\d+)/$','django.views.generic.list_detail.object_detail',deployment_info_dict),
                       (r'deployment/(?P<object_id>\d+)/add_setting/$','rolf_main.views.add_setting'),
                       (r'deployment/(?P<object_id>\d+)/edit_settings/$','rolf_main.views.edit_settings'),
                       (r'deployment/(?P<object_id>\d+)/add_stage/$','rolf_main.views.add_stage'),
                       (r'deployment/(?P<object_id>\d+)/clone/$','rolf_main.views.clone_deployment'),
                       (r'deployment/(?P<object_id>\d+)/push/$','rolf_main.views.push'),
                       (r'push/(?P<object_id>\d+)/$','django.views.generic.list_detail.object_detail',push_info_dict),
                       (r'push/(?P<object_id>\d+)/stage/$','rolf_main.views.stage'),
                       (r'cookbook/$','rolf_main.views.cookbook'),
                       (r'cookbook/(?P<object_id>\d+)/$','django.views.generic.list_detail.object_detail',recipe_info_dict),
                       (r'cookbook/(?P<object_id>\d+)/edit/$','rolf_main.views.edit_recipe'),
                       (r'cookbook/(?P<object_id>\d+)/delete/$','django.views.generic.create_update.delete_object',dict(model=Recipe,
                                                                                                                        post_delete_redirect="/cookbook/")),
                       (r'cookbook/add/$','rolf_main.views.add_cookbook_recipe'),
                       ('^accounts/',include('djangowind.urls')),
                       (r'^admin/(.*)', admin.site.root),
		       (r'^survey/',include('survey.urls')),
                       (r'^tinymce/', include('tinymce.urls')),
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media_root}),
                       (r'^uploads/(?P<path>.*)$','django.views.static.serve',{'document_root' : settings.MEDIA_ROOT}),
) + staticmedia.serve()

