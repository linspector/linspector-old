"""
The Linspector Interactive Shell...

This  will become an interface to Linspector at "start" time. Think about MidnightCommander... and then run
Linspector in a screen session and not as daemon, why not? BTW.: Daemonization is at this point of development
cancelled, because it makes no sense to daemonize everything. Linspector is a user software which will run in any
screen session perfectly.
"""

from lib.frontends.frontend import Frontend
import argparse

class LishFrontend(Frontend):
    def __init__(self, **kwargs):
        print("linspector interactive shell: Enter h or help for commands")
        parser = argparse.ArgumentParser()
        jobs = kwargs["jobs"]

        parser.add_argument("action", choices=["start", "stop"])
        parser.add_argument("-l", "--list", help="list current jobs")
        while True:


            rawInput = raw_input()
            print(rawInput)
            args = None
            try:
                args = parser.parse_args(rawInput.split(" "))
            except:
                pass

            print(str(args))

