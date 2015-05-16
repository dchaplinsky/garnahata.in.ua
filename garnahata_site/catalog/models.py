from django.db import models
from djgeojson.fields import PointField


class Ownership(models.Model):
    owner = models.TextField("Власник")
    registered = models.DateTimeField("Реєстрація", blank=True, null=True)
    asset = models.TextField("Власність")
    comment = models.TextField("Коментар", blank=True)
    mortgage = models.TextField("Іпотека", blank=True)
    address = models.ForeignKey("Address", verbose_name="Адреса")


class Address(models.Model):
    address = models.TextField("Адреса")
    city = models.CharField("Місто", max_length=50)
    commercial_name = models.CharField(
        "Назва комплексу або району", max_length=150, blank=True)
    link = models.URLField("Посилання на сайт забудовника")
    coords = PointField("Позиція на мапі", blank=True)
