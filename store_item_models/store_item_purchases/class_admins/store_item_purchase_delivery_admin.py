from django.contrib import admin
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter

from store_item_models.store_item_purchases.class_models.store_item_purchase_delivery import StoreItemPurchaseDelivery


class StoreItemPurchaseDeliveryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'account',
        'item_purchase',
        'deliver',
        'quantity',
        'delivery_price',
        'delivery_date',
        'arrived_date',
    )
    ist_display_links = ['deliver', ]
    list_per_page = 25
    list_filter = (
        # for ordinary fields
        ('delivery_date', DropdownFilter),
        ('arrived_date', DropdownFilter),
        ('quantity', DropdownFilter),
        # for choice fields
        # ('delivery_status', ChoiceDropdownFilter),
        # for related fields
        ('item_purchase', RelatedDropdownFilter),
        ('deliver', RelatedDropdownFilter),
    )

    def delivery_price(self, obj):
        if obj.account.currency is not None:
            return "{} {}".format(obj.cost_delivery, obj.account.currency.currency)
        else:
            return "not provided"

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "deliver":
    #         # db_field['customer']
    #         kwargs["queryset"] = StaffDeliver.objects.filter(is_active=True).all()
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(StoreItemPurchaseDelivery, StoreItemPurchaseDeliveryAdmin)


class StoreItemPurchaseDeliveryAdminInline(admin.StackedInline):
    model = StoreItemPurchaseDelivery
    extra = 0
