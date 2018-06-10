# coding: utf-8
import json

from django.db import models
from django.urls import reverse
from django.utils.html import mark_safe

from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.models import Page, Orderable
from wagtail.search import index
from wagtail.admin import widgets
from wagtail.core import hooks
from wagtail.admin.edit_handlers import (
    InlinePanel, FieldPanel, PageChooserPanel)

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase

from catalog.models import Address


class AdminMultiTagWidget(widgets.AdminTagWidget):
    def render_js_init(self, id_, name, value):
        return (
            "$.ui.keyCode.COMMA=$.ui.keyCode.ENTER;" +
            "$('#' + {0}).tagit({{autocomplete: {{source: {1}}}, allowSpaces: true}});".format(
                json.dumps(id_),
                json.dumps(reverse('wagtailadmin_tag_autocomplete'))))


class AbstractJinjaPage(object):
    @hooks.register('insert_editor_js')
    def editor_js():
        return mark_safe(
            """
            <script>
                $(function() {
                    $(".richtext").each(function() {
                        var widget = $(this).data("IKSHallo");
                        widget.keepActivated(true);
                        widget.activate();
                    });
                });
            </script>
            """
        )

    def get_context(self, request, *args, **kwargs):
        return {
            'page': self,
            'request': request,
        }


class StaticPage(Page, AbstractJinjaPage):
    body = RichTextField(verbose_name="Текст сторінки")
    template = "cms_pages/static_page.jinja"

    class Meta:
        verbose_name = "Статична сторінка"

StaticPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('body', classname="full"),
]


class RawHTMLPage(Page, AbstractJinjaPage):
    body = models.TextField(verbose_name="Текст сторінки")
    template = "cms_pages/static_page.jinja"

    class Meta:
        verbose_name = "Raw-HTML сторінка"

RawHTMLPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('body', classname="full"),
]


class NewsPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'cms_pages.NewsPage', related_name='tagged_items')


class NewsPage(Page, AbstractJinjaPage):
    lead = RichTextField(verbose_name="Лід", blank=True)
    body = RichTextField(verbose_name="Текст новини")
    date_added = models.DateTimeField(verbose_name="Опубліковано")

    reprint = models.BooleanField(verbose_name="Новина не є унікальною",
                                  default=False)
    sticky = models.BooleanField(verbose_name="Закріпити новину",
                                 default=False)
    important = models.BooleanField(verbose_name="Важлива новина",
                                    default=False)
    special_case = models.BooleanField(verbose_name="Особливий випадок", 
                                        default=False, db_index=True)

    tags = ClusterTaggableManager(through=NewsPageTag, blank=True)

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def get_tags(self):
        return '\n'.join(self.tags.all().values_list('name', flat=True))

    search_fields = Page.search_fields + [
        index.SearchField('lead'),
        index.SearchField('body'),
        index.SearchField('get_tags'),
    ]

    template = "cms_pages/news_page.jinja"

    class Meta:
        verbose_name = "Новина"

NewsPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('lead', classname="full"),
    FieldPanel('body', classname="full"),
    FieldPanel('date_added', classname="full"),
    FieldPanel('sticky', classname="full"),
    FieldPanel('special_case', classname="full"),
    FieldPanel('important', classname="full"),
    FieldPanel('reprint', classname="full"),
    ImageChooserPanel('image'),
    FieldPanel('tags', widget=AdminMultiTagWidget),
]


class LinkFields(models.Model):
    caption = models.CharField(max_length=255, blank=True)

    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
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


class HomePage(Page, AbstractJinjaPage):
    body = RichTextField(verbose_name="Текст сторінки")
    news_count = models.IntegerField(
        default=6,
        verbose_name="Кількість новин на сторінку")

    template = "cms_pages/home.jinja"

    def get_context(self, request, *args, **kwargs):
        ctx = super(HomePage, self).get_context(request, *args, **kwargs)

        hp_news = NewsPage.objects.live().filter(
            sticky=True).order_by("-date_added").first()

        latest_news = NewsPage.objects.live().filter(
            special_case=False).exclude(
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
    InlinePanel('top_menu_links', label="Меню зверху"),
]
