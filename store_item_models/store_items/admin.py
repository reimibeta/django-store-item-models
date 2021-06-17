from django.contrib import admin
from django_admin_listfilter_dropdown.filters import DropdownFilter
from django_image.renders.render_image import render_image

from store_item_models.store_items.class_models.store_item import StoreItem
from store_item_models.store_items.class_models.store_item_image import StoreItemImage


class StoreItemImageAdminInline(admin.TabularInline):
    model = StoreItemImage
    extra = 0


# store item

class StoreItemAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'item_image',
        'name',
        'is_active'
    ]
    list_display_links = ['name', 'item_image', ]
    list_per_page = 25
    search_fields = [
        'name'
    ]

    def item_image(self, obj):
        image = StoreItemImage.objects.filter(item=obj.id).first()
        return render_image.render(image.thumbnail.url) if image is not None else "Not provide"

    list_filter = (
        # for ordinary fields
        ('name', DropdownFilter),
        # ('available', DropdownFilter),
        # for choice fields
        # ('a_choicefield', ChoiceDropdownFilter),
        # for related fields
        # ('product_material__material', RelatedDropdownFilter),
    )

    inlines = [
        StoreItemImageAdminInline
    ]


admin.site.register(StoreItem, StoreItemAdmin)
