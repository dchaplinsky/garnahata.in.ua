from django.conf import settings
from django.conf.urls import url
from fs.views import index, get_xls


urlpatterns = [
    url(r'^$', index, name='home'),
    url(r'^(?P<path>.+)/$', get_xls, name='file_process'),
]
