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


def get_semantic_version():
    """Returns the version in semantic format.

    Returns the value of USE_SEMANTIC_VERSION environment if it's
    defined.

    If environment VERSION_TIME is set, appends %H%M (hour, minute) at
    the end of the string. Useful, if you need to release the same
    package the same day, since this function would simply use
    YEAR.MONTH.DAY for a semantic version string.

    Ignores VERSION_TIME if USE_SEMANTIC_VERSION was defined.

    """
    from os import environ as env

    if "USE_SEMANTIC_VERSION" in env:
        return env["USE_SEMANTIC_VERSION"]

    from datetime import datetime

    now = datetime.now()
    fmt = "%-y.%-m.%-d"

    if "VERSION_TIME" in env:
        fmt = fmt + ".%-H%-M"

    s = now.strftime(fmt)
    return s[:1] + "." + s[1:]


def save_version_file():
    """Creates the VERSION file with 'semantic' and 'packaged' info."""
    from os.path import isdir

    semantic = get_semantic_version()

    if isdir(".git"):
        from ..version import git_version

        packaged = git_version(shortened=True)
    else:
        packaged = "(unknown)"

    from .cache import DATA_VERSION_FILE
    from os.path import sep

    fname = DATA_VERSION_FILE.replace(".", sep)

    with open(fname, "w") as handle:
        for line in [semantic, packaged]:
            handle.write(line + "\n")


# vim: set ts=4 sw=4 tw=72 expandtab:
