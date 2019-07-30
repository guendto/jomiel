# -*- coding: utf-8 -*-
#
# jomiel-kore
#
# Copyright
#  2019 Toni Gündoğdu
#
#
# SPDX-License-Identifier: Apache-2.0
#
"""TODO."""


def if_proto_bindings_missing(exception, logger):
    """Checks if the exception was risen due to missing the generated
    python bindings for the jomiel message declarations. Handles the
    error by printing a message.

    Args:
        exception (obj): the exception that occurred
        logger (obj): the logger instance to write the text to

    Raises:
        Re-raise the same exception, unless deemed to be the exception
        we were expecting to handle.

    """
    msg = str(exception)
    if 'proto.Message_pb2' in msg:
        logger.error(msg)
        logger.error('Did you run `python setup.py build_py`?')
        from .app import exit_error
        exit_error()
    else:
        raise exception


# vim: set ts=4 sw=4 tw=72 expandtab:
