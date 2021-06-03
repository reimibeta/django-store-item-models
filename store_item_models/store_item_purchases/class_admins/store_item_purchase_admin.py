from django.contrib import admin
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter, DropdownFilter
from html_render_utils.html_render import HtmlRender

from store_item_models.store_item_purchases.class_admins.store_item_purchase_stock_admin import StoreItemPurchaseStockAdminInline
from store_item_models.store_item_purchases.class_models.store_item_purchase import StoreItemPurchase
from store_item_models.store_item_purchases.class_models.store_item_purchase_stock import StoreItemPurchaseStock


class StoreItemPurchaseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'note',
        'items',
        # 'item_supplier',
        'request_date',
        'purchase_date',
        'received_date',
    )
    list_display_links = ['note', 'items', ]
    # list_editable = []
    list_per_page = 25

    # readonly_fields = ['staff', ]
    def items(self, obj):
        arr = []
        stocks = StoreItemPurchaseStock.objects.filter(item_purchase=obj.id).all()
        if stocks:
            i = 0
            for stock in stocks:
                i = i + 1
                transfer = "transferred" if stock.is_transferred else "not transfer"
                paid = "paid" if stock.is_paid else "not paid"
                arr.append("{}-{}({})({})({})({})".format(
                    i, stock.item_stock,
                    stock.quantity,
                    stock.item_supplier,
                    transfer,
                    paid
                ))
        return HtmlRender.p(HtmlRender.br().join(arr), '#10284e')

    list_filter = (
        # for ordinary fields
        ('request_date', DropdownFilter),
        ('purchase_date', DropdownFilter),
        ('received_date', DropdownFilter),
        # ('product_supply_stock__is_paid', DropdownFilter),
        # ('product_supply_stock__is_transferred', DropdownFilter),
        # for choice fields
        # ('product_supply_stock__stock__product__name', DropdownFilter),
        # ('a_choicefield', ChoiceDropdownFilter),
        # for related fields
        # ('item_supplier', RelatedDropdownFilter),
    )
    inlines = [
        StoreItemPurchaseStockAdminInline,
    ]
    # search_fields = [
    #     'product_supply_stock__stock__product__name'
    # ]


admin.site.register(StoreItemPurchase, StoreItemPurchaseAdmin)
