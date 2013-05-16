"""
This is what job_function needs as parameter for each job to succesfully 
execute.
"""


class Job:
    def __init__(self, command=None, members=None, host=None, service=None):
        self.command = command
        self.members = members
        self.host = host
        self.service = service
