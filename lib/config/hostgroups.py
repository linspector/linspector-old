class HostGroupException(Exception):
    def __init__(self, msg):
        self.msg = msg
        
    def __str__(self):
        return repr(self.msg)


class HostGroupMissingArgumentException(HostGroupException):
    def __init__(self, missingArgument, hostgroupName):
        super(HostGroupMissingArgumentException, self).__init__("no " + missingArgument + " defined for Hostgroup " + hostgroupName)


class HostGroup(object):
    def __init__(self, name, **kwargs):
        self.name = name
        tmp = "members"
        self.members = []
        if not tmp in kwargs:
            raise HostGroupMissingArgumentException(tmp, name)
        self.add_members(kwargs[tmp])
        
        tmp = "hosts"
        self.hosts = []
        if not tmp in kwargs:
            raise HostGroupMissingArgumentException(tmp, name)
        self.add_hosts(kwargs[tmp])
        
        tmp = "services"
        self.__services = []
        if not tmp in kwargs:
            raise HostGroupMissingArgumentException(tmp, name)
        self.add_services(kwargs[tmp])
        
        self.parents = []
        tmp = "parents"
        if tmp in kwargs:
            self.add_parents(kwargs[tmp])
        
        tmp = "processors"
        self.processors = []
        if tmp in kwargs:
            self.add_processors(kwargs[tmp])
        
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
    
    def add_processors(self, processor):
        self.__add_internal(self.get_processors(), processor)
         
    def add_parents(self, parent):
        self.__add_internal(self.get_parents(), parent)

    def add_services(self, services):
        self.__add_internal(self.get_services(), services)
    
    def get_parents(self):
        return self.parents
         
    def get_processors(self):
        return self.processors
    
    def get_services(self):
        return self.__services
    
    def get_hosts(self):
        return self.hosts
    
    def get_name(self):
        return self.name
    
    def get_members(self):
        return self.members 

    def __str__(self):
        if True:
            return str(self.__dict__)
        ret = "HostGroup: " + self.name + "\n"
        ret += "members: {\n"
        for itm in self.members:
            ret += str(itm) + "\n"
        ret += "}\n"
        ret += "hosts: {\n"
        for itm in self.hosts:
            ret += str(itm) + "\n"
        ret += "}\n"
        ret += "services: {\n"
        for itm in self._services:
            ret += str(itm) + "\n"
        ret += "}\n"
        return ret


class HostGroupService:
    def __init__(self, services, periods):
        self.services = services
        self.periods = periods

    def __str__(self):
        return "HostgroupService { " + str([str(s) for s in self.services]) + ", " + str([p.name for p in self.periods]) + "}"


def parseHostGroupList(hostgroups, hosts, members, periods, services, log):
    parsedHostGroups = []
    for hgname, hgValues in hostgroups.items():
        hostGroup = HostGroup(hgname)
        hostGroup.members = [m for m in members if m.nameid in hgValues['members']]
        hostGroup.hosts = [h for h in hosts if h.name in hgValues['hosts']]
        hostGroup.threshold = hgValues['threshold']
        if 'parent' in hgValues:
            hostGroup.parent = hgValues['parent']
        hostGroup.services = []
        for serviceName, servicePeriods in hgValues['services'].items():
            services = []
            for host in hosts:
                service = host.getHostServiceByName(serviceName)
                if service is not None: 
                    services.append(service)
                else:
                    log.w("could not find HostService(" + str(serviceName) + ") for host " + host.name)
            hostGroupPeriods = [p for p in periods if p.name in servicePeriods]
            hostGroup.services.append(HostGroupService(services, hostGroupPeriods))
        parsedHostGroups.append(hostGroup)
    return parsedHostGroups