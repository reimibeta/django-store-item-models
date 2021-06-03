from store_item_models.class_projects.stock_managements.stock_supply_condition import StockSupplyCondition
from store_item_models.store_item_stocks.models import StoreItemStock


class ItemStockSupply:
    stock_supply = None

    def __init__(self):
        self.stock_supply = StockSupplyCondition(model=StoreItemStock)

    def supply_stock(self, current_instance):
        self.stock_supply.set_current_condition(current_instance.is_transferred)
        self.stock_supply.set_current_pk(current_instance.item_stock.id)
        self.stock_supply.supply_stock(current_instance.quantity)

    def update_stock(self, current_instance, last_instance):
        self.stock_supply.set_current_condition(current_instance.is_transferred)
        self.stock_supply.set_last_condition(last_instance.is_transferred)
        self.stock_supply.set_current_pk(current_instance.item_stock.id)
        self.stock_supply.set_last_pk(last_instance.item_stock.id)
        self.stock_supply.update_stock(current_instance.quantity, last_instance.quantity)

    def return_stock(self, last_instance):
        self.stock_supply.set_last_condition(last_instance.is_transferred)
        self.stock_supply.set_last_pk(last_instance.item_stock.id)
        self.stock_supply.return_stock(last_instance.quantity)


item_stock_supply = ItemStockSupply()
