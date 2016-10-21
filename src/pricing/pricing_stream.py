#!/usr/bin/env python

import argparse
import common.config
import os.path


def main():
    parser = argparse.ArgumentParser()
    common.config.add_argument(parser)
    args = parser.parse_args()

    account_id = args.config.active_account
    
    api = args.config.create_streaming_context()

    response = api.pricing.stream(
        account_id,
        snapshot=True,
        instruments="EUR_USD,USD_CAD"
    )
    
    for msg_type, msg in response.parts():
        if msg_type == "pricing.Heartbeat":
            continue

        base_bid = msg.bids[0].price
        base_ask = msg.asks[0].price

        prefix = os.path.commonprefix([base_bid, base_ask])

        print "{} {}{}/{}".format(
            msg.instrument,
            prefix,
            base_bid[len(prefix):],
            base_ask[len(prefix):]
        )


if __name__ == "__main__":
    main()
