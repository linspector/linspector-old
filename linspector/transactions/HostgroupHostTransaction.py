from linspector.transactions import HostgroupTransaction
from linspector.core.job import LinspectorJob

__author__ = 'rafael'

def handle_job(job):
    job.handle_call()


class HostgroupHostTransaction(HostgroupTransaction):
    def __init__(self, linspectorInterface,  hostgroup, host):
        super(HostgroupHostTransaction).__init__(linspectorInterface, hostgroup)
        self.host = host

class HostgroupAddHostTransaction(HostgroupHostTransaction):
    def __init__(self, linspectorInterface, hostgroup, host):
        super(HostgroupHostTransaction).__init__(linspectorInterface, hostgroup, host)



    def transact(self):
        hostgroup = self.interface.get_config().get_hostgroup_by_name(self.hostgroup)
        if hostgroup is not None:
            hostgroup.add_host(self.host)
            for service in hostgroup.get_services():
                for host in hostgroup.get_hosts():
                    for period in service.get_periods():

                        job = LinspectorJob(service,
                                            host,
                                            hostgroup.get_members(),
                                            None,
                                            hostgroup)
                        scheduler_job = period.createJob(self.scheduler, job, handle_job)
                        if scheduler_job is not None:
                            scheduler_job.misfire_grace_time = 2
                            job.set_job(scheduler_job)
                            self.interface.add_job(job)


        else:
            raise Exception("could not find hostgroup %s" % self.hostgroup )


