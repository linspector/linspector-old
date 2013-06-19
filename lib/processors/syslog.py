"""
The syslog processor
"""

from lib.processors.processor import Processor


class SyslogProcessor(Processor):
    def __init__(self, **kwargs):
        pass


def create(kwargs):
    return SyslogProcessor(**kwargs)