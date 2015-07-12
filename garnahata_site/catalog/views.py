from django.shortcuts import render
from django.http import JsonResponse
from catalog.models import Address
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
            }
            for res in Address.objects.all()
        ],
        safe=False
    )
