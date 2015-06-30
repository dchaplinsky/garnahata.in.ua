from django.db import models
from djgeojson.fields import PointField
from openpyxl import load_workbook


class Ownership(models.Model):
    owner = models.TextField("Власник")
    registered = models.DateTimeField("Реєстрація", blank=True, null=True)
    asset = models.TextField("Власність")
    comment = models.TextField("Коментар", blank=True)
    mortgage = models.TextField("Іпотека", blank=True)
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
