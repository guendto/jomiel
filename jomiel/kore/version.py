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

from importlib import import_module
from os import EX_OK

from .app import exit_error, subprocess_open


def try_version(pkg_resources_name):
    """Try to determine application version from different sources.

    Used for --version and alike output. setup.py gets its 'version'
    filled in another way.

    If .git subdir is present
        - Try to run git-show and use its return value
    If above two fail
        - Use pkg_resources for accessing packaged VERSION file
    If all three fail
        - Try to read the ./VERSION file
    If everything falls apart
        - Submit to defeat, and return '(unknown)'

    Args:
        pkg_resources_name (str): the module name to use with
            pkg_resources package (this is usually the __name__ of the
            app).

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

    if unknown in rval and pkg_resources_name:
        from pkg_resources import resource_filename

        try:
            version_file = resource_filename(
                pkg_resources_name, "VERSION"
            )
        except FileNotFoundError:
            from os.path import join

            version_file = join(pkg_resources_name, "VERSION")
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


def format_module_version(module_name, module_name_alt, destination):
    """Formats the module version string

    Args:
        module_name (str): the module name to look up
        module_name_alt (str): the alternative name for the module
        destination (list): the list to store the result (tuple) to

    """

    def try_module():
        """Tries to import a module."""
        try:
            module = import_module(module_name)
        except ImportError as msg:
            print("error: %s" % msg)
            exit_error()
        return module

    module = try_module()

    version = (
        module.__version__
        if hasattr(module, "__version__")
        else "(unknown)"
    )

    if module_name == "zmq":
        from zmq import zmq_version

        version = "{} (libzmq version {})".format(
            version, zmq_version()
        )

    destination.append((module_name_alt, version))


# vim: set ts=4 sw=4 tw=72 expandtab:
