#!/usr/bin/env python

import common.config
import common.input


def main():
    """
    Load an existing v20.conf file, update it interactively, and save it
    back to a file.
    """

    config = common.config.Config()

    filename = common.input.get_string(
        "Enter existing v20.conf filename to load",
        common.config.default_config_path()
    )

    try:
        config.load(filename)
    except Exception:
        print("Config file '{}' doesn't exist, starting with defaults.".format(
            filename
        ))
        print

    print("")
    print("------------ Initial v20 configuration -------------")
    print(str(config))
    print("----------------------------------------------------")
    print("")

    config.update_from_input()

    print("")
    print("-------------- New v20 configuration --------------")
    print(str(config))
    print("---------------------------------------------------")
    print("")

    dump = common.input.get_yn(
        "Dump v20 configuration to {}?".format(filename),
        True
    )

    if dump:
        config.dump(filename)


if __name__ == "__main__":
    main()
