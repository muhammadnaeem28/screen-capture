import pytest
import logging
import pathlib
import yaml

from helpers import report, aws, config_loader

log = logging.getLogger(__name__)

# This global variable is sort of a hack and should be fixed at some point
# It allows us to use email/report configs in the pytest_sessionfinish() method
# The test report must be generated before emailing/uploading so we can be sure
# it exists when method pytest_sessionfinish() is called.
test_report_config = {
    "report_s3_upload": False,
    "report_s3_bucket": ""
}


@pytest.fixture(scope='session', autouse=True)
def configs():
    global test_report_config

    # Create an instance of TestConfig with the loaded config data
    test_config = config_loader.TestConfig()

    # Fill in the global report configs object
    test_report_config = {
        "report_s3_upload": test_config.config["report"]["s3_upload"]["enabled"],
        "report_s3_bucket": test_config.config["report"]["s3_upload"]["bucket"],
        "aws_region": test_config.config["aws"]["default_region"]
    }

    return test_config


@pytest.fixture(scope="module", autouse=False)
def service_configs(configs, request):
    # Verify the env config value is set
    if configs.config["env"] == "":
        log.error("error getting service configs; env config value is empty")
        return {}

    # Get the config filename and path
    # The expected path of the service config is as follows:
    #   <test directory>/<env>.yml
    # So for example, in the stage environment for a products test,
    # the following config file is loaded and returned: tests/products/stage.yml
    config_filename = configs.config["env"] + ".yml"
    config_path = request.fspath.join("..").join(config_filename)

    # Verify file exists
    if not pathlib.Path(config_path).is_file():
        log.error("error getting service configs; config file does not exist in test directory: " + str(config_path))
        return {}

    # Load the yaml file and return the dict
    with open(config_path, 'r') as stream:
        try:
            config_dict = yaml.safe_load(stream)
        except yaml.YAMLError as err:
            log.error("error getting service configs; error loading yaml config file: " + str(err))
            return {}

    return config_dict




def pytest_configure(config):
    """
    Allows plugins and conftest files to perform initial configuration.
    This hook is called for every plugin and initial conftest
    file after command line options have been parsed.
    """
    pass


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    pass


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    # Email the test report if enabled
    # Upload test report to S3
    if test_report_config["report_s3_upload"]:
        report.upload_report_s3(
            report_location="report/report.html",
            bucket_name=test_report_config["report_s3_bucket"],
            aws_region=test_report_config["aws_region"]
        )
    # TODO upload log file also?

    log.info("Test completed with status code: " + str(exitstatus))


def pytest_unconfigure(config):
    """
    called before test process is exited.
    """
    pass
