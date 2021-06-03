from django.contrib import admin
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter, DropdownFilter
from html_render_utils.html_render import HtmlRender

from store_item_models.store_item_uses.class_models.store_item_use import StoreItemUse
from store_item_models.store_item_uses.class_models.store_item_use_stock import StoreItemUseStock


class StoreItemUseStockAdminInline(admin.TabularInline):
    model = StoreItemUseStock
    extra = 0


class StoreItemUseAdmin(admin.ModelAdmin):
    list_display = [
        'note',
        'items',
        'request_date',
        'take_out_date',
    ]

    search_fields = [
        'item_use_stock__item__name'
    ]

    def items(self, obj):
        arr = []
        items = StoreItemUseStock.objects.filter(item_use=obj.id).all()
        if items:
            i = 0
            for item in items:
                i = i + 1
                transfer = "transferred" if item.is_move_from_stock else "not transfer"
                arr.append("{}-{}({})({})".format(
                    i, item.item_stock,
                    item.quantity,
                    transfer
                ))
        return HtmlRender.p(HtmlRender.br().join(arr), '#10284e')

    list_display_links = [
        'items',
    ]

    list_per_page = 25
    list_filter = (
        # for ordinary fields
        ('request_date', DropdownFilter),
        ('take_out_date', DropdownFilter),
        # for choice fields
        # ('order_status', ChoiceDropdownFilter),
        # for related fields
        # ('item_stock', RelatedDropdownFilter),
    )

    # list_editable = ['is_move_from_stock']

    inlines = [
        StoreItemUseStockAdminInline
    ]


admin.site.register(StoreItemUse, StoreItemUseAdmin)
