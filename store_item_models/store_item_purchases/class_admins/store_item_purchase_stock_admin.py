from django.contrib import admin
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter

from store_item_models.store_item_purchases.class_models.store_item_purchase_stock import StoreItemPurchaseStock
from store_item_models.store_item_stocks.models import StoreItemStock


class StoreItemPurchaseStockAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'item_purchase',
        'item_stock',
        'quantity',
        'item_supplier',
        'purchase_price_per_unit',
        'purchase_price_total',
        'is_transferred'
    )
    list_display_links = ['item_purchase', 'item_stock', 'item_supplier']
    list_editable = [
        # 'quantity',
        'is_transferred',
    ]
    list_per_page = 25

    # readonly_fields = ['staff', ]
    # exclude = ['build', ]

    list_filter = (
        # for ordinary fields
        ('quantity', DropdownFilter),
        ('price_per_unit', DropdownFilter),
        ('is_transferred', DropdownFilter),
        # for choice fields
        # ('a_choicefield', ChoiceDropdownFilter),
        # for related fields
        ('item_purchase', RelatedDropdownFilter),
        ('item_stock', RelatedDropdownFilter),
        ('item_supplier', RelatedDropdownFilter),
    )
    inlines = []

    search_fields = [
        'item_stock__item__name'
    ]

    # disable actions
    def has_add_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def purchase_price_per_unit(self, obj):
        return "{} {}".format(obj.price_per_unit, obj.account.currency.currency)

    def purchase_price_total(self, obj):
        return "{} {}".format(
            obj.price_per_unit * obj.quantity, obj.account.currency.currency
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # stock
        if db_field.name == "item_stock":
            try:
                # parent_id = request.resolver_match.args[0]
                kwargs["queryset"] = StoreItemStock.objects.filter(
                    is_available=True
                ).order_by('item__name')
            except IndexError:
                pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(StoreItemPurchaseStock, StoreItemPurchaseStockAdmin)


class StoreItemPurchaseStockAdminInline(admin.TabularInline):
    model = StoreItemPurchaseStock
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # stock
        if db_field.name == "item_stock":
            try:
                # parent_id = request.resolver_match.args[0]
                kwargs["queryset"] = StoreItemStock.objects.filter(
                    is_available=True
                ).order_by('item__name')
            except IndexError:
                pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
