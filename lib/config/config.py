import json
from tasks import parseTaskList
from members import parseMemberList
from periods import parsePeriodList
#from hostgroups import parseHostGroupList
#from layouts import parseLayoutList


class Config:
    def __init__(self, configFile, log):
        self.configfile = configFile
        f = open(configFile)
        self.config = f.read()
        f.close()

        self.dict = json.loads(self.config)

        self.tasks = parseTaskList(self.dict['tasks'])
        self.members = parseMemberList(self.dict['members'], self.tasks, log)
        self.periods = parsePeriodList(self.dict['periods'], log)
        #self.hostgroups = parseHostGroupList(self.dict['hostgroups'],
        #                                     self.members,
        #                                     self.periods,
        #                                     log)

        #self.layouts = LayoutList(self.dict['layouts'], self.hostgroups)