linspector
==========

A simple, Python based, system & network vital information monitoring solution

Please visit http://linspector.org/ for more information. Much stuff there is outdated but we have redesigned a lot.

The code is very simple and easy to understand, so take a look there if you are interested in Linspector.

Linspector currently only supports a tcpconnect probe as a service to monitor. It support reporting via SMTP and XMPP.
Not more!

For us it is great that the idea of that kind of software works perfectly using Python. Parsing the configuration file wasn't easy since Linspector objects are created dynamically from configuration. Scheduling of jobs is also done. We need to fix some bugs but when this is done we will start adding features to make Linspector usable in the wild.

Linspector is licensed under the terms of the AGPL license.