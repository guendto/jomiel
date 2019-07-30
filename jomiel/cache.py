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


def dump_plugins():
    """Dumps plugin details to the stdout."""
    for namespace in plugin_handlers:  # pylint: disable=E0602
        print(namespace + ':')
        for handler in plugin_handlers[namespace]:  # pylint: disable=E0602
            print('- %s' % handler.name)
    from jomiel.kore.app import exit_normal
    exit_normal()


# vim: set ts=4 sw=4 tw=72 expandtab:
