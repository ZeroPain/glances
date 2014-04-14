# -*- coding: utf-8 -*-
#
# This file is part of Glances.
#
# Copyright (C) 2014 Nicolargo <nicolas@nicolargo.com>
#
# Glances is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Glances is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
Glances system plugin
"""

# Import system libs
import os
import platform

# Import Glances libs
from glances.plugins.glances_plugin import GlancesPlugin


class Plugin(GlancesPlugin):
    """
    Glances' Host/System Plugin

    stats is a dict
    """

    def __init__(self):
        GlancesPlugin.__init__(self)

        # We want to display the stat in the curse interface
        self.display_curse = True
        # Set the message position
        # It is NOT the curse position but the Glances column/line
        # Enter -1 to right align
        self.column_curse = 0
        # Enter -1 to diplay bottom
        self.line_curse = 0

    def update(self):
        """
        Update the host/system info
        Return the stats (dict)
        """
        self.stats = {}
        self.stats['os_name'] = platform.system()
        self.stats['hostname'] = platform.node()
        self.stats['platform'] = platform.architecture()[0]
        is_archlinux = os.path.exists(os.path.join("/", "etc", "arch-release"))
        if self.stats['os_name'] == "Linux":
            if is_archlinux:
                self.stats['linux_distro'] = "Arch Linux"
            else:
                linux_distro = platform.linux_distribution()
                self.stats['linux_distro'] = ' '.join(linux_distro[:2])
            self.stats['os_version'] = platform.release()
        elif self.stats['os_name'] == "FreeBSD":
            self.stats['os_version'] = platform.release()
        elif self.stats['os_name'] == "Darwin":
            self.stats['os_version'] = platform.mac_ver()[0]
        elif self.stats['os_name'] == "Windows":
            os_version = platform.win32_ver()
            self.stats['os_version'] = ' '.join(os_version[::2])
        else:
            self.stats['os_version'] = ""
        return self.stats

    def msg_curse(self, args=None):
        """
        Return the string to display in the curse interface
        """

        # Init the return message
        ret = []

        # Build the string message
        if (args.client):
            # Client mode
            if (args.cs_status.lower() == "connected"):
                msg = _("Connected to ")
                ret.append(self.curse_add_line(msg, 'OK'))
            elif (args.cs_status.lower() == "disconnected"):
                msg = _("Disconnected from ")
                ret.append(self.curse_add_line(msg, 'CRITICAL'))

        # Hostname is mandatory
        msg = _("{0}").format(self.stats['hostname'])
        ret.append(self.curse_add_line(msg, "TITLE"))
        # System info
        if (self.stats['os_name'] == "Linux"):
            msg = _(" ({0} {1} / {2} {3})").format(self.stats['linux_distro'],
                                                   self.stats['platform'],
                                                   self.stats['os_name'],
                                                   self.stats['os_version'])
        else:
            msg = _(" ({0} {1} {2})").format(self.stats['os_name'],
                                             self.stats['os_version'],
                                             self.stats['platform'])
        ret.append(self.curse_add_line(msg, optional=True))

        # Return the message with decoration
        return ret
