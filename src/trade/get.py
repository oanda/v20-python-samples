#!/usr/bin/env python

import argparse
import common.config
import common.view


def main():
    """
    Get details of a specific Trade or all open Trades in an Account
    """

    parser = argparse.ArgumentParser()

    #
    # Add the command line argument to parse to the v20 config
    #
    common.config.add_argument(parser)

    parser.add_argument(
        "--trade-id", "-t",
        help=(
            "The ID of the Trade to get. If prepended "
            "with an '@', this will be interpreted as a client Trade ID"
        )
    )

    parser.add_argument(
        "--all", "-a",
        action="store_true",
        default=False,
        help="Flag to get all open Trades in the Account"
    )

    parser.add_argument(
        "--summary", "-s",
        dest="summary",
        action="store_true",
        help="Print Trade summary instead of full details",
        default=True
    )

    parser.add_argument(
        "--verbose", "-v",
        dest="summary",
        help="Print Trade details instead of summary",
        action="store_false"
    )

    args = parser.parse_args()

    if args.trade_id is None and not args.all:
        parser.error("Must provide --trade-id or --all")

    account_id = args.config.active_account

    #
    # Create the api context based on the contents of the
    # v20 config file
    #
    api = args.config.create_context()

    if args.all:
        response = api.trade.list_open(account_id)

        if not args.summary:
            print("-" * 80)

        for trade in reversed(response.get("trades", 200)):
            if args.summary:
                print(trade.title())
            else:
                print(trade.yaml(True))
                print("-" * 80)

        return

    if args.trade_id:
        response = api.trade.get(account_id, args.trade_id)

        trade = response.get("trade", 200)

        if args.summary:
            print(trade.title())
        else:
            print(trade.yaml(True))

        return


if __name__ == "__main__":
    main()
