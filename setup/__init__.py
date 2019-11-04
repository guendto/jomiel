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


def init(pkg_name, proto_path):
    """Initializes the setup package for use with setup.py

    Args:
        pkg_name (str): the package name
        proto_path (str): the path (under pkg_name) to the proto files

    """
    from ..setup import cache  # See that? Get it?
    from os.path import join

    cache.PROTO_PATH = join(pkg_name, proto_path)
    cache.PROTO_FILES = ["Message.proto", "Status.proto", "Media.proto"]
    cache.PROTO_FILES = [
        join(cache.PROTO_PATH, fname) for fname in cache.PROTO_FILES
    ]

    cache.PROTO_INIT = join(cache.PROTO_PATH, "__init__.py")
    cache.VERSION_FILE = join(pkg_name, "VERSION")
    cache.PKG_NAME = pkg_name


# vim: set ts=4 sw=4 tw=72 expandtab:
