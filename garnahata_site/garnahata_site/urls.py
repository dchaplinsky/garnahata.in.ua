from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls import patterns, include, url

from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtailadmin import urls as wagtailadmin_urls


urlpatterns = patterns(
    '',
    url(r'^ajax/suggest$', 'catalog.views.suggest', name='suggest'),
    url(r'^map_markers$', 'catalog.views.map_markers', name='map_markers'),
    (r'^base$', TemplateView.as_view(template_name='base.jinja')),

    url(r'^a/(?P<slug>.+)$', 'catalog.views.address_details',
        name='address_details'),

    # url(r'^office/(?P<office_name>.+)$', 'catalog.views.office',
    #     name='office'),

    # url(r'^sitemap.xml$', 'catalog.views.sitemap',
    #     name='sitemap'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'', include(wagtail_urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
