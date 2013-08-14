"""
The Linspector Interactive Shell...

This  will become an interface to Linspector at "start" time. Think about MidnightCommander... and then run
Linspector in a screen session and not as daemon, why not? BTW.: Daemonization is at this point of development
cancelled, because it makes no sense to daemonize everything. Linspector is a user software which will run in any
screen session perfectly.
"""

from lib.frontends.frontend import Frontend


class LishFrontend(Frontend):
    def __init__(self, **kwargs):
        return