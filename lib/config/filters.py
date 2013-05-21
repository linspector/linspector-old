class Filter:
    def __init__(self, name="", command="", priority=0, comment=""):
        self.name = name
        self.command = command
        self.priority = priority
        self.comment = comment

    def __str__(self):
        return "Filter('Name: " + self.name + "', 'Command: " + self.command + "', 'Priority: " + str(
            self.priority) + "')"

    def clone(self):
        return Filter(self.name, self.command, self.priority, self.comment)


def parseFilterList(filters):
    return [Filter(name, **values) for name, values in filters.items()]
