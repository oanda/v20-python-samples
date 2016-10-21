#!/usr/bin/env python

import argparse
import common.config


def main():
    parser = argparse.ArgumentParser()
    common.config.add_argument(parser)
    args = parser.parse_args()

    account_id = args.config.active_account
    
    api = args.config.create_streaming_context()

    response = api.transaction.stream(account_id)
    
    for msg_type, msg in response.parts():
        print msg.summary()


if __name__ == "__main__":
    main()
