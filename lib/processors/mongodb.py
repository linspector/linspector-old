"""
The MongoDB processor
"""

from processor import Processor


class MongodbProcessor(Processor):
    def __init__(self):
        pass


def create(kwargs):
    return MongodbProcessor(**kwargs)