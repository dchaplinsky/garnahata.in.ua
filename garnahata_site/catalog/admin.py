from django import forms
from django.contrib import admin

from catalog.models import Address, Ownership
from tinymce.widgets import TinyMCE
from leaflet.admin import LeafletGeoAdmin


class AddressAdminForm(forms.ModelForm):
    xls_file = forms.FileField(
        label="Завантажити підготовлений xls(x)-файл з власниками",
        required=False,
        help_text="Увага! Файл має бути у спеціальному форматі. "
                  "Усі записи для цієї адреси буде стерто!")

    # description = forms.TextField(
    #     widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    def save(self, force_insert=False, force_update=False, commit=True):
        m = super(AddressAdminForm, self).save(commit=False)

        if self.cleaned_data["xls_file"]:
            m.import_owners(self.cleaned_data["xls_file"].file)

        if commit:
            m.save()

        return m

    class Media:
        css = {
            'all': ('css/Control.Geocoder.css', 'css/admin.map.css')
        }
        js = ('https://api-maps.yandex.ru/2.0/?load=package.map&lang=ru-RU',
              'js/Control.Geocoder.js', 'js/Yandex.js',
              'js/geocoder.init.js')

    class Meta:
        model = Address
        fields = '__all__'


class AddressAdmin(LeafletGeoAdmin):
    form = AddressAdminForm

    prepopulated_fields = {"slug": ("title",)}

    def address_or_cadastral(self, obj):
        return " ".join([obj.address, obj.cadastral_number]).strip()

    address_or_cadastral.short_description = 'Адреса або кадастровий номер'

    def records(self, obj):
        return Ownership.objects.filter(prop__address=obj).count()
    records.short_description = 'Кількість прав власності'

    list_display = (
        "title", "city", "address_or_cadastral", "date_added", "records")


class OwnershipAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "asset",
        "get_address",
        "registered",
        "ownership_ground",
        "ownership_form",
        "share",
        "mortgage_registered",
        "mortgage_charge",
        "mortgage_details",
        "mortgage_charge_subjects",
        "mortgage_holder",
        "mortgage_mortgagor",
        "mortgage_guarantor",
        "mortgage_other_persons"
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_address(self, obj):
        return obj.prop.address

    get_address.short_description = "Адреса"

    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
            [field.name for field in obj._meta.fields]


admin.site.register(Address, AddressAdmin)
admin.site.register(Ownership, OwnershipAdmin)
