from linspector.transactions import BaseTransaction


class HostgroupTransaction(BaseTransaction):
    def __init__(self, linspectorInterface, hostgroup):
        super(HostgroupTransaction, self).__init__(linspectorInterface)
        self.hostgroup = hostgroup