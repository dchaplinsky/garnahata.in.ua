from django.conf import settings
from django.conf.urls import url
from cms_pages.views import tag_news


urlpatterns = [
    url(r'^(?P<slug>.+)$', tag_news, name='tag_news'),
]