class Task:
    def __init__(self, name="", command="", priority=0, comment=""):
        self.name = name
        self.command = command
        self.priority = priority
        self.comment = comment

    def __str__(self):
        return "Task('Name: " + self.name + "', 'Command: " + self.command + "', 'Priority: " + str(self.priority) + "')"

    def clone(self):
        return Task(self.name, self.command, self.priority, self.comment)


def parseTaskList(tasks):
    return [Task(name, **values) for name, values in tasks.items()]