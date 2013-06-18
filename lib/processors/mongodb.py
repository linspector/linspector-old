"""
The MongoDB processor
"""

from processor import Processor


class Mongodb(Processor):
    def __init__(self):
        pass


def create(kwargs):
    return Mongodb(**kwargs)