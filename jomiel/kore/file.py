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

from os.path import join


def find_matching_files_py35(find_filename, location):
    """Find all matching files (recursively) from the current working
    directory (default), or from the location specified.

    Args:
        find_filename (str): file name to look for (can be a mask)
        location (str): the location to search for matching files

    Returns:
        list: of matching files

    Note:
        - This is the Python 3.5+

    """
    from glob import iglob
    _filter = join(location, '**', find_filename)
    result = []
    for filename in iglob(_filter, recursive=True):
        result.append(filename)
    return result


def find_matching_files_py27(find_filename, location):
    """Find all matching files (recursively) from the current working
    directory (default), or from the location specified.

    Args:
        find_filename (str): file name to look for (can be a mask)
        location (str): the location to search for matching files

    Returns:
        list: of matching files

    Note:
        - This is the Python 2.7

    """
    from fnmatch import filter as _filter
    from os import walk
    result = []
    for root, _, filenames in walk(location):
        for filename in _filter(filenames, find_filename):
            result.append(join(root, filename))
    return result


def find_matching_files(find_filename, location=None):
    """find_matchin_files

    Args:
        find_filename (str): file name to look for (can be a mask)

    Returns:
        list: of matching files

    """
    from sys import version_info
    if version_info >= (3, 5):
        func = find_matching_files_py35
    else:
        func = find_matching_files_py27

    def cwd():
        """Wraps os.getcwd."""
        from os import getcwd
        return getcwd()

    location = location if location else cwd()
    return func(find_filename, location)


def put(msg):
    """Put a message to the stdout.

    Args:
        msg (str): the message to write

    """
    from sys import stdout
    stdout.write(msg)


def unlink_if(fpath, verbose=True):
    """Remove the specified file conditionally (exists).

    Args:
        fpath (str): the path to the file
        verbose (bool): If set to false, pipes down the chatter

    """
    from os.path import exists
    from os import unlink
    if exists(fpath):
        if verbose:
            put('Removing file %s\n' % fpath)
        unlink(fpath)


# vim: set ts=4 sw=4 tw=72 expandtab:
