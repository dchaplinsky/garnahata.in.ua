# coding: utf-8
from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailsearch import index
from wagtail.wagtailadmin.edit_handlers import (
    InlinePanel, FieldPanel, PageChooserPanel)

from catalog.models import Address


class AbstractJinjaPage(object):
    def get_context(self, request, *args, **kwargs):
        return {
            'page': self,
            'request': request,
        }


class StaticPage(AbstractJinjaPage, Page):
    body = RichTextField(verbose_name="Текст сторінки")
    template = "cms_pages/static_page.jinja"

    class Meta:
        verbose_name = "Статична сторінка"

StaticPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('body', classname="full"),
]


class RawHTMLPage(AbstractJinjaPage, Page):
    body = models.TextField(verbose_name="Текст сторінки")
    template = "cms_pages/static_page.jinja"

    class Meta:
        verbose_name = "Raw-HTML сторінка"

RawHTMLPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('body', classname="full"),
]


class NewsPage(AbstractJinjaPage, Page):
    lead = RichTextField(verbose_name="Лід", blank=True)
    body = RichTextField(verbose_name="Текст новини")
    date_added = models.DateTimeField(verbose_name="Опубліковано")

    reprint = models.BooleanField(verbose_name="Новина не є унікальною",
                                  default=False)
    sticky = models.BooleanField(verbose_name="Закріпити новину",
                                 default=False)
    important = models.BooleanField(verbose_name="Важлива новина",
                                    default=False)

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + (
        index.SearchField('lead'),
        index.FilterField('body'),
    )

    template = "cms_pages/news_page.jinja"

    class Meta:
        verbose_name = "Новина"

NewsPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('lead', classname="full"),
    FieldPanel('body', classname="full"),
    FieldPanel('date_added', classname="full"),
    FieldPanel('sticky', classname="full"),
    FieldPanel('important', classname="full"),
    FieldPanel('reprint', classname="full"),
    ImageChooserPanel('image'),
]


class LinkFields(models.Model):
    caption = models.CharField(max_length=255, blank=True)

    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        else:
            return self.link_external

    panels = [
        FieldPanel('caption'),
        FieldPanel('link_external'),
        PageChooserPanel('link_page')
    ]

    class Meta:
        abstract = True


class HomePageTopMenuLink(Orderable, LinkFields):
    page = ParentalKey('cms_pages.HomePage', related_name='top_menu_links')


class HomePage(AbstractJinjaPage, Page):
    body = RichTextField(verbose_name="Текст сторінки")
    news_count = models.IntegerField(
        default=6,
        verbose_name="Кількість новин на сторінку")

    template = "cms_pages/home.jinja"

    def get_context(self, request, *args, **kwargs):
        ctx = super(HomePage, self).get_context(request, *args, **kwargs)

        hp_news = NewsPage.objects.live().filter(
            sticky=True).order_by("-date_added").first()

        latest_news = NewsPage.objects.live().exclude(
            pk=hp_news.pk if hp_news is not None else None).order_by(
            "-date_added")[:self.news_count]

        ctx["hp_news"] = hp_news
        ctx["latest_news"] = latest_news
        ctx["latest_addresses"] = Address.objects.order_by("-date_added")

        return ctx

    class Meta:
        verbose_name = "Головна сторінка"

HomePage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('body', classname="full"),
    InlinePanel(HomePage, 'top_menu_links', label="Меню зверху"),
]
