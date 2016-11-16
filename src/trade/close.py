#!/usr/bin/env python

import argparse
import common.config
import common.view
from order.view import print_order_create_response_transactions


def main():
    """
    Close an open Trade in an Account
    """

    parser = argparse.ArgumentParser()

    #
    # Add the command line argument to parse to the v20 config
    #
    common.config.add_argument(parser)

    parser.add_argument(
        "tradeid",
        help=(
            "The ID of the Trade to close. If prepended "
            "with an '@', this will be interpreted as a client Trade ID"
        )
    )

    parser.add_argument(
        "--units",
        default="ALL",
        help=(
            "The amount of the Trade to close. Either the string 'ALL' "
            "indicating a full Trade close, or the number of units of the "
            "Trade to close. This number must always be positive and may "
            "not exceed the magnitude of the Trade's open units"
        )
    )

    args = parser.parse_args()

    account_id = args.config.active_account

    #
    # Create the api context based on the contents of the
    # v20 config file
    #
    api = args.config.create_context()

    response = api.trade.close(
        account_id,
        args.tradeid,
        units=args.units
    )

    print(
        "Response: {} ({})\n".format(
            response.status,
            response.reason
        )
    )

    print_order_create_response_transactions(response)


if __name__ == "__main__":
    main()
