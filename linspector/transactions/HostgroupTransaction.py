from cherrypy.test.test_session import host
from linspector.transactions import BaseTransaction

__author__ = 'rafael'

class HostgroupTransaction(BaseTransaction):
    def __init__(self, linspectorInterface, hostgroup):
        super(HostgroupTransaction, self).__init__(linspectorInterface)
        self.hostgroup = hostgroup