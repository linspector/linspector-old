"""
The MariaDB processor
"""

from lib.processors.processor import Processor


class MariadbProcessor(Processor):
    def __init__(self, **kwargs):
        Processor.__init__(self, **kwargs)


def create(kwargs):
    return MariadbProcessor(**kwargs)