from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic.edit import DeleteView
from rolf.rolf_main.models import Category, Application, Deployment
from rolf.rolf_main.models import Push, Recipe, Stage
from rolf.rolf_main.views import DeleteStageView
admin.autodiscover()

category_info_dict = {
    'model': Category,
    'template_name': 'rolf/category_detail.html',
}

application_info_dict = {
    'model': Application,
    'template_name': 'rolf/application_detail.html',
}

deployment_info_dict = {
    'model': Deployment,
    'template_name': 'rolf/deployment_detail.html',
}

push_info_dict = {
    'model': Push,
    'template_name': 'rolf/push_detail.html',
}

stage_info_dict = {
    'model': Stage,
    'template_name': 'rolf/stage_detail.html',
}

recipe_info_dict = {
    'model': Recipe,
    'template_name': 'rolf/recipe_detail.html',
}


accounts_tuple = (r'^accounts/', include('django.contrib.auth.urls'))

urlpatterns = patterns(
    '',
    (r'^$', 'rolf.rolf_main.views.index'),
    (r'^category/add/', 'rolf.rolf_main.views.add_category'),
    (r'^category/(?P<object_id>\d+)/$',
     'rolf.rolf_main.views.generic_detail', category_info_dict),
    (r'^category/(?P<object_id>\d+)/add_application/$',
     'rolf.rolf_main.views.add_application'),
    (r'^category/(?P<pk>\d+)/delete/$',
     DeleteView.as_view(model=Category, success_url="/")),

    (r'^application/(?P<object_id>\d+)/$',
     'rolf.rolf_main.views.generic_detail', application_info_dict),
    (r'^application/(?P<object_id>\d+)/add_deployment/$',
     'rolf.rolf_main.views.add_deployment'),
    (r'^application/(?P<pk>\d+)/delete/$',
     DeleteView.as_view(model=Application, success_url="/")),

    url(r'^deployment/(?P<object_id>\d+)/$',
        'rolf.rolf_main.views.generic_detail',
        deployment_info_dict,
        name='deployment_detail'),
    (r'^deployment/(?P<object_id>\d+)/add_setting/$',
     'rolf.rolf_main.views.add_setting'),
    (r'^deployment/(?P<object_id>\d+)/edit_settings/$',
     'rolf.rolf_main.views.edit_settings'),
    (r'^deployment/(?P<object_id>\d+)/add_stage/$',
     'rolf.rolf_main.views.add_stage'),
    (r'^deployment/(?P<object_id>\d+)/clone/$',
     'rolf.rolf_main.views.clone_deployment'),
    (r'^deployment/(?P<object_id>\d+)/push/$',
     'rolf.rolf_main.views.push'),
    (r'^deployment/(?P<object_id>\d+)/remove_permission/$',
     'rolf.rolf_main.views.remove_permission'),
    (r'^deployment/(?P<object_id>\d+)/add_permission/$',
     'rolf.rolf_main.views.add_permission'),

    (r'^deployment/(?P<object_id>\d+)/remove_flag/$',
     'rolf.rolf_main.views.remove_flag'),
    (r'^deployment/(?P<object_id>\d+)/add_flag/$',
     'rolf.rolf_main.views.add_flag'),

    (r'^deployment/(?P<object_id>\d+)/rollback/$',
     'rolf.rolf_main.views.rollback'),
    (r'^deployment/(?P<object_id>\d+)/reorder_stages/$',
     'rolf.rolf_main.views.reorder_stages'),
    (r'^deployment/(?P<pk>\d+)/delete/$',
     DeleteView.as_view(model=Deployment, success_url="/")),

    (r'^push/(?P<object_id>\d+)/$',
     'rolf.rolf_main.views.generic_detail', push_info_dict),
    (r'^push/(?P<object_id>\d+)/stage/$', 'rolf.rolf_main.views.stage'),
    (r'^push/(?P<pk>\d+)/delete/$',
     DeleteView.as_view(model=Push, success_url="/")),

    (r'^cookbook/$', 'rolf.rolf_main.views.cookbook'),
    (r'^cookbook/(?P<object_id>\d+)/$',
     'rolf.rolf_main.views.generic_detail', recipe_info_dict),
    (r'^cookbook/(?P<object_id>\d+)/edit/$',
     'rolf.rolf_main.views.edit_recipe'),
    (r'^cookbook/(?P<pk>\d+)/delete/$',
     DeleteView.as_view(model=Recipe, success_url="/cookbook/")),
    (r'^cookbook/add/$', 'rolf.rolf_main.views.add_cookbook_recipe'),

    (r'^stage/(?P<object_id>\d+)/$',
     'rolf.rolf_main.views.generic_detail', stage_info_dict),
    (r'^stage/(?P<object_id>\d+)/edit/$', 'rolf.rolf_main.views.edit_stage'),
    url(r'^stage/(?P<pk>\d+)/delete/$', DeleteStageView.as_view(),
        name='stage_delete'),

    (r'^api/1.0/get_key/$',
     'rolf.rolf_main.views.get_api_key'),
    (r'^api/1.0/deployment/(?P<deployment_id>\d+)/push/$',
     'rolf.rolf_main.views.api_push'),
    (r'^api/1.0/push/(?P<push_id>\d+)/stage/(?P<stage_id>\d+)/$',
     'rolf.rolf_main.views.api_run_stage'),

    (r'^accounts/', include('djangowind.urls')),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    (r'^admin/', include(admin.site.urls)),
    (r'^stats/$', TemplateView.as_view(template_name="stats.html")),
    (r'smoketest/', include('smoketest.urls')),
    (r'^uploads/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
