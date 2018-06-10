from django.contrib import sitemaps
from django.urls import reverse


from catalog.models import Address
from cms_pages.models import NewsPage, StaticPage, RawHTMLPage


class MainXML(sitemaps.Sitemap):
    changefreq = 'daily'

    def items(self):
        pages = [
            ('wagtail_serve', ['']),
            ('latest_addresses', ''),
            ('addresses_by_city', ''),
        ]
        return pages

    def location(self, item):
        return reverse(item[0], args=item[1])


class NewsXML(sitemaps.Sitemap):
    def items(self):
        return NewsPage.objects.live()

    def lastmod(self, obj):
        return obj.date_added

    def location(self, item):
        return item.url


class StaticXML(sitemaps.Sitemap):
    def items(self):
        return (list(StaticPage.objects.live()) +
                list(RawHTMLPage.objects.live()))

    def location(self, item):
        return item.url
