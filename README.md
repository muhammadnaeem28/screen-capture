# Regression Test Suite for Core and Facade Services

A QA automation test suite for Dotcom services developed in Python using pytest.

### Download the Source

First clone the repo to a local folder if you haven't already:
```
~/.../dotcom/QAAutomation$ git clone https://gitlab.hallmarklabs.com/dotcom/qaautomation/core-services.git
```

And `cd` to the `core-services` directory. All future commands assume you'll be in `/core-services`.

### Setup Python and Virtualenv

Install Python3 if you don't have it already.

Install python virtualenv:
```
pip install virtualenv
```

To verify you have these installed:
```
python --version
virtualenv --version
```

Create the virtualenv, activate it and install dependencies. Dependencies for the project are in the `requirements.txt` file.
```
mkdir .venv
virtualenv .venv/
source ./.venv/bin/activate
pip3 install -r requirements.txt
```
After activating your virtualenv, you should see a `(.venv)` in the front of your console command line.

While in your virtualenv, if you require additional python packages, install them as follows: `pip3 install <package name>`

To include this package dependency in the `requirements.txt` file, you must do the following:
```
pip3 freeze > requirements.txt
```

To deacticate virtualenv:
```
deactivate
```

### Updating Configurations

Initially the repo has a `configs/local.yml.template` file. This file contains configuration parameters required to run the tests. The `.template` signifies it's a template and must be modified and `local` signifies it's for running localy (against services in the dev environment). There's values missing in this template because some information is sensitive and shouldn't be merged into the repo.

Copy this file to a `local.yml` file:
```
cp configs/local.yml.template configs/local.yml
```

The missing values in the `local.yml` must be filled in. You can get these values from Secrets Manager if you have access or from a qa/developer friend. Don't worry, you only have to do this once.

Note, the `configs/dev.yml` configuration file is used when running tests in the pipeline against the dev environment.

### Running the Regression

To run, while in your virtualenv:
```
pytest --tc-file=configs/local.yml
```
This sources the `configs/local.yml` configuration file for the test run.

All the configuration related to pytest is in the `pytest.ini` file. You can change command line options and logging level for example in this file. If you add `--tc-file=configs/local.yml` to the end of `addopts = ` on line 2, you can tell pytest to source in the configuration file automatically and then simply run `pytest` to run all tests.

To speed up test execution, specify the `-n` option with the number of parallel workers:
```
pytest --tc-file=configs/local.yml -n 5
```

To run a specific test use the `-k` option:
```
pytest --tc-file=configs/local.yml -k test_get_client_token_integration_with_authorization
pytest tests/auth/test_auth_sessions.py --tc-file=configs/local.yml -k test_health
```

### Test Markers

Individual tests can be marked with a `@pytest.mark` decorator, for example:
```
@pytest.mark.health
def test_health():
    # do something...
```

This "tags" the test with a marker, that can be refered to later when executing tests. A test can be marked with any number of markers.

To run a specific set of marked tests, use the `-m` option:
```
pytest --tc-file=configs/dev.yml -m health
```

To view all markers:
```
pytest --markers
```

### Docker

To run the regression through a docker container, first build it:
```
docker-compose build
```

And then run it:
```
docker-compose up
```

The `docker-compose.yml` file is already configured to source `configs/local.yml` for test configuration. The docker compose file has the line `"core-services.dev.dotcom.hmklabs.com:192.168.65.2"` configured for `extra_hosts`. This helps to route traffic for core services out the correct interface in the container. For this to work you'll have to be connected to the AWS Bastion SSH Instance and your `local.yml` config file will have to have the appropriate `core_base_url`, such as:
```
core_base_url: https://core-services.dev.dotcom.hmklabs.com:8080
```

After adding or updating tests, you don't have to build again, just run it. You will have to build again if you update the `requirements.txt` file.

Note, you don't have to be in your virtualenv to run the above docker commands.

### AWS

This framework can pull secrets from Secrets Manager and can upload the test report to S3. By default these features are disabled (configured in the yml config file).

While running in the venv, you can enable these features by setting `REPORT_S3_UPLOAD=true` and `SECRETS_LOAD=true` in the `local.yml` file. If these are enabled, it'll require AWS credentials. The easiest way to do this is to set the `AWS_PROFILE` env variable to a valid profile in your AWS config file, for example `AWS_PROFILE=dotcom-dev`. If your config profile requires a MFA code, the test will ask you to enter an MFA code while it's running. Enter the code and the test should continue executing.

If your AWS config profile requires an MFA code, running the test suite through Docker with the AWS features enabled will not work (unless you can figure it out). This is not a problem when the test suite runs in the environments (through the pipeline) as a MFA code is not required.

### Test Report and Emailing

TODO

### Pytest Log file

TODO

### Secerts from SecretsManager

TODO