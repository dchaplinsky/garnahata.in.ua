from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from cms_pages.models import NewsPageTag
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


def address_details(request, slug):
    address = get_object_or_404(
        Address, slug=slug
    )

    # Todo: cache
    tags = {t["tag__name"].lower(): {
            "slug": t["tag__slug"],
            "name": t["tag__name"]}

            for t in NewsPageTag.objects.select_related("tag").values(
        "tag__slug", "tag__name")}

    return render(
        request,
        "address_details.jinja",
        {
            "address": address,
            "tags": tags,
            "ownerships": Ownership.objects.filter(
                prop__address=address).order_by("prop_id", "owner", "pk")
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
        # TODO: pagination
        ownerships = ElasticOwnership.search().query(
            "match", _all={"query": query, "minimum_should_match": "2"}
        )[:20].execute()
        addresses = ElasticAddress.search().query(
            "match", _all={"query": query, "minimum_should_match": "2"}
        )[:20].execute()

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
