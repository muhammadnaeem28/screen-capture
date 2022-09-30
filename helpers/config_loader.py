import json
import logging
from distutils.util import strtobool
from os import environ
from pytest_testconfig import config

import global_config
from helpers import aws

log = logging.getLogger(__name__)


# TestConfig is a structure to hold config data
class TestConfig(object):
    def __init__(self):
        self.config = config
        global_config.validate_ssl_cert = self.config["validate_ssl_cert"]