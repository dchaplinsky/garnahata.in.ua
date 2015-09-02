from django.contrib.syndication.views import Feed


from cms_pages.models import NewsPage


class LatestNewsFeed(Feed):
    title = "Новини та розслідування Garnahata.in.ua"
    link = "/feeds/news/"
    description = "Останні новини"

    def items(self):
        return NewsPage.objects.live().order_by("-date_added")

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_link(self, item):
        return item.url

    def item_pubdate(self, item):
        return item.date_added
