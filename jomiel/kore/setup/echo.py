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

from distutils.debug import DEBUG  # pylint: disable=E0611,E0401
from sys import stdout


def put(msg):
    """Print a message to the stdout.

    Args:
        msg (str): the message to print

    """
    if DEBUG:
        stdout.write(msg)


# vim: set ts=4 sw=4 tw=72 expandtab:
