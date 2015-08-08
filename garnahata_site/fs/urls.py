from django.conf import settings
from django.conf.urls import patterns, url


urlpatterns = patterns(
	'fs.views',
    url(r'^$', 'index',
        name='home'),
    url(r'^(?P<path>.+)/$', 'get_xls',
        name='file_process'),
)
