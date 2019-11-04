# -*- coding: utf-8 -*-
#
# jomiel
#
# Copyright
#  2019 Toni Gündoğdu
#
#
# SPDX-License-Identifier: Apache-2.0
#
"""TODO."""


def main():
    """main"""
    from sys import path

    path.insert(0, ".")

    from jomiel.keygen.app import App

    App(
        no_default_config_files=True,
        pkg_resources_name="jomiel",  # shares the pkg_resources
        no_config_file_option=True,
        no_logger_options=True,
        no_print_config=True,
    ).run()


# vim: set ts=4 sw=4 tw=72 expandtab:
