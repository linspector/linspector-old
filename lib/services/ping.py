"""
The ping service in pure Python.
"""

# http://code.activestate.com/recipes/409689-icmplib-library-for-creating-and-reading-icmp-pack/
from service import Service


class PingService(Service):
    def __init__(self, **kwargs):
        super(PingService, self).__init__(**kwargs)


def create(self, **kwargs):
    return PingService(**kwargs)