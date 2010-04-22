from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
import os.path
admin.autodiscover()
import staticmedia
from rolf_main.models import Category, Application, Deployment

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
                       ('^accounts/',include('djangowind.urls')),
                       (r'^admin/(.*)', admin.site.root),
		       (r'^survey/',include('survey.urls')),
                       (r'^tinymce/', include('tinymce.urls')),
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media_root}),
                       (r'^uploads/(?P<path>.*)$','django.views.static.serve',{'document_root' : settings.MEDIA_ROOT}),
) + staticmedia.serve()

