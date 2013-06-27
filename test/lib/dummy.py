__author__ = 'rafael'


class Dummy(object):
    def __init__(self, **kwargs):
        self.args = kwargs

def create(args):
    return Dummy(**args)
