import common.view
import trade.view
import position.view
import order.view

def print_account(account):
    """Display an Account's details including open Trades, open Positions
    and pending Orders.

    Args:
        account: Account representation
    """

    common.view.print_entity(
        account.title(),
        account
    )

    print

    trade.view.print_trade_summaries(account.trades)

    print

    position.view.print_positions(account.positions)

    print

    order.view.print_order_summaries(account.orders)

    print
