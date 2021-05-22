#
# jomiel
#
# Copyright
#  2019-2021 Toni Gündoğdu
#
#
# SPDX-License-Identifier: Apache-2.0
#
"""TODO."""
from jomiel.cache import opts
from jomiel.log import lg
from jomiel.log import log_sanitize_string
from requests import get


def be_verbose():
    """Make httplib and requests verbose."""

    def verbose_httplib():
        """Enable verbose output in httplib."""
        from http.client import HTTPConnection

        HTTPConnection.debuglevel = 1

    def verbose_logging():
        """Enable verbose output in logging standard library."""
        from logging import getLogger, DEBUG, basicConfig

        basicConfig()
        getLogger().setLevel(DEBUG)

        logger = getLogger("requests.packages.urllib3")
        logger.propagate = True
        logger.setLevel(DEBUG)

    verbose_httplib()
    verbose_logging()


def http_headers(headers=None):
    """Construct common HTTP headers from the jomiel options.

    Args:
        headers (dict): additional headers to use

    Returns:
        A headers dictionary ready to be used with `requests`

    """
    result = {"user-agent": opts.http_user_agent}
    if headers:
        result.update(headers)
    return result


def http_get(uri, **kwargs):
    """Make a new HTTP/GET request.

    Args:
        uri (string): URI to retrieve

    Returns:
        obj: requests.Response

    """
    headers = http_headers(**kwargs)

    lg().debug("http<get>: '%s'", log_sanitize_string(uri))
    lg().debug("http<get/headers>: '%s'", log_sanitize_string(headers))

    result = get(
        uri,
        allow_redirects=opts.http_allow_redirects,
        timeout=opts.http_timeout,
        headers=headers,
    )

    result.raise_for_status()
    return result


# vim: set ts=4 sw=4 tw=72 expandtab:
