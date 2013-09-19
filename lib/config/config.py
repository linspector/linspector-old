"""
The LinspectorConfig class.
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