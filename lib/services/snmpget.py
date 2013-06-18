"""
The snmpget service in pure Python.
"""

#from pysnmp.entity.rfc3413.oneliner import cmdgen
from service import Service


class SnmpgetService(Service):
    def __init__(self, **kwargs):
        super(SnmpgetService, self).__init__(**kwargs)
        
        args = self.get_arguments()
        
        if "community" in args:
            self.community = args["community"]
        else:
            raise Exception("There is no community")
        
        if "oid" in args:
            self.oid = args["oid"]
        else:
            raise Exception("There is no oid")
        
        self.port = "161"
        if "port" in args:
            self.port = args["port"]
            
    def needs_arguments(self):
        return True

    def execute(self):
        pass
        #cmdGen = cmdgen.CommandGenerator()

        #errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        #    cmdgen.CommunityData(self.community),
        #    cmdgen.UdpTransportTarget((self._host, self.port)),
        #    cmdgen.MibVariable(self.oid)
        #)
        
        #if errorIndication:
        #    print(errorIndication)
        #else:
        #    if errorStatus:
        #        print('%s at %s' % (
        #            errorStatus.prettyPrint(),
        #            errorIndex and varBinds[int(errorIndex) - 1] or '?'
        #        ))
        #    else:
        #        for name, val in varBinds:
        #            print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))


def create(kargs):
    return SnmpgetService(**kwargs)