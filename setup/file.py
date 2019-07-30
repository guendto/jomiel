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


def touch_file(fpath):
    """Creates/updates the specified file

    Args:
        fpath (str): the path to the file

    """
    from .echo import put
    put('Touching %s...' % fpath)

    with open(fpath, 'a'):
        from os import utime
        utime(fpath, None)

    put(' done.\n')


def read_file(fpath):
    """Return the contents of a file.

    Args:
        fpath (str): the file name

    """
    with open(fpath, 'r') as handle:
        return handle.read()


# vim: set ts=4 sw=4 tw=72 expandtab:
