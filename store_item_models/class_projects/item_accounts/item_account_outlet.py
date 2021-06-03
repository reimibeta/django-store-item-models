from wallet_models.class_projects.balances.outlets.balance_outlet_condition import balance_outlet_condition


class ItemAccountOutlet:
    """ need is_paid to confirm """

    def outlet_account(self, current_instance, current_amount):
        balance_outlet_condition.set_current_pk(current_instance.account.id)
        balance_outlet_condition.set_current_condition(current_instance.is_paid)
        balance_outlet_condition.outlet_account(current_amount)

    def update_outlet_account(self, current_instance, last_instance, current_amount, last_amount):
        balance_outlet_condition.set_current_pk(current_instance.account.id)
        balance_outlet_condition.set_current_condition(current_instance.is_paid)
        balance_outlet_condition.set_last_pk(last_instance.account.id)
        balance_outlet_condition.set_last_condition(last_instance.is_paid)
        balance_outlet_condition.update_outlet_account(
            current_amount=current_amount,
            last_amount=last_amount
        )

    def refund_outlet_account(self, last_instance, last_amount):
        balance_outlet_condition.set_last_condition(last_instance.is_paid)
        balance_outlet_condition.set_last_pk(last_instance.account.id)
        balance_outlet_condition.refund_outlet_account(last_amount=last_amount)


item_account_outlet = ItemAccountOutlet()
