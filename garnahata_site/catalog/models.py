import logging
from itertools import groupby
from operator import itemgetter

from django.db import models
from django.core.validators import RegexValidator
from django.db import transaction
from django.forms.models import model_to_dict
from django.utils import timezone
from django.core.urlresolvers import reverse

from tinymce import models as tinymce_models
from djgeojson.fields import PointField
from openpyxl import load_workbook
from dateutil.parser import parse
from elasticsearch.helpers import streaming_bulk
from elasticsearch_dsl import Index
from elasticsearch_dsl.connections import connections


from catalog.elastic_models import (
    Address as ElasticAddress,
    Ownership as ElasticOwnership
)


class OwnershipsQuerySet(models.QuerySet):
    def reindex(self):
        conn = connections.get_connection()
        docs_to_index = [
            ElasticOwnership(**p.to_dict(include_address=True,
                             include_name_alternatives=True))
            for p in self]

        for response in streaming_bulk(
                conn, ({'_index': getattr(d.meta, 'index', d._doc_type.index),
                        '_type': d._doc_type.name,
                        '_source': d.to_dict()} for d in docs_to_index)):
            pass


class Ownership(models.Model):
    objects = OwnershipsQuerySet.as_manager()

    owner = models.TextField("Власник")
    asset = models.TextField("Властивості нерухомості")
    registered = models.DateTimeField("Дата реєстрації", blank=True, null=True)
    ownership_ground = models.TextField("Підстава власності", blank=True)
    ownership_form = models.TextField("Форма власності", blank=True)
    share = models.TextField("Частка", blank=True)
    comment = models.TextField("Коментар", blank=True)

    mortgage_registered = models.DateTimeField(
        "Дата реєстрації іпотеки", blank=True, null=True)

    mortgage_charge = models.TextField("Підстава обтяження", blank=True)
    mortgage_details = models.TextField("Деталі за іпотекою", blank=True)
    mortgage_charge_subjects = models.TextField(
        "Суб'єкти обтяження", blank=True)
    mortgage_holder = models.TextField(
        "Заявник або іпотекодержатель", blank=True)
    mortgage_mortgagor = models.TextField(
        "Власник або іпотекодавець", blank=True)
    mortgage_guarantor = models.TextField(
        "Поручитель", blank=True)
    mortgage_other_persons = models.TextField(
        "Інші суб'єкти обтяження", blank=True)

    prop = models.ForeignKey("Property", verbose_name="Власність")

    def __unicode__(self):
        return "%s: %s" % (
            self.owner,
            self.asset)

    def __str__(self):
        return self.__unicode__()

    def to_dict(self, include_address=False, include_name_alternatives=False):
        """
        Convert Ownership model to an indexable presentation for ES.
        """
        d = model_to_dict(self, fields=[
            "id", "owner", "asset", "registered", "ownership_ground",
            "ownership_form", "share", "comment", "mortgage_registered",
            "mortgage_charge", "mortgage_details", "mortgage_charge_subjects",
            "mortgage_holder", "mortgage_mortgagor", "mortgage_guarantor",
            "mortgage_other_persons"])

        if include_address:
            addr = self.prop.address
            d["addr_title"] = addr.title
            d["addr_address"] = addr.address
            d["addr_commercial_name"] = addr.commercial_name
            d["addr_city"] = addr.get_city_display()

        if include_name_alternatives:
            last_name = ""
            first_name = ""
            patronymic = ""
            name_parts = d["owner"].split(None, 3)

            if name_parts:
                last_name = name_parts[0]

                if len(name_parts) > 1:
                    first_name = name_parts[1]

                if len(name_parts) > 2:
                    patronymic = name_parts[2]

                d["full_name_suggest"] = [
                    {
                        "input": " ".join([last_name, first_name, patronymic]),
                        "weight": 5
                    },
                    {
                        "input": " ".join([first_name, patronymic, last_name]),
                        "weight": 3
                    },
                    {
                        "input": " ".join([first_name, last_name]),
                        "weight": 3
                    }
                ]

        d["_id"] = d["id"]
        d["prop_id"] = self.prop_id
        d["url"] = self.url

        return d

    def get_absolute_url(self):
        return self.prop.address.get_absolute_url() + (
            "#ownership_%s" % self.pk)

    @property
    def url(self):
        return self.get_absolute_url()

    class Meta:
        verbose_name = u"Власник"
        verbose_name_plural = u"Власники"

        index_together = [
            ["id", "prop", "owner"],
        ]


class Property(models.Model):
    address = models.ForeignKey("Address", verbose_name="Адреса")

    def to_dict(self):
        """
        Convert Property model to an indexable presentation for ES.
        """

        owners = []
        for owner in self.ownership_set.all():
            owners.append(owner.to_dict())

        return owners

    class Meta:
        verbose_name = u"Об'єкт"
        verbose_name_plural = u"Об'єкти"


KOATUU = {
    5: "Вінниця",
    80: "м. Київ",
    1: "Сімферополь",
    7: "Луцьк",
    12: "Дніпропетровськ",
    14: "Донецьк",
    18: "Житомир",
    21: "Ужгород",
    23: "Запоріжжя",
    26: "Івано-Франківськ",
    32: "Київська область",
    35: "Кіровоград",
    44: "Луганськ",
    46: "Львів",
    48: "Миколаїв",
    51: "Одеса",
    53: "Полтава",
    56: "Рівне",
    59: "Суми",
    61: "Тернопіль",
    63: "Харків",
    65: "Херсон",
    68: "Хмельницький",
    71: "Черкаси",
    73: "Чернівці",
    74: "Чернігів",
    85: "Севастополь"
}


class AddressesQuerySet(models.QuerySet):
    def map_markers(self):
        return [res.map_marker() for res in self if res.coords]

    def reindex(self):
        conn = connections.get_connection()
        docs_to_index = [
            ElasticAddress(**p.to_dict())
            for p in self]

        for response in streaming_bulk(
                conn, ({'_index': getattr(d.meta, 'index', d._doc_type.index),
                        '_type': d._doc_type.name,
                        '_source': d.to_dict()} for d in docs_to_index)):
            pass


class Address(models.Model):
    objects = AddressesQuerySet.as_manager()

    title = models.CharField(
        "Коротка адреса", max_length=150)

    description = tinymce_models.HTMLField(
        "Опис об'єкта", default="", blank=True)

    meta_title = models.CharField(
        "title сторінки", max_length=150, blank=True, default="")

    meta_description = models.TextField(
        "meta description сторінки", default="", blank=True)

    slug = models.SlugField("slug", max_length=200)

    address = models.TextField(
        "Адреса", blank=True)

    cadastral_number = models.CharField(
        "Кадастровий номер", blank=True, validators=[
            RegexValidator(
                regex="^\d{10}:\d{2}:\d{3}:0000$",
                message="Кадастровий код не задовільняє формату")],
        max_length=25)

    city = models.IntegerField(
        "Місто", default=80,
        choices=sorted(KOATUU.items(), key=lambda x: x[1]))

    commercial_name = models.CharField(
        "Назва комплексу або району", max_length=150, blank=True)

    link = models.URLField(
        "Посилання на сайт забудовника", max_length=1000, blank=True,
        db_index=True)

    coords = PointField(
        "Позиція на мапі", blank=True)

    date_added = models.DateTimeField(
        "Дата додання на сайт",
        default=timezone.now)

    photo = models.ImageField(u"Фото об'єкта", blank=True, upload_to="images")

    def __unicode__(self):
        return u"%s %s" % (
            self.get_city_display(),
            self.title)

    def __str__(self):
        return self.__unicode__()

    def get_absolute_url(self):
        return reverse('address_details', args=[self.slug])

    @property
    def url(self):
        return self.get_absolute_url()

    class Meta:
        verbose_name = u"Адреса"
        verbose_name_plural = u"Адреси"

        index_together = [
            ["id", "city", "title"],
        ]

    def to_dict(self):
        """
        Convert Address model to an indexable presentation for ES.
        """
        d = model_to_dict(self, fields=[
            "id", "title", "description", "address", "cadastral_number",
            "commercial_name", "link", "coords", "date_added"])

        raw_props = [
            o.to_dict()
            for o in Ownership.objects.select_related("prop__address").filter(
                prop__address_id=self.pk).order_by("prop_id")]

        properties = [
            list(owns)
            for x, owns in groupby(raw_props, itemgetter("prop_id"))]

        d["_id"] = d["id"]
        d["city"] = self.get_city_display()
        d["properties"] = properties
        d["url"] = self.url
        d["map_marker"] = self.map_marker() or {}

        return d

    @transaction.atomic
    def import_owners(self, xls_file):
        wb = load_workbook(xls_file, read_only=True)
        ws = wb.active

        self.save()
        self.property_set.all().delete()

        prev_is_blank = True
        prev_owner = ""
        total_imported = 0

        for i, r in enumerate(ws.rows):
            if i == 0:
                continue

            # Файл, Адрес/Номер, Дата, Власник, Нерухомість, Підстава, Форма,
            # Частка, Дата Обт, Причина Обт, Деталі Обт,
            # Заявник або Іпотекодержатель, Власник або Іпотекодавець,
            # Поручитель, Інші суб"єкти ОБТ

            row = [x.value.strip() if isinstance(x.value, str) else x.value
                   for x in r[:15]]

            row = [x if x is not None else "" for x in row]

            if len(row) == 14:
                (_, registered, owner, asset, ownership_ground, ownership_form,
                 share, mortgage_registered, mortgage_charge, mortgage_details,
                 mortgage_holder, mortgage_mortgagor, mortgage_charge_subjects,
                 mortgage_other_persons) = row
            else:
                (_, _, registered, owner, asset, ownership_ground, ownership_form,
                 share, mortgage_registered, mortgage_charge, mortgage_details,
                 mortgage_holder, mortgage_mortgagor, mortgage_charge_subjects,
                 mortgage_other_persons) = row

            if not any(row):
                prev_is_blank = True
                prev_owner = ""
                continue

            if prev_is_blank:
                curr_property = Property(address=self)
                curr_property.save()
                prev_is_blank = False

            if not owner:
                owner = prev_owner

            if isinstance(registered, str) and registered:
                registered = parse(registered, dayfirst=True)

            if isinstance(mortgage_registered, str) and mortgage_registered:
                mortgage_registered = parse(mortgage_registered, dayfirst=True)

            Ownership(
                prop=curr_property,
                registered=registered or None,
                owner=owner,
                asset=asset,
                ownership_ground=ownership_ground,
                ownership_form=ownership_form,
                share=share,
                mortgage_registered=mortgage_registered or None,
                mortgage_charge=mortgage_charge,
                mortgage_details=mortgage_details,
                mortgage_holder=mortgage_holder,
                mortgage_mortgagor=mortgage_mortgagor,
                mortgage_charge_subjects=mortgage_charge_subjects,
                mortgage_other_persons=mortgage_other_persons
            ).save()
            total_imported += 1

            prev_owner = owner

        logging.debug("Imported in total: %s" % total_imported)
        self.date_added = timezone.now()
        self.save()
        return total_imported

    def map_marker(self):
        if self.coords:
            return {
                # WTF!?
                "coords": self.coords["coordinates"][::-1],
                "title": self.title,
                "commercial_name": self.commercial_name,
                "href": self.get_absolute_url()
            }
        else:
            return ""


# @receiver(post_save, sender=Address)
def reindex_addresses(sender, **kwargs):
    Index(ElasticAddress.META.index).delete(ignore=404)

    Address.objects.all().reindex()
    Ownership.objects.select_related("prop__address").reindex()
