import json
from services import serviceList
from filters import parseFilterList
from members import parseMemberList
from hosts import parseHostList
from periods import parsePeriodList
from hostgroups import parseHostGroupList
#from layouts import *


class Config:
    def __init__(self, configFile):
        self.configfile = configFile
        f = open(configFile)
        self.config = f.read()
        f.close()

        self.dict = json.loads(self.config)

        self.services = serviceList(self.dict['services'])

        self.filters = parseFilterList(self.dict['filters'])

        self.members = parseMemberList(self.dict['members'], self.filters)

        self.periods = parsePeriodList(self.dict['periods'])

        self.hosts = parseHostList(self.dict['hosts'], self.services)

        self.hostgroups = parseHostGroupList(self.dict['hostgroups'],
                                             self.hosts,
                                             self.members,
                                             self.periods,
                                             self.services)

        #self.layouts = LayoutList(self.dict['layouts'], self.hostgroups)
