"""
The MariaDB processor
"""

from processor import Processor


class MariadbProcessor(Processor):
    def __init__(self):
        pass


def create(kwargs):
    return MariadbProcessor(**kwargs)