"""
The Linspector XMPP Frontend...

Just for the fun in it... Linspector connects to a XMPP Server and are accepting commands from special users and can
give back information. The Linspector admin client will then be any Jabber Client... ;)
"""

from lib.frontends.frontend import Frontend


class XmmpFrontend(Frontend):
    def __init__(self, **kwargs):
        pass