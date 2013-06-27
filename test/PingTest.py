__author__ = 'rafael'


from lib.services.ping import PingService
from lib.config.hostgroups import HostGroup
from lib.config.members import Member

member = Member()
ps = PingService(fails={"warn": 100})
hg = HostGroup("pingGroup", members=[])
