from django.conf import settings
from django.conf.urls import patterns, url


urlpatterns = patterns(
	'cms_pages.views',
    url(r'^(?P<slug>.+)$', 'tag_news',
        name='tag_news'),
)