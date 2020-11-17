import common.view
from position.view import print_positions_map
from order.view import print_orders_map
from trade.view import print_trades_map


def update_attribute(dest, name, value):
    """
    Set dest[name] to value if it exists and is not None
    """

    if hasattr(dest, name) and \
       getattr(dest, name) is not None:
        setattr(dest, name, value)


class Account(object):
    """
    An Account object is a wrapper for the Account entities fetched from the
    v20 REST API. It is used for caching and updating Account state.
    """
    def __init__(self, account, transaction_cache_depth=100):
        """
        Create a new Account wrapper

        Args:
            account: a v20.account.Account fetched from the server
        """

        #
        # The collection of Trades open in the Account
        #
        self.trades = {}

        for trade in getattr(account, "trades", []):
            self.trades[trade.id] = trade

        setattr(account, "trades", None)

        #
        # The collection of Orders pending in the Account
        #
        self.orders = {}

        for order in getattr(account, "orders", []):
            self.orders[order.id] = order

        setattr(account, "orders", None)

        #
        # Map from OrderID -> OrderState. Order State is tracked for
        # TrailingStopLoss orders, and includes the trailingStopValue
        # and triggerDistance
        #
        self.order_states = {}

        #
        # Teh collection of Positions open in the Account
        #
        self.positions = {}

        for position in getattr(account, "positions", []):
            self.positions[position.instrument] = position

        setattr(account, "positions", None)

        #
        # Keep a cache of the last self.transaction_cache_depth Transactions
        #
        self.transaction_cache_depth = transaction_cache_depth
        self.transactions = []

        #
        # The Account details
        #
        self.details = account

    def dump(self):
        """
        Print out the whole Account state
        """

        common.view.print_entity(
            self.details,
            title=self.details.title()
        )

        print("")

        print_positions_map(self.positions)

        print_orders_map(self.orders)

        print_trades_map(self.trades)

    def trade_get(self, id):
        """
        Fetch an open Trade

        Args:
            id: The ID of the Trade to fetch

        Returns:
            The Trade with the matching ID if it exists, None otherwise
        """

        return self.trades.get(id, None)

    def order_get(self, id):
        """
        Fetch a pending Order

        Args:
            id: The ID of the Order to fetch

        Returns:
            The Order with the matching ID if it exists, None otherwise
        """

        return self.orders.get(id, None)

    def position_get(self, instrument):
        """
        Fetch an open Position

        Args:
            instrument: The instrument of the Position to fetch

        Returns:
            The Position with the matching instrument if it exists, None
            otherwise
        """

        return self.positions.get(instrument, None)

    def apply_changes(self, changes):
        """
        Update the Account state with a set of changes provided by the server.

        Args:
            changes: a v20.account.AccountChanges object representing the
                     changes that have been made to the Account
        """

        for order in changes.ordersCreated:
            print("[Order Created] {}".format(order.title()))
            self.orders[order.id] = order

        for order in changes.ordersCancelled:
            print("[Order Cancelled] {}".format(order.title()))
            self.orders.pop(order.id, None)

        for order in changes.ordersFilled:
            print("[Order Filled] {}".format(order.title()))
            self.orders.pop(order.id, None)

        for order in changes.ordersTriggered:
            print("[Order Triggered] {}".format(order.title()))
            self.orders.pop(order.id, None)

        for trade in changes.tradesOpened:
            print("[Trade Opened] {}".format(trade.title()))
            self.trades[trade.id] = trade

        for trade in changes.tradesReduced:
            print("[Trade Reduced] {}".format(trade.title()))
            self.trades[trade.id] = trade

        for trade in changes.tradesClosed:
            print("[Trade Closed] {}".format(trade.title()))
            self.trades.pop(trade.id, None)

        for position in changes.positions:
            print("[Position Changed] {}".format(position.instrument))
            self.positions[position.instrument] = position

        for transaction in changes.transactions:
            print("[Transaction] {}".format(transaction.title()))

            self.transactions.append(transaction)

            if len(self.transactions) > self.transaction_cache_depth:
                self.transactions.pop(0)

    def apply_trade_states(self, trade_states):
        """
        Update state for open Trades

        Args:
            trade_states: A list of v20.trade.CalculatedTradeState objects
                          representing changes to the state of open Trades

        """
        for trade_state in trade_states:
            trade = self.trade_get(trade_state.id)

            if trade is None:
                continue

            for field in trade_state.fields():
                setattr(trade, field.name, field.value)

    def apply_position_states(self, position_states):
        """
        Update state for all Positions

        Args:
            position_states: A list of v20.trade.CalculatedPositionState
                             objects representing changes to the state of open
                             Position

        """

        for position_state in position_states:
            position = self.position_get(position_state.instrument)

            if position is None:
                continue

            position.unrealizedPL = position_state.netUnrealizedPL
            position.long.unrealizedPL = position_state.longUnrealizedPL
            position.short.unrealizedPL = position_state.shortUnrealizedPL

    def apply_order_states(self, order_states):
        """
        Update state for all Orders

        Args:
            order_states: A list of v20.order.DynamicOrderState objects
                          representing changes to the state of pending Orders
        """

        for order_state in order_states:
            order = self.order_get(order_state.id)

            if order is None:
                continue

            order.trailingStopValue = order_state.trailingStopValue

            self.order_states[order.id] = order_state

    def apply_state(self, state):
        """
        Update the state of an Account

        Args:
            state: A v20.account.AccountState object representing changes to
                   the Account's trades, positions, orders and state.
        """

        #
        # Update Account details from the state
        #
        for field in state.fields():
            update_attribute(self.details, field.name, field.value)

        self.apply_trade_states(state.trades)

        self.apply_position_states(state.positions)

        self.apply_order_states(state.orders)
