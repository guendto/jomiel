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


def init(**kwargs):
    """Initializes the cache values for use with setup.py and the custom
    commands.

    Args:
        **kwargs: arbitrary keyword args

    Supported arbitrary keyword args (kwargs):

        name (str): the package name

        data_dir (str): the package data dir

        bootstrap_path (str): the path to the `bootstrap` script of
            jomiel-proto

        proto_root_dir (str): the root dir containing the .proto files

        bindings_dir (str): the destination dir for the compiled bindings

    """
    from ..setup import cache

    cache.NAME = kwargs.get("name", None)

    cache.BOOTSTRAP_PATH = kwargs.get("bootstrap_path", None)
    cache.PROTO_ROOT_DIR = kwargs.get("proto_root_dir", None)

    cache.DATA_DIR = kwargs.get("data_dir", None)

    cache.DATA_VERSION_FILE = "{}.{}.{}".format(
        cache.NAME, cache.DATA_DIR, "VERSION",
    )

    cache.DATA_BINDINGS_DIR = "{}.{}.{}".format(
        cache.NAME, cache.DATA_DIR, kwargs.get("bindings_dir", None),
    )


# vim: set ts=4 sw=4 tw=72 expandtab:
