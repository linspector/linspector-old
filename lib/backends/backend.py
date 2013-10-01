"""
Backends can be a http service or xml-rpc service; let's say background threads providing an interface somewhere. They
should run as background threads.

Backends are absolutely no requirement for running Linspector.
"""


class Backend():
    def __init__(self, **kwargs):
        return