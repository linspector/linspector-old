from parser import Parser


class ShellParser(Parser):
    def __init__(self):
        pass


def create(kwargs):
    return ShellParser(**kwargs)