"""
The snmpget service in pure Python.
"""

from pysnmp.entity.rfc3413.oneliner import cmdgen
from service import Service


class SnmpgetService(Service):
    def __init__(self, parser, log, **kwargs):
        super(Service, self).__init__(parser)
        if "community" in kwargs:
            self.community = kwargs["community"]
        else:
            log.w("There is no community")
            raise
        if "oid" in kwargs:
            self.oid = kwargs["oid"]
        else:
            log.w("There is no oid")
            raise
        if "port" in kwargs:
            self.port = kwargs["port"]
        else:
            self.port = "161"

    def execute(self):
        cmdGen = cmdgen.CommandGenerator()

        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
            cmdgen.CommunityData(self.community),
            cmdgen.UdpTransportTarget((self.host, self.port)),
            cmdgen.MibVariable(self.oid)
        )

        if errorIndication:
            print(errorIndication)
        else:
            if errorStatus:
                print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex) - 1] or '?'
                ))
            else:
                for name, val in varBinds:
                    print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))