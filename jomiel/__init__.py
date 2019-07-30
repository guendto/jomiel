# -*- coding: utf-8 -*-
#
# jomiel
#
# Copyright
#  2019 Toni Gündoğdu
#
#
# SPDX-License-Identifier: Apache-2.0
#
"""TODO."""


def main():
    """main"""
    from jomiel.kore.path import set_proto_path
    set_proto_path(__file__, 'comm/proto/')

    from jomiel.app import App

    App(module_name=__name__,
        pkg_resources_name=__name__,
        config_module='jomiel.cache').run()


def lg():  # pylint: disable=C0103
    """Returns the logger instance used to print to the logging
    subsystem to record new events.

    The subsystem is configured via a separate logger YAML configuration
    file. The configuration supports different logger identities.

    To use this function (lg):

        from jomiel import lg
        lg().debug('foo=%s' % foo)

    Returns
        The logger instance

    """
    from jomiel.cache import opts  # pylint: disable=E0611
    import logging as lg
    return lg.getLogger(opts.logger_ident)


def log_sanitize_string(data):
    """Sanitize (conditionally) data deemed to be too "sensitive" to be
    logged as it is.

    Simply withholds the the given data from the log.

    Args:
        data (str): the data to be sanitized

    Returns:
        str: the sanitized string, or the original string if sanitation
            was not requested

    """
    from jomiel.cache import opts  # pylint: disable=E0611
    return data if opts.debug_sensitive else '<withheld>'


# vim: set ts=4 sw=4 tw=72 expandtab:
