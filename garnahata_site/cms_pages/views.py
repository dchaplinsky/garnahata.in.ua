from django.shortcuts import render, redirect
from django.http import Http404
from django.core.paginator import EmptyPage, PageNotAnInteger
from catalog.paginator import BetterPaginator

from cms_pages.models import NewsPage


def tag_news(request, slug):
    if slug:
        news_results = NewsPage.objects.filter(tags__slug=slug)
        if not news_results:
            raise Http404("Нажаль, за цим тегом нічого не знайдено.")
        else:
            if len(news_results) == 1:
                return redirect(news_results[0].url)

    return render(
        request,
        "news_by_tag.jinja",
        {
            'news_results': news_results,
        }
    )


def news(request):
    news = BetterPaginator(
        NewsPage.objects.live().order_by("-first_published_at"), 1)

    page = request.GET.get('page')
    try:
        news = news.page(page)
    except PageNotAnInteger:
        news = news.page(1)
    except EmptyPage:
        news = news.page(news.num_pages)

    return render(
        request,
        "news.jinja",
        {
            "news": news,
        }
    )
