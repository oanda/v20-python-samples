from datetime import datetime
import argparse
import v20.transaction

def instrument(i):
    return i.replace("/", "_")

def date_time(fmt="%Y-%m-%d %H:%M:%S"):
    def parse(s):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            msg = "Not a valid date: '{0}'.".format(s)
            raise argparse.ArgumentTypeError(msg)

    return parse
