import common.view


def print_orders_map(orders_map):
    """
    Print a map of Order Summaries in table format.

    Args:
        orders_map: The map of id->Order to print
    """

    print_orders(
        sorted(
            orders_map.values(),
            key=lambda o: o.id
        )
    )


def print_orders(orders):
    """
    Print a collection or Orders in table format.

    Args:
        orders: The list or Orders to print
    """

    #
    # Mapping from Order type to human-readable name
    #
    order_names = {
        "STOP": "Stop",
        "LIMIT": "Limit",
        "MARKET": "Market",
        "MARKET_IF_TOUCHED": "Entry",
        "ONE_CANCELS_ALL": "One Cancels All",
        "TAKE_PROFIT": "Take Profit",
        "STOP_LOSS": "Stop Loss",
        "TRAILING_STOP_LOSS": "Trailing Stop Loss"
    }

    #
    # Print the Orders in a table with their ID, type, state, and summary
    #
    common.view.print_collection(
        "{} Orders".format(len(orders)),
        orders,
        [
            ("ID", lambda o: o.id),
            ("Type", lambda o: order_names.get(o.type, o.type)),
            ("State", lambda o: o.state),
            ("Summary", lambda o: o.summary()),
        ]
    )

    print("")


def print_order_create_response_transactions(response):
    """
    Print out the transactions found in the order create response
    """

    common.view.print_response_entity(
        response, None,
        "Order Create",
        "orderCreateTransaction"
    )

    common.view.print_response_entity(
        response, None,
        "Long Order Create",
        "longOrderCreateTransaction"
    )

    common.view.print_response_entity(
        response, None,
        "Short Order Create",
        "shortOrderCreateTransaction"
    )

    common.view.print_response_entity(
        response, None,
        "Order Fill",
        "orderFillTransaction"
    )

    common.view.print_response_entity(
        response, None,
        "Long Order Fill",
        "longOrderFillTransaction"
    )

    common.view.print_response_entity(
        response, None,
        "Short Order Fill",
        "shortOrderFillTransaction"
    )

    common.view.print_response_entity(
        response, None,
        "Order Cancel",
        "orderCancelTransaction"
    )

    common.view.print_response_entity(
        response, None,
        "Long Order Cancel",
        "longOrderCancelTransaction"
    )

    common.view.print_response_entity(
        response, None,
        "Short Order Cancel",
        "shortOrderCancelTransaction"
    )

    common.view.print_response_entity(
        response, None,
        "Order Reissue",
        "orderReissueTransaction"
    )

    common.view.print_response_entity(
        response, None,
        "Order Reject",
        "orderRejectTransaction"
    )

    common.view.print_response_entity(
        response, None,
        "Order Reissue Reject",
        "orderReissueRejectTransaction"
    )

    common.view.print_response_entity(
        response, None,
        "Replacing Order Cancel",
        "replacingOrderCancelTransaction"
    )
