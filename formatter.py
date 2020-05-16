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
from json import dumps


def json_get_pprint(json_object, indent=2):
    """Return the pretty string of the given json object.

    Args:
        json_object: the json object to use
        indent: the used indentation

    Notes:
        - https://stackoverflow.com/a/16319664, kudos

    Returns:
        the prettified json string

    """
    return dumps(
        json_object,
        sort_keys=True,
        indent=indent,
        separators=(",", ": "),
    )


def json_pprint(json_object):
    """Pretty print the given json object to the stdout.

    Args:
        json_object: the json object to use

    Returns:
    """
    json_str = json_get_pprint(json_object)
    print(json_str)


# vim: set ts=4 sw=4 tw=72 expandtab:
