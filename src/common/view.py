from __future__ import print_function

import sys

from tabulate import tabulate


def print_title(s):
    print(s)
    print(len(s) * "=")
    print()


def print_subtitle(s):
    print(s)
    print(len(s) * "-")
    print()


def print_entity(title, entity):
    if title is not None and len(title) > 0:
        print_title(title)

    headers = ["Name", "Value"]
    tablefmt = "fancy_grid"
    body = []

    for field in entity.fields():
        name = field.displayName
        value = field.value
        if field.typeClass.startswith("array"):
            value = "[{}]".format(len(field.value))
        elif field.typeClass.startswith("object"):
            value = "<{}>".format(field.typeName)
        body.append([name, value])

    getattr(sys.stdout, 'buffer', sys.stdout).write(
        tabulate
        (
            body,
            headers,
            tablefmt=tablefmt
        ).encode('utf-8')
    )
    print()


def print_collection(title, entities, columns):
    if len(entities) == 0:
        return

    if title is not None and len(title) > 0:
        print_title(title)

    headers = [c[0] for c in columns]
    tablefmt = "fancy_grid"
    body = []

    for e in entities:
        body.append([c[1](e) for c in columns])

    getattr(sys.stdout, 'buffer', sys.stdout).write(
        tabulate
        (
            body,
            headers,
            tablefmt=tablefmt
        ).encode('utf-8')
    )
    print()


def print_trade_summaries(trades):
    print_collection(
        "Open Trades",
        trades,
        [
            ("ID", lambda t: t.id),
            ("Summary", lambda t: t.summary()),
            ("Unrealized P/L", lambda t: t.unrealizedPL)
        ]
    )

def print_trades(trades):
    def dependentOrders(trade):
        tp = "-" 
        if trade.takeProfitOrder is not None:
            tp = trade.takeProfitOrder.price 
        sl = "-" 
        if trade.stopLossOrder is not None:
            sl = trade.stopLossOrder.price 
        tsl = "-" 
        if trade.trailingStopLossOrder is not None:
            tsl = trade.trailingStopLossOrder.trailingStopValue 
        return "{}/{}/{}".format(tp, sl, tsl)

    print_collection(
        "Open Trades",
        trades,
        [
            ("ID", lambda t: t.id),
            ("Summary", lambda t: t.summary()),
            ("Unrealized P/L", lambda t: t.unrealizedPL),
            ("TP/SL/TSL", dependentOrders)
        ]
    )


def print_positions(positions):
    def position_side_formatter(side_name):
        def f(p):
            side = getattr(p, side_name)
            if side is None:
                return ""
            if side.units == "0":
                return ""
            return "{} @ {}".format(side.units, side.averagePrice)
        return f

    print_collection(
        "Positions",
        positions,
        [
            ("Instrument", lambda p: p.instrument),
            ("P/L", lambda p: p.pl),
            ("Unrealized P/L", lambda p: p.unrealizedPL),
            ("Long", position_side_formatter("long")),
            ("Short", position_side_formatter("short")),
        ]
    )


def print_orders(orders):
    order_names = {
        "STOP" : "Stop",
        "LIMIT" : "Limit",
        "MARKET" : "Market",
        "MARKET_IF_TOUCHED" : "Entry",
        "ONE_CANCELS_ALL" : "One Cancels All",
        "TAKE_PROFIT" : "Take Profit",
        "STOP_LOSS" : "Stop Loss",
        "TRAILING_STOP_LOSS" : "Trailing Stop Loss"
    }

    print_collection(
        "{} Pending Orders".format(len(orders)),
        orders,
        [
            ("ID", lambda o: o.id),
            ("Type", lambda o: order_names.get(o.type, o.type)),
            ("Summary", lambda o: o.summary()),
        ]
    )


def print_response_transaction(
    response,
    expected_status,
    title,
    transaction_name
):
    try:
        print_entity(
            title,
            response.get(transaction_name, expected_status)
        )
        print()
    except:
        pass
