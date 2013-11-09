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


class HostGroupException(Exception):
    def __init__(self, msg):
        self.msg = msg
        
    def __str__(self):
        return repr(self.msg)


class HostGroupMissingArgumentException(HostGroupException):
    def __init__(self, missingArgument, hostgroupName):
        super(HostGroupMissingArgumentException, self).__init__("no " + missingArgument + " defined for Hostgroup " + hostgroupName)


class HostGroup(object):
    def __init__(self, _name, **kwargs):
        self.name = _name
        tmp = "members"
        self.members = []
        if not tmp in kwargs:
            raise HostGroupMissingArgumentException(tmp, _name)
        self.add_members(kwargs[tmp])
        
        tmp = "hosts"
        self.hosts = []
        if not tmp in kwargs:
            raise HostGroupMissingArgumentException(tmp, _name)
        self.add_hosts(kwargs[tmp])
        
        tmp = "services"
        self.__services = []
        if not tmp in kwargs:
            raise HostGroupMissingArgumentException(tmp, _name)
        self.add_services(kwargs[tmp])
        
        self.parents = []
        tmp = "parents"
        if tmp in kwargs:
            self.add_parents(kwargs[tmp])

    def __str__(self):
        return self.name

    def _to_config_dict(self, configDict):
        me = {}
        me["members"] = [member.nameid for member in self.get_members()]
        me["hosts"] = self.hosts
        me["parents"] = [hg.get_name() for hg in self.get_parents()]
        #TODO implement delegation
        #me["services"] = [service._to_config_dict(configDict) for service in self.get_services()]
        #me["processors"] = [processor._to_config_dict(configDict) for processor in self.get_processors()]
        configDict["hostgroups"][self.get_name()] = me

    def __add_internal(self, l, item):
        if isinstance(item, list):
            l.extend(item)
        else:
            l.append(item)

    def add_members(self, member):
        self.__add_internal(self.get_members(), member)
            
    def add_hosts(self, host):
        self.__add_internal(self.get_hosts(), host)
         
    def add_parents(self, parent):
        self.__add_internal(self.get_parents(), parent)

    def add_services(self, services):
        self.__add_internal(self.get_services(), services)
    
    def get_parents(self):
        return self.parents
    
    def get_services(self):
        return self.__services

    def get_hosts(self):
        return self.hosts
    
    def get_name(self):
        return self.name
    
    def get_members(self):
        return self.members