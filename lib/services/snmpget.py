"""
The snmpget service in pure Python.

Copyright (c) 2011-2013 "Johannes Findeisen and Rafael Timmerberg"

This file is part of Linspector (http://linspector.org).

Linspector is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

#from pysnmp.entity.rfc3413.oneliner import cmdgen
from lib.services.service import Service


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


def create(kwargs):
    return SnmpgetService(**kwargs)