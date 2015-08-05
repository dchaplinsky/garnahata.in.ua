from django.shortcuts import render, redirect
from django.http import Http404

from cms_pages.models import NewsPage


def tag_news(request, slug):
    if slug:
        news_results = NewsPage.objects.filter(tags__slug=slug)
        if not news_results:
            raise Http404("No News posts for that tag are found.")
        else:
            if len(news_results) == 1:
                return redirect(news_results[0].url)

    return render(
        request,
        "cms_pages/news_details.jinja",
        {
            'news_results': news_results,
        }
    )
