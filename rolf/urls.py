import django.contrib.auth.views
import django.views.static

from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic.edit import DeleteView
from rolf.rolf_main.models import Category, Application, Deployment
from rolf.rolf_main.models import Push, Recipe, Stage
from rolf.rolf_main.views import (
    DeleteStageView, generic_detail, edit_recipe, add_cookbook_recipe,
    api_push, get_api_key, api_run_stage, cookbook, stage, add_flag,
    remove_flag, add_permission, rollback, reorder_stages, edit_stage,
    push, clone_deployment, add_stage, edit_settings, add_setting,
    add_deployment, remove_permission, add_application,
    add_category, index,
)

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


accounts_tuple = url(r'^accounts/', include('django.contrib.auth.urls'))

urlpatterns = [
    url(r'^$', index),
    url(r'^category/add/', add_category),
    url(r'^category/(?P<object_id>\d+)/$', generic_detail, category_info_dict),
    url(r'^category/(?P<object_id>\d+)/add_application/$', add_application),
    url(r'^category/(?P<pk>\d+)/delete/$', DeleteView.as_view(
        model=Category, success_url="/")),

    url(r'^application/(?P<object_id>\d+)/$', generic_detail,
        application_info_dict),
    url(r'^application/(?P<object_id>\d+)/add_deployment/$', add_deployment),
    url(r'^application/(?P<pk>\d+)/delete/$', DeleteView.as_view(
        model=Application, success_url="/")),

    url(r'^deployment/(?P<object_id>\d+)/$', generic_detail,
        deployment_info_dict, name='deployment_detail'),
    url(r'^deployment/(?P<object_id>\d+)/add_setting/$', add_setting),
    url(r'^deployment/(?P<object_id>\d+)/edit_settings/$', edit_settings),
    url(r'^deployment/(?P<object_id>\d+)/add_stage/$', add_stage),
    url(r'^deployment/(?P<object_id>\d+)/clone/$', clone_deployment),
    url(r'^deployment/(?P<object_id>\d+)/push/$', push),
    url(r'^deployment/(?P<object_id>\d+)/remove_permission/$',
        remove_permission),
    url(r'^deployment/(?P<object_id>\d+)/add_permission/$', add_permission),

    url(r'^deployment/(?P<object_id>\d+)/remove_flag/$', remove_flag),
    url(r'^deployment/(?P<object_id>\d+)/add_flag/$', add_flag),

    url(r'^deployment/(?P<object_id>\d+)/rollback/$', rollback),
    url(r'^deployment/(?P<object_id>\d+)/reorder_stages/$', reorder_stages),
    url(r'^deployment/(?P<pk>\d+)/delete/$', DeleteView.as_view(
        model=Deployment, success_url="/")),

    url(r'^push/(?P<object_id>\d+)/$', generic_detail, push_info_dict),
    url(r'^push/(?P<object_id>\d+)/stage/$', stage),
    url(r'^push/(?P<pk>\d+)/delete/$', DeleteView.as_view(
        model=Push, success_url="/")),

    url(r'^cookbook/$', cookbook),
    url(r'^cookbook/(?P<object_id>\d+)/$', generic_detail, recipe_info_dict),
    url(r'^cookbook/(?P<object_id>\d+)/edit/$', edit_recipe),
    url(r'^cookbook/(?P<pk>\d+)/delete/$', DeleteView.as_view(
        model=Recipe, success_url="/cookbook/")),
    url(r'^cookbook/add/$', add_cookbook_recipe),
    url(r'^stage/(?P<object_id>\d+)/$', generic_detail, stage_info_dict),
    url(r'^stage/(?P<object_id>\d+)/edit/$', edit_stage),
    url(r'^stage/(?P<pk>\d+)/delete/$', DeleteStageView.as_view(),
        name='stage_delete'),

    url(r'^api/1.0/get_key/$', get_api_key),
    url(r'^api/1.0/deployment/(?P<deployment_id>\d+)/push/$', api_push),
    url(r'^api/1.0/push/(?P<push_id>\d+)/stage/(?P<stage_id>\d+)/$',
        api_run_stage),

    url(r'^accounts/', include('djangowind.urls')),
    url(r'^logout/$', django.contrib.auth.views.logout, {'next_page': '/'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^stats/$', TemplateView.as_view(template_name="stats.html")),
    url(r'smoketest/', include('smoketest.urls')),
    url(r'^uploads/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT}),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
