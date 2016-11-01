import common.view


def print_trades_map(trades_map):
    """
    Print a map of Trade Summaries in table format.

    Args:
        orders_map: The map of id->Trade to print
    """

    print_trades(
        sorted(
            trades_map.values(),
            key=lambda t: t.id
        )
    )


def print_trades(trades):
    """
    Print a collection or Trades in table format.

    Args:
        trades: The list of Trades to print
    """

    #
    # Print the Trades in a table with their ID, state, summary, upl and pl
    #
    common.view.print_collection(
        "{} Trades".format(len(trades)),
        trades,
        [
            ("ID", lambda t: t.id),
            ("State", lambda t: t.state),
            ("Summary", lambda t: t.summary()),
            ("Unrealized P/L", lambda t: t.unrealizedPL),
            ("P/L", lambda t: t.realizedPL)
        ]
    )

    print("")
