"""
The LinspectorConfig class.

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


class LinspectorConfig(object):
    def __init__(self):
        self._layouts = None
        self._hostgroups = None
        self._members = None
        self._periods = None

    def set_hostgroups(self, hostgroups):
        self._hostgroups = hostgroups

    def get_hostgroups(self):
        return self._hostgroups

    def set_layouts(self, layouts):
        self._layouts = layouts

    def get_layouts(self):
        return self._layouts

    def set_members(self, members):
        self._members = members

    def get_members(self):
        return self._members

    def set_periods(self, periods):
        self._periods = periods

    def get_periods(self):
        return self._periods

    def get_enabled_layouts(self):
        return [l for l in self.get_layouts() if l.is_enabled()]

    def _get_by_name(self, items, name):
        for itm in items:
            if itm.get_name() == name:
                return itm
        return None

    def get_hostgroup_by_name(self, name):
        return self._get_by_name(self.get_hostgroups(), name)

    def get_layout_by_name(self, name):
        return self._get_by_name(self.get_layouts(), name)

    def get_member_by_name(self, name):
        return self._get_by_name(self.get_members(), name)

    def get_period_by_name(self, name):
        return self._get_by_name(self.get_periods(), name)