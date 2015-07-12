# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from catalog.models import Address, Ownership
from catalog.elastic_models import (
    Address as ElasticAddress,
    Ownership as ElasticOwnership
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        ElasticAddress.init()
        counter = 0
        for p in Address.objects.all():
            item = ElasticAddress(**p.to_dict())
            item.save()
            counter += 1

        self.stdout.write(
            'Loaded {} addresses to persistence storage'.format(counter))

        ElasticOwnership.init()
        counter = 0
        for p in Ownership.objects.all():
            item = ElasticOwnership(**p.to_dict(
                include_address=True, include_name_alternatives=True
            ))
            item.save()
            counter += 1

        self.stdout.write(
            'Loaded {} ownerships to persistence storage'.format(counter))
