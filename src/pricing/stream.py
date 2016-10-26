#!/usr/bin/env python

import argparse
import common.config
import common.args
import view


def main():
    """
    Stream the prices for a list of Instruments for the active Account.
    """

    parser = argparse.ArgumentParser()

    common.config.add_argument(parser)
    
    parser.add_argument(
        '--instrument',
        type=common.args.instrument,
        required=True,
        action="append",
        help="Instrument to get prices for"
    )

    parser.add_argument(
        '--show-heartbeats',
        action='store_true',
        default=False,
        help="display heartbeats"
    )

    args = parser.parse_args()

    account_id = args.config.active_account
    
    api = args.config.create_streaming_context()

    #
    # Subscribe to the pricing stream
    #
    response = api.pricing.stream(
        account_id,
        snapshot=True,
        instruments=",".join(args.instrument),
    )
    
    #
    # Print out each price as it is received
    #
    for msg_type, msg in response.parts():
        if msg.type == "HEARTBEAT" and args.show_heartbeats:
            print view.heartbeat_to_string(msg)
        elif msg.type == "PRICE":
           print view.price_to_string(msg)  

if __name__ == "__main__":
    main()
