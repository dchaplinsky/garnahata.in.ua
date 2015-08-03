from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from cms_pages.models import NewsPageTag
from catalog.models import Address, Ownership
from catalog.api import hybrid_response
from catalog.paginator import paginated_search

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
    addresses = Address.objects.order_by("-city", "title")

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


def _ownership_search(request):
    query = request.GET.get("q", "")

    if query:
        return paginated_search(request, ElasticOwnership.search().query(
            "match", _all={"query": query, "minimum_should_match": "2"}
        ))

    return paginated_search(
        request, ElasticOwnership.search().query("match_all"))


def _addresses_search(request):
    query = request.GET.get("q", "")

    if query:
        return paginated_search(request, ElasticAddress.search().query(
            "match", _all={"query": query, "minimum_should_match": "2"}
        ))

    return paginated_search(
        request, ElasticAddress.search().query("match_all"))


def _news_search(request):
    query = request.GET.get("q", "")

    if query:
        return NewsPage.objects.search(query)
    else:
        return None


@hybrid_response("search.jinja")
def search(request, sources=["ownerships", "addresses", "news"]):
    query = request.GET.get("q", "")

    res = {
        "query": query,
    }

    if "ownerships" in sources:
        res["ownerships"] = _ownership_search(request)

    if "addresses" in sources:
        res["addresses"] = _addresses_search(request)

    if "news" in sources:
        res["news_results"] = _news_search(request)

    return res
