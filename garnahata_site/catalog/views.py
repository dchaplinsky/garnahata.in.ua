from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from catalog.models import Address, Ownership
from catalog.elastic_models import Ownership as ElasticOwnership


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
