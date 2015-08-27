from django.contrib.syndication.views import Feed


from cms_pages.models import NewsPage


class LatestNewsFeed(Feed):
    title = "Garnahata.in.ua site news"
    link = "/feeds/news/"
    description = "Latest news"

    def items(self):
        return NewsPage.objects.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_link(self, item):
        return item.url