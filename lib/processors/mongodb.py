"""
The MongoDB processor
"""

from lib.processors.processor import Processor


class MongodbProcessor(Processor):
    def __init__(self, **kwargs):
        Processor.__init__(self, **kwargs)


def create(kwargs):
    return MongodbProcessor(**kwargs)