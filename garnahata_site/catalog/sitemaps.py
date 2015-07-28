from django.contrib.sitemaps import Sitemap

from catalog.models import Address


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
