class HostGroup:
    def __init__(self, name, members="", hosts="", services="", threshold="", parent="", comment=""):
        self.name = name
        self.interval = 0
        self.members = members
        self.hosts = hosts
        self.services = services
        self.threshold = threshold
        self.parent = parent
        self.comment = comment

    def __str__(self):
        ret = "HostGroup: " + self.name + " threshold: " + str(self.threshold) + " parent: " + self.parent + "\n"
        ret += "members: {\n"
        for itm in self.members:
            ret += str(itm) + "\n"
        ret += "}\n"
        ret += "hosts: {\n"
        for itm in self.hosts:
            ret += str(itm) + "\n"
        ret += "}\n"
        ret += "services: {\n"
        for itm in self.services:
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
