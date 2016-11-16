from __future__ import print_function
import yaml
import os
import sys
import v20

from common import input


#
# The default environment variable that points to the location of the v20
# configuration file
#
DEFAULT_ENV = "V20_CONF"

#
# The default path for the v20 configuration file
#
DEFAULT_PATH = "~/.v20.conf"


class ConfigPathError(Exception):
    """
    Exception that indicates that the path specifed for a v20 config file
    location doesn't exist
    """

    def __init__(self, path):
        self.path = path

    def __str__(self):
        return "Config file '{}' could not be loaded.".format(self.path)


class ConfigValueError(Exception):
    """
    Exception that indicates that the v20 configuration file is missing
    a required value
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Config is missing value for '{}'.".format(self.value)


class Config(object):
    """
    The Config object encapsulates all of the configuration required to create
    a v20 API context and configure it to work with a specific Account. 

    Using the Config object enables the scripts to exist without many command
    line arguments (host, token, accountID, etc)
    """
    def __init__(self):
        """
        Initialize an empty Config object
        """
        self.hostname = None
        self.streaming_hostname = None
        self.port = 443
        self.ssl = True
        self.token = None
        self.username = None
        self.accounts = []
        self.active_account = None
        self.path = None
        self.datetime_format = "RFC3339"

    def __str__(self):
        """
        Create the string (YAML) representaion of the Config instance 
        """

        s = ""
        s += "hostname: {}\n".format(self.hostname)
        s += "streaming_hostname: {}\n".format(self.streaming_hostname)
        s += "port: {}\n".format(self.port)
        s += "ssl: {}\n".format(str(self.ssl).lower())
        s += "token: {}\n".format(self.token)
        s += "username: {}\n".format(self.username)
        s += "datetime_format: {}\n".format(self.datetime_format)
        s += "accounts:\n"
        for a in self.accounts:
            s += "- {}\n".format(a)
        s += "active_account: {}".format(self.active_account)

        return s

    def dump(self, path):
        """
        Dump the YAML representation of the Config instance to a file.

        Args:
            path: The location to write the config YAML
        """

        path = os.path.expanduser(path)

        with open(path, "w") as f:
            print(str(self), file=f)

    def load(self, path):
        """
        Load the YAML config representation from a file into the Config instance

        Args:
            path: The location to read the config YAML from
        """

        self.path = path

        try:
            with open(os.path.expanduser(path)) as f:
                y = yaml.load(f)
                self.hostname = y.get("hostname", self.hostname)
                self.streaming_hostname = y.get(
                    "streaming_hostname", self.streaming_hostname
                )
                self.port = y.get("port", self.port)
                self.ssl = y.get("ssl", self.ssl)
                self.username = y.get("username", self.username)
                self.token = y.get("token", self.token)
                self.accounts = y.get("accounts", self.accounts)
                self.active_account = y.get(
                    "active_account", self.active_account
                )
                self.datetime_format = y.get("datetime_format", self.datetime_format)
        except:
            raise ConfigPathError(path)

    def validate(self):
        """
        Ensure that the Config instance is valid
        """

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
        if self.datetime_format is None:
            raise ConfigValueError("datetime_format")

    def update_from_input(self):
        """
        Populate the configuration instance by interacting with the user using
        prompts
        """

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
        print("")

        self.username = input.get_string("Enter username", self.username)

        print("> username is: {}".format(self.username))
        print("")

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

        if response.status != 200:
            print(response)
            sys.exit()

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

        print("")

        self.active_account = input.get_from_list(
            self.accounts,
            "Available Accounts:",
            "Select Active Account",
            index
        )

        print("> Active Account is: {}".format(self.active_account))
        print("")

        time_formats = ["RFC3339", "UNIX"]

        index = 0

        try:
            index = time_formats.index(self.datetime_format)
        except:
            pass

        self.datetime_format = input.get_from_list(
            time_formats,
            "Available Time Formats:",
            "Select Time Format",
            index
        )

    def create_context(self):
        """
        Initialize an API context based on the Config instance
        """
        ctx = v20.Context(
            self.hostname,
            self.port,
            self.ssl,
            application="sample_code",
            token=self.token,
            datetime_format=self.datetime_format
        )

        return ctx

    def create_streaming_context(self):
        """
        Initialize a streaming API context based on the Config instance
        """
        ctx = v20.Context(
            self.streaming_hostname,
            self.port,
            self.ssl,
            application="sample_code",
            token=self.token,
            datetime_format=self.datetime_format
        )

        return ctx


def make_config_instance(path):
    """
    Create a Config instance, load its state from the provided path and 
    ensure that it is valid.

    Args:
        path: The location of the configuration file
    """

    config = Config()

    config.load(path)

    config.validate()

    return config


def default_config_path():
    """
    Calculate the default configuration file path. 

    The default is first selected to be the contents of the V20_CONF
    environment variable, followed by the default path ~/.v20.conf
    """

    global DEFAULT_ENV
    global DEFAULT_PATH

    return os.environ.get(DEFAULT_ENV, DEFAULT_PATH)


def add_argument(parser):
    """
    Add the --config argument to an ArgumentParser that enables the creation of
    a Config instance. The user is required to provide the path to load the
    configuration from, else the parser falls back to the location specified in
    the V20_CONF environment variable followed by the default config file
    location of ~/.v20.conf

    Args:
        parser: The ArgumentParser to add the config option to
    """
    global DEFAULT_ENV
    global DEFAULT_PATH

    parser.add_argument(
        "--config",
        type=make_config_instance,
        default=default_config_path(),
        help="The location of the v20 config file to load. "
             "This defaults to the file set in the ${} "
             "environment variable, followed by file {}".format(
                 DEFAULT_ENV,
                 DEFAULT_PATH
             )
    )
