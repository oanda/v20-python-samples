from __future__ import print_function

import yaml
import os
import sys
import v20

from common import input


DEFAULT_ENV = "V20_CONF"
DEFAULT_PATH = "~/.v20.conf"


class ConfigPathError(Exception):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return "Config file '{}' could not be loaded.".format(self.path)


class ConfigValueError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Config is missing value for '{}'.".format(self.value)


class Config(object):
    def __init__(self):
        self.hostname = None
        self.streaming_hostname = None
        self.port = 443
        self.ssl = True
        self.token = None
        self.username = None
        self.accounts = []
        self.active_account = None
        self.path = None

    def __str__(self):
        s = ""
        s += "hostname: {}\n".format(self.hostname)
        s += "streaming_hostname: {}\n".format(self.streaming_hostname)
        s += "port: {}\n".format(self.port)
        s += "ssl: {}\n".format(str(self.ssl).lower())
        s += "token: {}\n".format(self.token)
        s += "username: {}\n".format(self.username)
        s += "accounts:\n"
        for a in self.accounts:
            s += "- {}\n".format(a)
        s += "active_account: {}\n".format(self.active_account)
        return s

    def dump(self, path):
        path = os.path.expanduser(path)

        with open(path, "w") as f:
            print(str(self), file=f)

    def load(self, path):
        self.path = path

        try:
            with open(os.path.expanduser(path)) as f:
                y = yaml.load(f)
                self.hostname = y.get("hostname", self.hostname)
                self.streaming_hostname = y.get("streaming_hostname", self.streaming_hostname)
                self.port = y.get("port", self.port)
                self.ssl = y.get("ssl", self.ssl)
                self.username = y.get("username", self.username)
                self.token = y.get("token", self.token)
                self.accounts = y.get("accounts", self.accounts)
                self.active_account = y.get("active_account", self.active_account)
        except:
            raise ConfigPathError(path)

    def validate(self):
        if self.hostname is None:
            raise ConfigValueError("hostname")
        if self.streaming_hostname is None:
            raise ConfigValueError("hostname")
        if self.port is None:
            raise ConfigValueError("port")
        if self.ssl is None:
            raise ConfigValueError("ssl")
        if self.username is None:
            raise ConfigValueError("username")
        if self.token is None:
            raise ConfigValueError("token")
        if self.accounts is None:
            raise ConfigValueError("account")
        if self.active_account is None:
            raise ConfigValueError("account")

    def update_from_input(self):
        environments = [
            "fxtrade",
            "fxpractice"
        ]

        hostnames = [
            "api-fxtrade.oanda.com",
            "api-fxpractice.oanda.com"
        ]

        streaming_hostnames = [
            "stream-fxtrade.oanda.com",
            "stream-fxpractice.oanda.com"
        ]

        index = 0

        try:
            index = hostnames.index(self.hostname)
        except:
            pass

        environment = input.get_from_list(
            environments,
            "Available environments:",
            "Select environment",
            index
        )

        index = environments.index(environment)
        
        self.hostname = hostnames[index]
        self.streaming_hostname = streaming_hostnames[index]

        print("> API host selected is: {}".format(self.hostname))
        print("> Streaming host selected is: {}".format(self.streaming_hostname))
        print()

        self.username = input.get_string("Enter username", self.username)

        print("> username is: {}".format(self.username))
        print()

        self.token = input.get_string("Enter personal access token", self.token)

        print("> Using personal access token: {}".format(self.token))

        ctx = v20.Context(
            self.hostname,
            self.port,
            self.ssl
        )

        ctx.set_token(self.token)

        ctx_streaming = v20.Context(
            self.streaming_hostname,
            self.port,
            self.ssl
        )

        ctx_streaming.set_token(self.token)

        response = ctx.account.list()

        self.accounts = [
            account.id for account in response.body.get("accounts")
        ]

        self.accounts.sort()

        if len(self.accounts) == 0:
            print("No Accounts available")
            sys.exit()

        index = 0

        try:
            index = self.accounts.index(self.active_account)
        except:
            pass

        print()

        self.active_account = input.get_from_list(
            self.accounts,
            "Available Accounts:",
            "Select Active Account",
            index
        )

        print("> Active Account is: {}".format(self.active_account))
        print()

    def create_context(self):
        ctx = v20.Context(
            self.hostname,
            self.port,
            self.ssl,
            application="sample_code"
        )

        ctx.set_token(self.token)

        return ctx

    def create_streaming_context(self):
        ctx = v20.Context(
            self.streaming_hostname,
            self.port,
            self.ssl
        )

        ctx.set_token(self.token)

        return ctx


def make(s):
    config = Config()
    config.load(s)
    config.validate()
    return config


def path():
    global DEFAULT_ENV
    global DEFAULT_PATH

    return os.environ.get(DEFAULT_ENV, DEFAULT_PATH)


def add_argument(parser):
    global DEFAULT_ENV
    global DEFAULT_PATH

    parser.add_argument(
        "--config",
        type=make,
        default=path(),
        help="The location of the v20 config file to load. "
             "This defaults to the file set in the ${} "
             "environment variable, followed by file {}".format(
                 DEFAULT_ENV,
                 DEFAULT_PATH
             )
    )
