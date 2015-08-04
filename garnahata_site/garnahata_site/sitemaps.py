from django.contrib import sitemaps
from django.core.urlresolvers import reverse


from catalog.models import Address
from cms_pages.models import NewsPage, HomePage, StaticPage


class MainXML(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        pages = (
            ('wagtail_serve', ['']),
            ('latest_addresses', ''),
            ('addresses_by_city', ''),
        )
        return [pages[0],pages[1],pages[2]]

    def location(self, item):
        return reverse(item[0], args=item[1])


class NewsXML(sitemaps.Sitemap):
    changefreq = "daily"

    def items(self):
        return NewsPage.objects.live()

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
        return StaticPage.objects.live()

    def location(self, item):
        return item.url
