#!/usr/bin/env python

import argparse
import common.config
from .args import OrderArguments, add_replace_order_id_argument
from .view import print_order_create_response_transactions


def main():
    """
    Create or replace an OANDA Limit Order in an Account based on the provided
    command-line arguments.
    """

    parser = argparse.ArgumentParser()

    #
    # Add the command line argument to parse to the v20 config
    #
    common.config.add_argument(parser)

    #
    # Add the argument to support replacing an existing argument
    #
    add_replace_order_id_argument(parser)

    #
    # Add the command line arguments required for a Limit Order
    #
    orderArgs = OrderArguments(parser)
    orderArgs.add_instrument()
    orderArgs.add_units()
    orderArgs.add_price()
    orderArgs.add_time_in_force()
    orderArgs.add_position_fill()
    orderArgs.add_take_profit_on_fill()
    orderArgs.add_stop_loss_on_fill()
    orderArgs.add_trailing_stop_loss_on_fill()
    orderArgs.add_client_order_extensions()
    orderArgs.add_client_trade_extensions()

    args = parser.parse_args()

    #
    # Create the api context based on the contents of the
    # v20 config file
    #
    api = args.config.create_context()

    #
    # Use the api context's datetime formatter when serializing data
    #
    orderArgs.set_datetime_formatter(lambda dt: api.datetime_to_str(dt))

    #
    # Extract the Limit Order parameters from the parsed arguments
    #
    orderArgs.parse_arguments(args)

    if args.replace_order_id is not None:
        #
        # Submit the request to cancel and replace a Limit Order
        #
        response = api.order.limit_replace(
            args.config.active_account,
            args.replace_order_id,
            **orderArgs.parsed_args
        )
    else:
        #
        # Submit the request to create a Limit Order
        #
        response = api.order.limit(
            args.config.active_account,
            **orderArgs.parsed_args
        )

    print("Response: {} ({})".format(response.status, response.reason))
    print("")

    print_order_create_response_transactions(response)


if __name__ == "__main__":
    main()
