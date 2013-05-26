import json
from services import serviceList
from filters import parseFilterList
from members import parseMemberList
from hosts import parseHostList
from periods import parsePeriodList
from hostgroups import parseHostGroupList
#from layouts import *


class Config:
    def __init__(self, configFile, log):
        self.configfile = configFile
        f = open(configFile)
        self.config = f.read()
        f.close()

        self.dict = json.loads(self.config)

        self.services = serviceList(self.dict['services'])

        self.filters = parseFilterList(self.dict['filters'])

        self.members = parseMemberList(self.dict['members'], self.filters, log)

        self.periods = parsePeriodList(self.dict['periods'],log)

        self.hosts = parseHostList(self.dict['hosts'], self.services, log)

        self.hostgroups = parseHostGroupList(self.dict['hostgroups'],
                                             self.hosts,
                                             self.members,
                                             self.periods,
                                             self.services,
                                             log)

        #self.layouts = LayoutList(self.dict['layouts'], self.hostgroups)
