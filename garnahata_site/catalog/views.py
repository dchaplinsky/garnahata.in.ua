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
    def assume(q, fuzziness):
        search = ElasticOwnership.search()\
            .suggest(
                'name',
                q,
                completion={
                    'field': 'full_name_suggest',
                    'size': 10,
                    'fuzzy': {
                        'fuzziness': fuzziness,
                        'unicode_aware': 1
                    }
                }
        )

        res = search.execute()

        if res.success():
            return [val['text'] for val in res.suggest['name'][0]['options']]
        else:
            []

    q = request.GET.get('q', '').strip()

    # It seems, that for some reason 'AUTO' setting doesn't work properly
    # for unicode strings
    fuzziness = 0

    if len(q) > 2:
        fuzziness = 1

    suggestions = assume(q, fuzziness)

    if not suggestions:
        suggestions = assume(q, fuzziness + 1)

    return JsonResponse(suggestions, safe=False)


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
    addresses = Address.objects.order_by("city", "title")

    return render(
        request,
        "by_city.jinja",
        {
            "addresses": addresses,
        }
    )


def latest_addresses(request):
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

    fields_to_search = [
        "owner", "asset", "ownership_ground", "ownership_form", "share",
        "comment", "mortgage_charge", "mortgage_details",
        "mortgage_charge_subjects", "mortgage_holder", "mortgage_mortgagor",
        "mortgage_guarantor", "mortgage_other_persons"]

    if query:
        ownerships = ElasticOwnership.search().query(
            "multi_match", query=query, operator="and",
            fields=fields_to_search
        )

        if ownerships.count() == 0:
            # PLAN B, PLAN B
            ownerships = ElasticOwnership.search().query(
                "multi_match", query=query,
                operator="or",
                minimum_should_match="2",
                fields=fields_to_search
            )
    else:
        ownerships = ElasticOwnership.search().query("match_all")

    return paginated_search(request, ownerships)


def _addresses_search(request):
    query = request.GET.get("q", "")

    if query:
        addresses = ElasticAddress.search().query(
            "match", _all={"query": query, "operator": "and"}
        )

        if addresses.count() == 0:
            # PLAN B, PLAN B
            addresses = ElasticAddress.search().query(
                "match", _all={
                    "query": query,
                    "operator": "or",
                    "minimum_should_match": "2"
                },
            )
    else:
        addresses = ElasticAddress.search().query("match_all")

    return paginated_search(request, addresses)


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
