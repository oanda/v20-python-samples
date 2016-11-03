#!/usr/bin/env python

import argparse
import common.args
from order.view import print_order_create_response_transactions
import v20


def main():
    """
    Create a Market Order in an Account based on the provided command-line
    arguments.
    """

    parser = argparse.ArgumentParser()

    #
    # Add arguments for API connection
    #
    parser.add_argument(
        "--hostname",
        default="api-fxpractice.oanda.com",
        help="v20 REST Server hostname"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=443,
        help="v20 REST Server port"
    )

    #
    # Add Account arguments
    #
    parser.add_argument(
        "--account-id",
        required=True,
        help="v20 Account ID"
    )

    parser.add_argument(
        "--token",
        required=True,
        help="v20 Auth Token"
    )

    #
    # Add arguments for minimal Market Order
    #
    parser.add_argument(
        "--instrument",
        type=common.args.instrument,
        required=True,
        help="The instrument to place the Market Order for"
    )

    parser.add_argument(
        "--units",
        required=True,
        help="The number of units for the Market Order"
    )

    args = parser.parse_args()

    #
    # Create the API context based on the provided arguments
    #
    api = v20.Context(
        args.hostname,
        args.port,
        True
    )

    #
    # Set the auth token to use
    #
    api.set_token(args.token)

    #
    # Extract the Account ID from the arguments
    #
    account_id = args.account_id

    #
    # Submit the request to create the Market Order
    #
    response = api.order.market(
        account_id,
        instrument=args.instrument,
        units=args.units
    )

    #
    # Process the response
    #
    print("Response: {} ({})".format(response.status, response.reason))

    print("")

    print_order_create_response_transactions(response)


if __name__ == "__main__":
    main()
