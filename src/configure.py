#!/usr/bin/env python

from __future__ import print_function

import sys
import os
import v20
import common.config
import common.input


def main():

    config = common.config.Config()

    filename = common.input.get_string(
        "Enter v20.conf filename",
        common.config.path()
    )

    try:
        config.load(filename)
    except:
        print(
            "Config file '{}' doesn't exist, starting with defaults.".
            format(filename)
        )
        print()

    print("intitial v20 configuration follows:")
    print("---")
    print(str(config),)
    print("---")
    print()

    config.update_from_input()

    print("v20 configuration follows:")
    print("---")
    print(str(config),)
    print("---")
    print()

    dump = common.input.get_yn(
        "Dump v20 configuration to {}?".format(filename),
        True
    )

    if dump:
        config.dump(filename)


if __name__ == "__main__":
    main()
