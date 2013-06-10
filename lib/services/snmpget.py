"""
The snmpget service in pure Python.
"""

# http://pysnmp.sourceforge.net/

"""
1. install net-snmp package on localhost
2. Use this /etc/snmp/snmpd.conf:

com2sec local     127.0.0.1/32          linspector
com2sec local     192.168.2.0/24        linspector
#
group MyROGroup v1         local
group MyROGroup v2c        local
group MyROGroup usm        local
view all    included  .1                               80
access MyROGroup "" any     noauth    exact  all    none   none
#
syslocation Sylt
syscontact Admin {Admin@example.com}
3. start the snmpd service
4. the following code should work
"""

from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()

errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    cmdgen.CommunityData('linspector'),
    cmdgen.UdpTransportTarget(('localhost', 161)),

    # Names variables:
    #cmdgen.MibVariable('SNMPv2-MIB', 'sysName', 0)

    # OID's:
    cmdgen.MibVariable('.1.3.6.1.4.1.2021.10.1.3.1')  # load
    #cmdgen.MibVariable('.1.3.6.1.4.1.2021.10.1.3.2')  # load
    #cmdgen.MibVariable('.1.3.6.1.4.1.2021.10.1.3.3')  # load
    #cmdgen.MibVariable('.1.3.6.1.2.1.1.3.0')  # systems uptime
    # more:
    # http://www.debianadmin.com/linux-snmp-oids-for-cpumemory-and-disk-statistics.html
    # http://www.mibdepot.com/index.shtml
)

# Check for errors and print out results
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