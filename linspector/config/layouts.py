"""
Copyright (c) 2011-2013 "Johannes Findeisen and Rafael Timmerberg"

This file is part of Linspector (http://linspector.org).

Linspector is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

from logging import getLogger

logger = getLogger(__name__)


class LayoutException(Exception):
    def __init__(self, msg):
        self.msg = msg
        
    def __str__(self):
        return repr(self.msg)


class Layout(object):
    def __init__(self, name, enabled=False, hostgroups=None):
        self._name = name
        self._enabled = enabled

        if hostgroups is None or len(hostgroups) <= 0:
            raise LayoutException("Layout: " + self._name + " without hostgroups is useless")
        else:
            self._hostgroups = hostgroups

    def _to_config_dict(self, configDict):
        me = {}
        me["hostgroups"] = [hg.name for hg in self.get_hostgroups()]
        me["enabled"] = self.is_enabled()
        configDict["layouts"][self.get_name()] = me
        for hostgroup in self.get_hostgroups():
            hostgroup._to_config_dict(configDict)

    def get_name(self):
        return self._name
    
    def is_enabled(self):
        return self._enabled

    def get_hostgroups(self):
        return self._hostgroups

    def __str__(self):
        ret = "Layout: 'Name:" + str(self.name) + "', 'Enabled: " + str(self.enabled) + " "
        for group in self.hostgroups:
            ret += str(group)
        return ret


class LayoutList:
    def __init__(self, layouts, hostgroups):
        self.layouts = []
        self.dict = layouts
        self.plugins = []
        for k, v in layouts.items():
            if k in ("plugins", "Plugins"):
                self.plugins = v
                continue
            else:
                l = Layout(k)
                for k1, v1 in v.items():
                    if k1 in ("enabled", "Enabled"):
                        l.enabled = v1
                    elif k1 in ("hostgroups", "Hostgroups"):
                        l.hostgroups = []
                        for group in v1:
                            h = None
                            for hostg in hostgroups:
                                if hostg.name == group:
                                    h = hostg
                                    break
                            if h is not None:
                                l.hostgroups.append(h)
                            else:
                                pass
                self.layouts.append(l)

    def __str__(self):
        ret = ""
        ret += "Plugins: " + str(self.plugins) + "\n"
        for layout in self.layouts:
            ret += str(layout) + "\n"
        return ret