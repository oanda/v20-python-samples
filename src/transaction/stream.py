#!/usr/bin/env python

import argparse
import common.config


def main():
    """
    Stream Transactions for the active Account
    """

    parser = argparse.ArgumentParser()

    common.config.add_argument(parser)

    parser.add_argument(
        '--show-heartbeats',
        action='store_true',
        default=False,
        help="display heartbeats"
    )

    args = parser.parse_args()

    account_id = args.config.active_account

    api = args.config.create_streaming_context()

    response = api.transaction.stream(account_id)

    for _, msg in response.parts():
        if msg.type == "HEARTBEAT" and not args.show_heartbeats:
            continue

        print(msg.summary())


if __name__ == "__main__":
    main()
