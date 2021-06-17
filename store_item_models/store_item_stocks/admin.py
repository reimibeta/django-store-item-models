from django.contrib import admin
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter
from django_image.renders.render_image import render_image

from store_item_models.store_item_stocks.models import StoreItemStock
from store_item_models.store_items.class_models.store_item import StoreItem
from store_item_models.store_items.class_models.store_item_image import StoreItemImage


class StoreItemStockAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_image', 'item', 'quantity', 'is_available')
    list_display_links = ['item', 'item_image', ]
    list_per_page = 25

    list_filter = (
        # for ordinary fields
        ('quantity', DropdownFilter),
        ('is_available', DropdownFilter),
        # for choice fields
        # ('a_choicefield', ChoiceDropdownFilter),
        # for related fields
        ('item', RelatedDropdownFilter),
    )
    search_fields = [
        'item__name'
    ]

    def item_image(self, obj):
        image = StoreItemImage.objects.filter(item=obj.item.id).first()
        if image:
            return render_image.render(image.thumbnail.url)
        else:
            return "Not provide"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # stock
        if db_field.name == "item":
            try:
                # parent_id = request.resolver_match.args[0]
                kwargs["queryset"] = StoreItem.objects.filter(
                    is_active=True
                ).order_by('name')
            except IndexError:
                pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(StoreItemStock, StoreItemStockAdmin)
