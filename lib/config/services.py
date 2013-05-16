class Service:
    def __init__(self, name="", command="", comment="", parser=""):
        self.name = name
        self.command = command
        self.comment = comment
        self.parser = parser

    def __str__(self):
        return "Service('Name: " + self.name + "', 'Command: " + self.command + ", 'Parser: " + self.parser + "')"

    def clone(self):
        return Service(self.name, self.command, self.comment)


def serviceList(services):
    return [Service(name=key, **values) for key, values in services.items()]
