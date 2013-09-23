linspector
==========

A simple, Python based, system & network vital information monitoring solution.

Please visit http://linspector.org/ for more information. Much stuff there is outdated but we have redesigned a lot.

The code is very simple and easy to understand, so take a look there if you are interested in Linspector.

Linspector currently only supports a "tcpconnect" probe on ports as a service to monitor. It supports reporting via SMTP and XMPP. Not more!

For us it is great that the idea of that kind of software works perfectly using Python.

Parsing the configuration file wasn't easy since Linspector objects are being created dynamically from configuration. It works!

Scheduling of jobs is also done. It works!

We need to fix some bugs but when this is done we will start adding features to make Linspector usable in the wild.

Next step will be business logic to manage an admins everyday monitoring tasks. SNMP will be added when the "tcpconnect" service works perfectly; Then some more services will be added too. We need the framework running first and then we will go on... ;)

Linspector is licensed under the terms of the AGPL license.