"""
The syslog processor
"""

from processor import Processor


class SyslogProcessor(Processor):
    def __init__(self):
        pass


def create(kwargs):
    return SyslogProcessor(**kwargs)