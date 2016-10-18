import common.view

def print_positions(positions, open_only=True):
    """Print a collection or Positions in table format.

    Args:
        positions: The list of Positions to print
        open_only: Flag that controls if only open Positions are displayed
    """

    def position_side_formatter(side_name):
        """Create a formatter that extracts and formats the long or short side
        from a Position

        Args:
            side_name: "long" or "short" indicating which side of the position to format
        """
        def f(p):
            """The formatting function for the long or short side"""

            side = getattr(p, side_name)

            if side is None:
                return ""
            if side.units == "0":
                return ""

            return "{} @ {}".format(side.units, side.averagePrice)

        return f

    filtered_positions = [
        p for p in positions 
        if not open_only or p.long.units != "0" or p.short.units != "0"
    ]

    #
    # Print the Trades in a table with their Instrument, realized PL,
    # unrealized PL long postion summary and shor position summary
    #
    common.view.print_collection(
        "{} Positions".format(len(filtered_positions)),
        filtered_positions,
        [
            ("Instrument", lambda p: p.instrument),
            ("P/L", lambda p: p.pl),
            ("Unrealized P/L", lambda p: p.unrealizedPL),
            ("Long", position_side_formatter("long")),
            ("Short", position_side_formatter("short")),
        ]
    )


