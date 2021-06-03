from store_item_models.class_projects.stock_managements.stock_outlet_condition import StockOutletCondition
from store_item_models.store_item_stocks.models import StoreItemStock


class ItemStockOutlet:
    stock_outlet = None

    def __init__(self):
        self.stock_outlet = StockOutletCondition(model=StoreItemStock)

    def outlet_stock(self, current_instance):
        self.stock_outlet.set_current_condition(current_instance.is_move_from_stock)
        self.stock_outlet.set_current_pk(current_instance.item_stock.id)
        self.stock_outlet.outlet_stock(current_instance.quantity)

    def update_stock(self, current_instance, last_instance):
        self.stock_outlet.set_current_condition(current_instance.is_move_from_stock)
        self.stock_outlet.set_last_condition(last_instance.is_move_from_stock)
        self.stock_outlet.set_current_pk(current_instance.item_stock.id)
        self.stock_outlet.set_last_pk(last_instance.item_stock.id)
        self.stock_outlet.update_stock(current_instance.quantity, last_instance.quantity)

    def refund_stock(self, last_instance):
        self.stock_outlet.set_last_condition(last_instance.is_move_from_stock)
        self.stock_outlet.set_last_pk(last_instance.item_stock.id)
        self.stock_outlet.refund_stock(last_instance.quantity)


item_stock_outlet = ItemStockOutlet()
