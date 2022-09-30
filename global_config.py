# NOTE: Do not adding anything here unless you absolutely have to
# It allows certain configuration parameters to be injected into non-test methods
# such as in the helpers. All test-related configuration parameters should be
# specified in the yaml config file (if required) and injected through test fixtures.
# The values here will be set when loading the configs in config_loader.py
# If there's a better way of doing it, we should remove this file.

# When testing locally, SSL certifcate validation will fail when connecting to core services
# through the bastion host. This value will be set to false for local executions to disable
# the cert validation.
validate_ssl_cert = True
