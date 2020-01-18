# -*- coding: utf-8 -*-
#
# jomiel-kore
#
# Copyright
#  2019-2020 Toni Gündoğdu
#
#
# SPDX-License-Identifier: Apache-2.0
#
"""TODO."""


def if_proto_bindings_missing(exception, logger=None):
    """Checks if the exception was risen due to missing the generated
    python bindings for the jomiel message declarations. Handles the
    error by printing a message.

    Args:
        exception (obj): the exception that occurred
        logger (obj): the logger instance to write the text to (or None)

    Raises:
        Re-raise the same exception, unless deemed to be the exception
        we were expecting to handle.

    """
    msg = str(exception)
    if "data.bindings" in msg:
        notice = "Did you run `python setup.py build_py`?"
        if logger:
            logger.error(msg)
            logger.error(notice)
        else:
            from sys import stderr

            print("error: %s" % msg, file=stderr)
            print("error: %s" % notice, file=stderr)
        from .app import exit_error

        exit_error()
    else:
        raise exception


# vim: set ts=4 sw=4 tw=72 expandtab:
