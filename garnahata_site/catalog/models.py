from django.db import models
from djgeojson.fields import PointField
from openpyxl import load_workbook


class Ownership(models.Model):
    owner = models.TextField("Власник")
    asset = models.TextField("Властивості нерухомості")
    registered = models.DateTimeField("Дата реєстрації", blank=True, null=True)
    ownership_ground = models.TextField("Підстава власності", blank=True)
    ownership_form = models.TextField("Форма власності", blank=True)
    share = models.TextField("Частка", blank=True)
    comment = models.TextField("Коментар", blank=True)

    mortgage_registered = models.DateTimeField(
        "Дата реєстрації іпотекі", blank=True, null=True)

    mortgage_charge = models.TextField("Підстава обтяження", blank=True)
    mortgage_details = models.TextField("Деталі за іпотекой", blank=True)
    mortgage_charge_subjects = models.TextField(
        "Суб'єкти обтяження", blank=True)
    mortgage_holder = models.TextField(
        "Заявник або іпотекодержатель", blank=True)
    mortgage_mortgagor = models.TextField(
        "Власник або іпотекодавець", blank=True)
    mortgage_guarantor = models.TextField(
        "Власник або іпотекодавець", blank=True)

    prop = models.ForeignKey("Property", verbose_name="Власність")


class Property(models.Model):
    address = models.ForeignKey("Address", verbose_name="Адреса")


class Address(models.Model):
    title = models.CharField("Коротка адреса", max_length=150)
    address = models.TextField("Адреса", blank=True)
    city = models.CharField("Місто", max_length=50)
    commercial_name = models.CharField(
        "Назва комплексу або району", max_length=150, blank=True)
    link = models.URLField("Посилання на сайт забудовника", max_length=1000)
    coords = PointField("Позиція на мапі", blank=True)

    def import_owners(self, xls_file):
        print(xls_file)
        wb = load_workbook(xls_file, read_only=True)
        ws = wb.active

        self.ownership_set.all().delete()
        prev_owner = ""

        for i, r in enumerate(ws.rows):
            if i == 0:
                print(r[0].value)
                continue

            # Власник   Реєстрація  Власність   Коментар    Іпотека
            owner, registered, asset, comment, mortgage = [
                x.value for x in r[:5]]

            if not owner:
                if any([registered, asset, comment, mortgage]):
                    if not prev_owner:
                        print("oh fuck")
                        print(registered, asset, comment, mortgage)
                    owner = prev_owner
                else:
                    prev_owner = ""
                    continue

            prev_owner = owner

            # self.ownership_set.create(
            #     owner=owner, registered=registered, asset=asset,
            #     comment=comment, mortgage=mortgage
            # )
