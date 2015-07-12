from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

from catalog.models import Address, Ownership
from catalog.elastic_models import (
    Ownership as ElasticOwnership,
    Address as ElasticAddress
)

from cms_pages.models import NewsPage


def suggest(request):
    search = ElasticOwnership.search()\
        .suggest(
            'name',
            request.GET.get('q', ''),
            completion={
                'field': 'full_name_suggest',
                'size': 10,
                'fuzzy': {
                    'fuzziness': 2,
                    'unicode_aware': 1
                }
            }
    )

    res = search.execute()

    if res.success():
        return JsonResponse(
            [val['text'] for val in res.suggest['name'][0]['options']],
            safe=False
        )
    else:
        return JsonResponse([], safe=False)


def map_markers(request):
    return JsonResponse(
        [
            {
                # WTF!?
                "coords": res.coords["coordinates"][::-1],
                "title": res.title,
                "commercial_name": res.commercial_name,
                "href": res.get_absolute_url()
            }
            for res in Address.objects.all()
        ],
        safe=False
    )


def address_details(request, slug):
    address = get_object_or_404(
        Address, slug=slug
    )

    return render(
        request,
        "address_details.jinja",
        {
            "address": address,
            "ownerships": Ownership.objects.filter(prop__address=address)
        }
    )


def addresses_by_city(request):
    # TBD: pagination

    # Because cities are weirdly ordered (according to koatuu), we are
    # using this cheap hack to put Kiev on top.
    addresses = Address.objects.order_by("-city")

    return render(
        request,
        "by_city.jinja",
        {
            "addresses": addresses,
        }
    )


def latest_addresses(request):
    # TBD: pagination

    # Because cities are weirdly ordered (according to koatuu), we are
    # using this cheap hack to put Kiev on top.
    addresses = Address.objects.order_by("-date_added")

    return render(
        request,
        "by_latest.jinja",
        {
            "addresses": addresses,
        }
    )


def search(request):
    query = request.GET.get("q", "")

    news_results = None
    addresses = None
    if query:
        ownerships = ElasticOwnership.search().query(
            "match", _all=query)[:20].execute()
        addresses = ElasticAddress.search().query(
            "match", _all=query)[:20].execute()
        news_results = NewsPage.objects.search(query)
    else:
        ownerships = ElasticOwnership.search().query("match_all").execute()

    return render(
        request,
        "search.jinja",
        {
            "query": query,
            "ownerships": ownerships,
            "news_results": news_results,
            "addresses": addresses
        }
    )
