from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from catalog.models import Address
from cms_pages.models import NewsPage, HomePage


class LatestXML(Sitemap):
    changefreq = "daily"

    def items(self):
        return Address.objects.order_by("-date_added")

    def lastmod(self, obj):
        return obj.date_added


class СitiesXML(Sitemap):
    changefreq = "daily"

    def items(self):
        return Address.objects.order_by("-city")

    def lastmod(self, obj):
        return obj.date_added


class NewsXML(Sitemap):
    changefreq = "daily"

    def items(self):
        return NewsPage.objects.all()

    def lastmod(self, obj):
        return obj.date_added

    def location(self, item):
        return '/' + item.slug


class HomeXML(Sitemap):
    changefreq = "daily"

    def items(self):
        return HomePage.objects.all()

    def location(self, item):
        return '/'


class AdressXML(Sitemap):
    changefreq = "daily"

    def items(self):
        return Address.objects.all()

    def lastmod(self, obj):
        return obj.date_added


