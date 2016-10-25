#!/usr/bin/env python

import argparse
import common.config
import common.args
from view import CandlePrinter
from datetime import datetime


def main():
    """
    Create an API context, and use it to fetch candles for an instrument.

    The configuration for the context is parsed from the config file provided
    as an argumentV
    """

    parser = argparse.ArgumentParser()

    #
    # The config object is initialized by the argument parser, and contains
    # the REST APID host, port, accountID, etc.
    #
    common.config.add_argument(parser)

    parser.add_argument(
        "--instrument",
        type=common.args.instrument,
        required=True,
        help="The instrument to get candles for"
    )

    parser.add_argument(
        "--mid", 
        action='store_true',
        help="Get midpoint-based candles"
    )

    parser.add_argument(
        "--bid", 
        action='store_true',
        help="Get bid-based candles"
    )

    parser.add_argument(
        "--ask", 
        action='store_true',
        help="Get ask-based candles"
    )

    parser.add_argument(
        "--smooth", 
        action='store_true',
        help="'Smooth' the candles"
    )

    parser.set_defaults(mid=False, bid=False, ask=False)

    parser.add_argument(
        "--granularity",
        default=None,
        help="The candles granularity to fetch"
    )

    parser.add_argument(
        "--count",
        default=None,
        help="The number of candles to fetch"
    )

    date_format = "%Y-%m-%d %H:%M:%S"

    parser.add_argument(
        "--from-time",
        default=None,
        type=common.args.date_time(),
        help="The start date for the candles to be fetched. Format is 'YYYY-MM-DD HH:MM:SS'"
    )

    parser.add_argument(
        "--to-time",
        default=None,
        type=common.args.date_time(),
        help="The end date for the candles to be fetched. Format is 'YYYY-MM-DD HH:MM:SS'"
    )

    args = parser.parse_args()

    account_id = args.config.active_account

    #
    # The v20 config object creates the v20.Context for us based on the
    # contents of the config file.
    #
    api = args.config.create_context()

    kwargs = {}

    if args.granularity is not None:
        kwargs["granularity"] = args.granularity

    if args.smooth is not None:
        kwargs["smooth"] = args.smooth

    if args.count is not None:
        kwargs["count"] = args.count

    if args.from_time is not None:
        kwargs["fromTime"] = args.from_time.strftime("%Y-%m-%dT%H:%M:%S.000000000Z")

    if args.to_time is not None:
        kwargs["toTime"] = args.to_time.strftime("%Y-%m-%dT%H:%M:%S.000000000Z")

    price = "mid"

    if args.mid:
        kwargs["price"] = "M" + kwargs.get("price", "")
        price = "mid"

    if args.bid:
        kwargs["price"] = "B" + kwargs.get("price", "")
        price = "bid"

    if args.ask:
        kwargs["price"] = "A" + kwargs.get("price", "")
        price = "ask"

    #
    # Fetch the candles
    #
    response = api.instrument.candles(args.instrument, **kwargs)

    if response.status != 200:
        print response
        print response.body
        return

    print "Instrument: {}".format(response.get("instrument", 200))
    print "Granularity: {}".format(response.get("granularity", 200))

    printer = CandlePrinter()

    printer.print_header()

    candles = response.get("candles", 200)

    for candle in response.get("candles", 200):
        printer.print_candle(candle)


if __name__ == "__main__":
    main()
