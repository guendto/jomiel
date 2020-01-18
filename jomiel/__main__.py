# -*- coding: utf-8 -*-
#
# jomiel
#
# Copyright
#  2019-2020 Toni Gündoğdu
#
#
# SPDX-License-Identifier: Apache-2.0
#
"""TODO."""


def main():
    """main"""
    from sys import path

    path.append(".")

    from jomiel.app import App

    pkg_name = "jomiel"
    data_dir = "%s.data" % pkg_name

    App(
        package_name=pkg_name,
        package_data_dir=data_dir,
        package_additional_search_paths=["%s.bindings" % data_dir],
        config_module="%s.cache" % pkg_name,
    ).run()


if __name__ == "__main__":
    try:
        main()
    except ModuleNotFoundError as error:
        from jomiel.kore.error import if_proto_bindings_missing

        if_proto_bindings_missing(error)

# vim: set ts=4 sw=4 tw=72 expandtab:
