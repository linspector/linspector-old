"""
The syslog processor
"""

from processor import Processor


class Syslog(Processor):
    def __init__(self):
        pass

def create(kwargs):
    return Syslog(**kwargs)
