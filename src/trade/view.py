import common.view

def print_trade_summaries(trades):
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
