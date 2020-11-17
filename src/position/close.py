#!/usr/bin/env python

import argparse
import common.config
import common.view
import common.args
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
        "instrument",
        type=common.args.instrument,
        help=(
            "The Instrument of the Position to close. If prepended "
            "with an '@', this will be interpreted as a client Trade ID"
        )
    )

    parser.add_argument(
        "--long-units",
        default=None,
        help=(
            "The amount of the long Position to close. Either the string "
            "'ALL' indicating a full Position close, the string 'NONE', or "
            "the number of units of the Position to close"
        )
    )

    parser.add_argument(
        "--short-units",
        default=None,
        help=(
            "The amount of the short Position to close. Either the string "
            "'ALL' indicating a full Position close, the string 'NONE', or "
            "the number of units of the Position to close"
        )
    )

    args = parser.parse_args()

    account_id = args.config.active_account

    #
    # Create the api context based on the contents of the
    # v20 config file
    #
    api = args.config.create_context()

    if args.long_units is not None and args.short_units is not None:
        response = api.position.close(
            account_id,
            args.instrument,
            longUnits=args.long_units,
            shortUnits=args.short_units
        )
    elif args.long_units is not None:
        response = api.position.close(
            account_id,
            args.instrument,
            longUnits=args.long_units
        )
    elif args.short_units is not None:
        response = api.position.close(
            account_id,
            args.instrument,
            shortUnits=args.short_units
        )
    else:
        print("No units have been provided")
        return

    print(
        "Response: {} ({})\n".format(
            response.status,
            response.reason
        )
    )

    print_order_create_response_transactions(response)


if __name__ == "__main__":
    main()
