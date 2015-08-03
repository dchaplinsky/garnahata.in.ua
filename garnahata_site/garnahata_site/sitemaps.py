from django.contrib import sitemaps
from django.core.urlresolvers import reverse


from catalog.models import Address
from cms_pages.models import NewsPage, HomePage, StaticPage


class MainXML(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['/#home','/latest', '/by_city']

    def location(self, item):
        return item


class NewsXML(sitemaps.Sitemap):
    changefreq = "daily"

    def items(self):
        return NewsPage.objects.all()

    def lastmod(self, obj):
        return obj.date_added

    def location(self, item):
        return item.url


class AdressXML(sitemaps.Sitemap):
    changefreq = "daily"

    def items(self):
        return Address.objects.all()

    def lastmod(self, obj):
        return obj.date_added

    def location(self, item):
        return item.url


class StaticXML(sitemaps.Sitemap):
    changefreq = "daily"

    def items(self):
        return StaticPage.objects.all()

    def location(self, item):
        return item.url
