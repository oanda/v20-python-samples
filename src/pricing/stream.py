#!/usr/bin/env python

import argparse
import common.config
import common.args
from .view import price_to_string, heartbeat_to_string


def main():
    """
    Stream the prices for a list of Instruments for the active Account.
    """

    parser = argparse.ArgumentParser()

    common.config.add_argument(parser)

    parser.add_argument(
        '--instrument', "-i",
        type=common.args.instrument,
        required=True,
        action="append",
        help="Instrument to get prices for"
    )

    parser.add_argument(
        '--snapshot',
        action="store_true",
        default=True,
        help="Request an initial snapshot"
    )

    parser.add_argument(
        '--no-snapshot',
        dest="snapshot",
        action="store_false",
        help="Do not request an initial snapshot"
    )

    parser.add_argument(
        '--show-heartbeats', "-s",
        action='store_true',
        default=False,
        help="display heartbeats"
    )

    args = parser.parse_args()

    account_id = args.config.active_account

    api = args.config.create_streaming_context()

    # api.set_convert_decimal_number_to_native(False)

    # api.set_stream_timeout(3)

    #
    # Subscribe to the pricing stream
    #
    response = api.pricing.stream(
        account_id,
        snapshot=args.snapshot,
        instruments=",".join(args.instrument),
    )

    #
    # Print out each price as it is received
    #
    for msg_type, msg in response.parts():
        if msg_type == "pricing.Heartbeat" and args.show_heartbeats:
            print(heartbeat_to_string(msg))
        elif msg_type == "pricing.Price":
            print(price_to_string(msg))


if __name__ == "__main__":
    main()
