from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.views.generic.simple import direct_to_template
import os.path
admin.autodiscover()
from rolf_main.models import Category, Application, Deployment, Push, Recipe, Stage

category_info_dict = {
    'model': Category,
    'template_name' : 'rolf/category_detail.html',
}

application_info_dict = {
    'model': Application,
    'template_name' : 'rolf/application_detail.html',
}

deployment_info_dict = {
    'model': Deployment,
    'template_name' : 'rolf/deployment_detail.html',
}

push_info_dict = {
    'model': Push,
    'template_name' : 'rolf/push_detail.html',
}

stage_info_dict = {
    'model': Stage,
    'template_name' : 'rolf/stage_detail.html',
}

recipe_info_dict = {
    'model': Recipe,
    'template_name' : 'rolf/recipe_detail.html',
}


site_media_root = os.path.join(os.path.dirname(__file__),"media")

accounts_tuple = (r'^accounts/',include('django.contrib.auth.urls'))

if hasattr(settings,'WIND_BASE'):
    # we have a centralized auth system at Columbia,
    # so if that is configured (in local_settings), use it
    # instead of regular django auth
    accounts_tuple = ('^accounts/',include('djangowind.urls'))

urlpatterns = patterns('',
                       (r'^$','rolf_main.views.index'),
                       (r'^category/add/','rolf_main.views.add_category'),
                       (r'^category/(?P<object_id>\d+)/$','rolf_main.views.generic_detail',category_info_dict),
                       (r'^category/(?P<object_id>\d+)/add_application/$','rolf_main.views.add_application'),
                       (r'^category/(?P<object_id>\d+)/delete/$','django.views.generic.create_update.delete_object',dict(model=Category,post_delete_redirect="/")),

                       (r'^application/(?P<object_id>\d+)/$','rolf_main.views.generic_detail',application_info_dict),
                       (r'^application/(?P<object_id>\d+)/add_deployment/$','rolf_main.views.add_deployment'),
                       (r'^application/(?P<object_id>\d+)/delete/$','django.views.generic.create_update.delete_object',dict(model=Application,post_delete_redirect="/")),

                       (r'^deployment/(?P<object_id>\d+)/$','rolf_main.views.generic_detail',deployment_info_dict),
                       (r'^deployment/(?P<object_id>\d+)/add_setting/$','rolf_main.views.add_setting'),
                       (r'^deployment/(?P<object_id>\d+)/edit_settings/$','rolf_main.views.edit_settings'),
                       (r'^deployment/(?P<object_id>\d+)/add_stage/$','rolf_main.views.add_stage'),
                       (r'^deployment/(?P<object_id>\d+)/clone/$','rolf_main.views.clone_deployment'),
                       (r'^deployment/(?P<object_id>\d+)/push/$','rolf_main.views.push'),
                       (r'^deployment/(?P<object_id>\d+)/remove_permission/$','rolf_main.views.remove_permission'),
                       (r'^deployment/(?P<object_id>\d+)/add_permission/$','rolf_main.views.add_permission'),

                       (r'^deployment/(?P<object_id>\d+)/remove_flag/$','rolf_main.views.remove_flag'),
                       (r'^deployment/(?P<object_id>\d+)/add_flag/$','rolf_main.views.add_flag'),

                       (r'^deployment/(?P<object_id>\d+)/rollback/$','rolf_main.views.rollback'),
                       (r'^deployment/(?P<object_id>\d+)/reorder_stages/$','rolf_main.views.reorder_stages'),
                       (r'^deployment/(?P<object_id>\d+)/delete/$','django.views.generic.create_update.delete_object',dict(model=Deployment,post_delete_redirect="/")),

                       (r'^push/(?P<object_id>\d+)/$','rolf_main.views.generic_detail',push_info_dict),
                       (r'^push/(?P<object_id>\d+)/stage/$','rolf_main.views.stage'),
                       (r'^push/(?P<object_id>\d+)/delete/$','django.views.generic.create_update.delete_object',dict(model=Push,post_delete_redirect="/")),

                       (r'^cookbook/$','rolf_main.views.cookbook'),
                       (r'^cookbook/(?P<object_id>\d+)/$','rolf_main.views.generic_detail',recipe_info_dict),
                       (r'^cookbook/(?P<object_id>\d+)/edit/$','rolf_main.views.edit_recipe'),
                       (r'^cookbook/(?P<object_id>\d+)/delete/$','django.views.generic.create_update.delete_object',dict(model=Recipe,post_delete_redirect="/cookbook/")),
                       (r'^cookbook/add/$','rolf_main.views.add_cookbook_recipe'),

                       (r'^stage/(?P<object_id>\d+)/$','rolf_main.views.generic_detail',stage_info_dict),
                       (r'^stage/(?P<object_id>\d+)/edit/$','rolf_main.views.edit_stage'),
                       (r'^stage/(?P<object_id>\d+)/delete/$','django.views.generic.create_update.delete_object',dict(model=Stage,post_delete_redirect="/")),

                       (r'^api/1.0/get_key/$',
                        'rolf_main.views.get_api_key'),
                       (r'^api/1.0/deployment/(?P<deployment_id>\d+)/push/$',
                        'rolf_main.views.api_push'),
                       (r'^api/1.0/push/(?P<push_id>\d+)/stage/(?P<stage_id>\d+)/$',
                        'rolf_main.views.api_run_stage'),

                       accounts_tuple,
                       (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page':'/'}), 
                     
                       (r'^admin/', include(admin.site.urls)),
                       (r'^stats/total_pushes/$','rolf_main.views.total_pushes'),
                       (r'^stats/current_pushes/$','rolf_main.views.current_pushes'),
                       ('^munin/',include('munin.urls')),
                       (r'^stats/',direct_to_template, {'template': 'stats.html'}),
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media_root}),
                       (r'^uploads/(?P<path>.*)$','django.views.static.serve',{'document_root' : settings.MEDIA_ROOT}),
) 

