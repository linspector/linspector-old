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
    def __init__(self, service, periods):
        self.service = service
        self.periods = periods

    def __str__(self):
        return "HostgroupService { " + str(self.service) + ", " + str(self.periods) + "}"


def parseHostGroupList(hostgroups, hosts, members, periods, services, log):
    parsedHostGroups = []
    for hgname, hgValues in hostgroups.items():
        hostGroup = HostGroup(hgname)
        hostGroup.members = filter(lambda m: m.nameid in hgValues['members'], members)
        hostGroup.hosts = filter(lambda h: h.name in hgValues['hosts'], hosts)
        hostGroup.threshold = hgValues['threshold']
        if 'parent' in hgValues:
            hostGroup.parent = hgValues['parent']
        hostGroup.services = []
        for serviceName, servicePeriods in hgValues['services'].items():
            service = filter(lambda s: s.name in serviceName, services)
            if len(service) == 0:
                log.w("Service " + serviceName + " is not defined for Hostgroup " + hgname)
                continue
            service = service[0]
            hostGroupPeriods = filter(lambda p: p.name in servicePeriods, periods)
            hostGroup.services.append(HostGroupService(service, hostGroupPeriods))
        parsedHostGroups.append(hostGroup)
    return parsedHostGroups
