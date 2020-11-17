import common.view


def position_side_formatter(side_name):
    """
    Create a formatter that extracts and formats the long or short side from a
    Position

    Args:
        side_name: "long" or "short" indicating which side of the position to
                   format
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


def print_positions_map(positions_map, open_only=True):
    """
    Print a map of Positions in table format.

    Args:
        positions: The map of instrument->Positions to print
        open_only: Flag that controls if only open Positions are displayed
    """

    print_positions(
        sorted(
            positions_map.values(),
            key=lambda p: p.instrument
        ),
        open_only
    )


def print_positions(positions, open_only=True):
    """
    Print a list of Positions in table format.

    Args:
        positions: The list of Positions to print
        open_only: Flag that controls if only open Positions are displayed
    """

    filtered_positions = [
        p for p in positions
        if not open_only or p.long.units != "0" or p.short.units != "0"
    ]

    if len(filtered_positions) == 0:
        return

    #
    # Print the Trades in a table with their Instrument, realized PL,
    # unrealized PL long postion summary and short position summary
    #
    common.view.print_collection(
        "{} {}Positions".format(
            len(filtered_positions),
            "Open " if open_only else ""
        ),
        filtered_positions,
        [
            ("Instrument", lambda p: p.instrument),
            ("P/L", lambda p: p.pl),
            ("Unrealized P/L", lambda p: p.unrealizedPL),
            ("Long", position_side_formatter("long")),
            ("Short", position_side_formatter("short")),
        ]
    )

    print("")
