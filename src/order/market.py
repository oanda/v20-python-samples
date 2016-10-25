#!/usr/bin/env python

import argparse
import common.config
import common.arg_helper
from args import OrderArguments
from v20.order import MarketOrderRequest
from common.view import print_response_transaction


def main():

    parser = argparse.ArgumentParser()

    #
    # Add the command line argument to parse to the v20 config
    #
    common.config.add_argument(parser)

    #
    # Add the command line arguments required for a Market Order
    #
    orderArgs = OrderArguments(parser)
    orderArgs.add_instrument()
    orderArgs.add_units()
    orderArgs.add_time_in_force(["FOK", "IOC"])
    orderArgs.add_price_bound()
    orderArgs.add_position_fill()
    orderArgs.add_take_profit_on_fill()
    orderArgs.add_stop_loss_on_fill()
    orderArgs.add_trailing_stop_loss_on_fill()
    orderArgs.add_client_order_extensions()
    orderArgs.add_client_trade_extensions()

    args = parser.parse_args()

    #
    # Extract the Market order parameters from the parsed arguments
    #
    orderArgs.parse_arguments(args)

    account_id = args.config.active_account

    api = args.config.create_context()

    #
    # Create a MarketOrderRequest from the parsed arguments
    #
    order_request = MarketOrderRequest(**orderArgs.order_request)

    #
    # Submit the request to create the Market Order
    #
    response = api.order.create(account_id, order=order_request)

    if response.status / 100 != 2:
        print "Error {}: {}".format (response.status, response.body)
        return

    #
    # Print out the resulting transactions if they exist in the response
    #
    print_response_transaction(
        response, 201, "Order Create", "orderCreateTransaction"
    )

    print_response_transaction(
        response, 201, "Order Fill", "orderFillTransaction"
    )

    print_response_transaction(
        response, 201, "Order Cancel", "orderCancelTransaction"
    )

    print_response_transaction(
        response, 201, "Order Reissue", "orderReissueTransaction"
    )

    print_response_transaction(
        response, 400, "Order Reject", "orderRejectTransaction"
    )


if __name__ == "__main__":
    main()
