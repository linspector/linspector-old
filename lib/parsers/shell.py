from lib.parsers.parser import Parser


class ShellParser(Parser):
    def __init__(self, **kwargs):
        pass


def create(kwargs):
    return ShellParser(**kwargs)