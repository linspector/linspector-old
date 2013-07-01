import re


class Member:
    def __init__(self, id, name="",  comment="", tasks=None):
        self.id = id
        self.name = name
        self.tasks = []
        self.add_task(tasks)
        self.comment = comment

    def get_id(self):
        return self.id

    def add_task(self, task):
        if task is None:
            return
        if isinstance(task, list):
            self.tasks.extend(task)
        else:
            self.tasks.append(task)
    
    def get_tasks(self):
        return self.tasks

    def __str__(self):
        ret = "Member Id: " + self.nameid + " Name: " + self.name + " Filters: " + str(self.phone)
        for f in self.filters:
            ret += str(f)
        return ret


class MemberFilter:
    def __init__(self, filter, Value):
        self.filter = filter
        self.value = Value

    def __str__(self):
        return "Filter:" + str(self.filter) + " Value:" + self.value


def parseMemberList(members, filters, log):
    parsedMembers = [Member(nameid, **values) for nameid, values in members.items()]
    for member in parsedMembers:
        mFilter = []
        for filtername, replacement in member.filters.items():
            found = False
            for filt in filters:
                if filt.name != filtername:
                    continue
                found = True
                memberFilter = filt.clone()
                memberFilter.command = re.sub('@member', replacement, filt.command)
                mFilter.append(memberFilter)
            if not found:
                log.w("filter: " + filtername + " is not defined in member " + member.name)
        member.filters = mFilter
    return parsedMembers