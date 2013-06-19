"""
The MariaDB processor
"""

from lib.processors.processor import Processor


class MariadbProcessor(Processor):
    def __init__(self, **kwargs):
        pass


def create(kwargs):
    return MariadbProcessor(**kwargs)