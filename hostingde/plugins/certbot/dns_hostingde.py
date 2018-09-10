"""Unofficial Hosting.de DNS Authenticator plugin.

"""
import logging
import zope.interface

from certbot import interfaces
from certbot import errors
from certbot.plugins import dns_common

from hostingde.api.dns import DnsApiClient
from hostingde.api.errors import (
    ObjectNotFoundError,
    ApiHttpStatusError,
    ApiResponseError,
)

logger = logging.getLogger(__name__)


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """Example Authenticator."""

    description = "Unofficial Hosting.de DNS Authenticator plugin"

    ttl = 60

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(
            add, default_propagation_seconds=60
        )
        add("credentials", help="Path to Hosting.de API Key file.", default=None)

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return (
            "This plugin configures a DNS TXT record to respond to a dns-01 challenge using "
            + "the Hosting.de DNS API."
        )

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            "credentials",
            "Hosting.de credentials file",
            {"apikey": "API key for Hosting.de DNS account"},
        )
        dns_common.validate_file_permissions(self.conf("credentials"))

    def _perform(self, domain, validation_domain_name, validation):
        logger.debug(
            "Attempting to perform domain validation for: [ domain: %s, validation_domain: %s, validation: %s ]",
            domain,
            validation_domain_name,
            validation,
        )
        try:
            self._getApiClient().addRecord(
                validation_domain_name, "TXT", '"{}"'.format(validation), self.ttl
            )
        except (ObjectNotFoundError, ApiHttpStatusError, ApiResponseError) as e:
            logger.error(
                "Encountered error adding TXT record. [{}]: {}".format(
                    validation_domain_name, e.message
                )
            )
            raise self._getPluginErrorFromException(e)

    def _cleanup(self, domain, validation_domain_name, validation):
        logger.debug(
            "Attempting to cleanup domain validation for: [ domain: %s, validation_domain: %s, validation: %s ]",
            domain,
            validation_domain_name,
            validation,
        )
        try:
            self._getApiClient().deleteRecord(
                validation_domain_name, "TXT", '"{}"'.format(validation)
            )
        except (ObjectNotFoundError, ApiHttpStatusError, ApiResponseError) as e:
            logger.error(
                "Encountered error deleting TXT record. [{}]: {}".format(
                    validation_domain_name, e.message
                )
            )
            raise self._getPluginErrorFromException(e)

    def _getPluginErrorFromException(self, e):

        message = "Unknown exception from Hosting.de DNS API: {}".format(e.message)
        if isinstance(e, ObjectNotFoundError):
            message = "Object could not be retrieved from Hosting.de DNS API: {}".format(
                e.message
            )
        if isinstance(e, ApiHttpStatusError):
            message = "Got an unexpected response code from the Hosting.de DNS API - [HTTP/{}] {}".format(
                e.status_code, e.message
            )
        if isinstance(e, ApiResponseError):
            message = "Hosting.de DNS API responded with error. [{}]: {}".format(
                e.errors[0]["code"], e.errors[0]["text"]
            )

        logger.error(message)
        return errors.PluginError(message, e)

    def _getApiClient(self):
        apiKey = self.credentials.conf("apikey")
        logger.debug("Using apiKey: {}".format(apiKey))
        return DnsApiClient(apiKey)
