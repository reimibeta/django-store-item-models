from django.contrib import admin
from django_admin_listfilter_dropdown.filters import DropdownFilter
from django_html_render.html_render import HtmlRender

from store_item_models.store_item_suppliers.models import StoreItemSupplier


class StoreItemSupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_date', 'updated_date', 'active')
    list_display_links = ['name', ]
    list_per_page = 25
    list_filter = (
        # for ordinary fields
        ('name', DropdownFilter),
        ('is_active', DropdownFilter),
        # for choice fields
        # ('a_choicefield', ChoiceDropdownFilter),
        # for related fields
        # ('staff', RelatedDropdownFilter),
    )

    def active(self, obj):
        check = 'active' if obj.is_active else 'inactive'
        color = 'green' if obj.is_active else 'orange'
        return HtmlRender.p(text=check, color=color)


admin.site.register(StoreItemSupplier, StoreItemSupplierAdmin)
