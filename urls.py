from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
import os.path
admin.autodiscover()
import staticmedia

site_media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
                       # Example:
                       # (r'^rolf/', include('rolf.foo.urls')),
                       ('^accounts/',include('djangowind.urls')),
                       (r'^admin/(.*)', admin.site.root),
		       (r'^survey/',include('survey.urls')),
                       (r'^tinymce/', include('tinymce.urls')),
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media_root}),
                       (r'^uploads/(?P<path>.*)$','django.views.static.serve',{'document_root' : settings.MEDIA_ROOT}),
) + staticmedia.serve()

