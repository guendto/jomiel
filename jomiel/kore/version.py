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

from os import EX_OK

from .app import subprocess_open

try:  # py38+
    from importlib.metadata import version as metadata_version
    from importlib.metadata import PackageNotFoundError
except ModuleNotFoundError:
    from importlib_metadata import version as metadata_version
    from importlib_metadata import PackageNotFoundError


def try_version(package_data_path):
    """Try to determine application version from different sources.

    Used for --version and alike output. setup.py gets its 'version'
    filled in another way.

    If .git subdir is present
        - Try to run git-show and use its return value
    If above two fail
        - Use pkg_resources for accessing packaged VERSION file
    If all three fail
        - Try to read the PACKAGE_DATA_PATH/VERSION file
    If everything falls apart
        - Submit to defeat, and return '(unknown)'

    Args:
        package_data_path (str): the package data path

    Returns:
        str: the version string

    """
    from os.path import isdir

    rval = unknown = "(unknown)"

    if isdir(".git"):
        try:
            rval = git_version()
        except OSError:
            pass

    def read_version_file(fpath):
        """read_version_file

        Args:
            fpath (str): the file to read

        Returns:
            list: the read lines from the file (or None if failed)

        """
        with open(fpath, "r") as handle:
            return handle.readlines()
        return None

    if unknown in rval and package_data_path:
        try:  # py37+
            from importlib.resources import path as resources_path
        except ImportError:
            from importlib_resources import path as resources_path
        fname = "VERSION"
        try:
            with resources_path(package_data_path, fname) as path:
                version_file = str(path)
        except FileNotFoundError:
            from os.path import join, sep

            version_file = join(
                package_data_path.replace(".", sep), fname
            )
        try:
            rval = read_version_file(version_file)
        except FileNotFoundError:
            pass
    return rval


def git_version(shortened=False):
    """Return a version string constructed from the details returned byt
    `git-show` and `git-describe`.

    Args:
        shortened (bool): If True, omits the "[%h]" and "(%cr)" from the
            resulting string

    Returns:
        str: the constructed version string

    """
    return "git-{}, {}".format(
        git_describe_version(), git_show_version(shortened),
    )


def run_command(args):
    """Run a command and return the output.

    Args:
        args (list): of args to be passed to Popen

    Returns:
        str: the git command output

    """
    (rval, data) = subprocess_open(args)
    return data if rval == EX_OK else ""


def git_describe_version():
    """Return the `git describe` output which i sused for the version
    string."""
    args = [
        "git",
        "describe",
        "--match=v[0-9]*",
        "--abbrev=6",
        "--tags",
        "--always",
        "HEAD",
    ]
    return run_command(args).replace("v", "")


def git_show_version(shortened=False):
    """Return the `git show` output which is used for the version
    string.

    Args:
        shortened (bool): If True, omits the "[%h]" and "(%cr)" from the
            resulting string

    Returns:
        str: the version string

    """
    fmt = "--format=%cI"

    if not shortened:
        fmt += " (%cr)"

    return run_command(["git", "show", "-s", fmt, "--abbrev=6", "HEAD"])


def package_version(package_name, destination):
    """Returns the package version string

    Args:
        package_name (str): the package name to look up
        destination (list): the list to store the result (tuple) to

    """
    try:
        version = metadata_version(package_name)
    except PackageNotFoundError:
        version = "<unavailable>"

    if package_name == "pyzmq":
        from zmq import zmq_version

        version = "{} (libzmq version {})".format(
            version, zmq_version()
        )

    destination.append((package_name, version))


# vim: set ts=4 sw=4 tw=72 expandtab:
