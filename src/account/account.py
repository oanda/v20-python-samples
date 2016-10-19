import common.view
import trade.view
import position.view
import order.view

class Account(object):
    """
    An Account object wraps the Account entites fetched from the v20 REST API
    for the purpose of storing and updating Account state.
    """
    def __init__(self, account):
        """
        Create a new Account wrapper

        Args:
            account: a v20.account.Account fetched from the server
        """

        self.trades = getattr(account, "trades", None)
        setattr(account, "trades", None)

        self.orders = getattr(account, "orders", None)
        setattr(account, "orders", None)

        self.positions = getattr(account, "positions", None)
        setattr(account, "positions", None)

        self.details = account


    def dump(self):
        common.view.print_entity(
            self.details.title(),
            self.details
        )

        print

        if self.positions is not None:
            position.view.print_positions(self.positions)
            print

        if self.trades is not None:
            trade.view.print_trade_summaries(self.trades)
            print

        if self.orders is not None:
            order.view.print_order_summaries(self.orders)
            print

