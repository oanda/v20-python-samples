#!/usr/bin/env python

from __future__ import print_function
import sys
import os
import argparse
import v20
import common.config
from common.arg_helper import parse_instrument
from common.view import print_response_transaction


def add_order_request_args(OrderRequestType, parser):
    for property in OrderRequestType._properties:
        if property.name == "type":
            continue

        if property.required:
            options = {
                "help": property.description
            }

            if property.typeName == "primitives.InstrumentName":
                options["type"] = parse_instrument

            if property.default:
                options["default"] = property.default
            else:
                options["default"] = argparse.SUPPRESS
                options["required"] = True

            parser.add_argument(
                "--{}".format(property.name),
                **options
            )

        elif property.typeClass == "primitive":

            options = {
                "help": property.description
            }

            if property.typeName == "primitives.InstrumentName":
                options["type"] = parse_instrument

            if property.default:
                options["default"] = property.default
            else:
                options["default"] = argparse.SUPPRESS

            parser.add_argument(
                "--{}".format(property.name),
                **options
            )
        elif property.typeClass == "object":
            pass
            # print(property.name)


def main():
    order_map = {
        "market_order.py" : v20.order.MarketOrderRequest,
        "limit_order.py" : v20.order.LimitOrderRequest,
        "entry_order.py" : v20.order.MarketIfTouchedOrderRequest,
        "stop_order.py" : v20.order.StopOrderRequest,
        "take_profit_order.py" : v20.order.TakeProfitOrderRequest,
        "stop_loss_order.py" : v20.order.StopLossOrderRequest,
        "trailing_stop_loss_order.py" : v20.order.TrailingStopLossOrderRequest
    }

    #
    # Use the symbolic link (argv[0]) to determine what kind of order is being
    # created
    #
    OrderRequestType = order_map.get( 
        os.path.basename(sys.argv[0])
    )

    if OrderRequestType is None:
        print("Unknown Order Type")
        sys.exit()

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    common.config.add_argument(parser)

    add_order_request_args(OrderRequestType, parser)

    args = parser.parse_args()

    args_dict = vars(args)

    account_id = args.config.active_account

    api = args.config.create_context()

    response = api.order.create(
        account_id,
        order=OrderRequestType(**args_dict)
    )

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
