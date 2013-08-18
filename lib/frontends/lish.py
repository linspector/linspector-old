"""
Lish is the Linspector Interactive Shell...

This  will become an interface to Linspector at "start" time. Think about MidnightCommander... and then run
Linspector in a screen session and not as daemon, why not? BTW.: Daemonization is at this point of development
cancelled, because it makes no sense to daemonize everything. Linspector is a user software which will run in any
screen session perfectly.
"""

# what is this?
#from requests.status_codes import title

'''
     #see http://docs.python.org/dev/library/argparse.html

     Cheat Sheet:

    ++++++++++++ Argument Parser creation +++++++++++++++++
    prog - The name of the program (default: sys.argv[0])
    usage - The string describing the program usage (default: generated from arguments added to parser)
    description - Text to display before the argument help (default: none)
    epilog - Text to display after the argument help (default: none)
    parents - A list of ArgumentParser objects whose arguments should also be included
    formatter_class - A class for customizing the help output
    prefix_chars - The set of characters that prefix optional arguments (default: -)
    fromfile_prefix_chars - The set of characters that prefix files from which additional arguments should be read (default: None)
    argument_default - The global default value for arguments (default: None)
    conflict_handler - The strategy for resolving conflicting optionals (usually unnecessary)


    ++++++++++++++++++ add_argument() +++++++++++++++++++++
    name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action - The basic type of action to be taken when this argument is encountered at the command line.
    nargs - The number of command-line arguments that should be consumed.
    const - A constant value required by some action and nargs selections.
    default - The value produced if the argument is absent from the command line.
    type - The type to which the command-line argument should be converted.
    choices - A container of the allowable values for the argument.
    required - Whether or not the command-line option may be omitted (optionals only).
    help - A brief description of what the argument does.
    metavar - A name for the argument in usage messages.
    dest - The name of the attribute to be added to the object returned by parse_args().

    +++++++ add_subparsers()-> obj with one method -> add_parser() +++++++++


'''

from lib.frontends.frontend import Frontend
import argparse
import os
from shlex import split as shsplit
from cmd import Cmd

VERSION = "0.1"


class LishFrontend(Frontend):
    def __init__(self, **kwargs):

        print(kwargs)
        #self.jobs = kwargs["jobs"]

        ns = argparse.Namespace()

        commander = LishCommander(kwargs)
        run = True
        while run:
            try:
                commander.cmdloop("LISH - Linspector interactive shell")
            except KeyboardInterrupt, ki:
                run = False
            except Exception, err:
                print(err)

            if commander.can_exit():
                run = False


class Exit(Cmd, object):
    def __init__(self):
        super(Exit, self).__init__()
        self._canExit = False

    def can_exit(self):
        return self._canExit

    def do_exit(self, text):
        self.exit = True
        return self.can_exit()

    def help_exit(self):
        print("exits linspector")

    do_EOF = do_exit
    help_EOF = help_exit


class ShellCommander(Cmd, object):
    def do_shell(self, text):
        os.system(text)

    def help_shell(self):
        print("execute any shell command. Can also be archieved by a '!' postfix")


class HostgroupCommander(Exit, object):
    def __init__(self, hostgroup):
        super(HostgroupCommander, self).__init__()
        self.prompt = "<HG:%s>" % hostgroup.get_name()
        self._hostgroup = hostgroup

    def do_member(self, text):
        print("dear maintainer, ")
        print("I typed '%s', and would appreciate, if you could stay away from outside to implement it" % text)
        print("must be kidding me!!!")
        return True

    def help_member(self):
        print("gives you control over a member of the hostgroup")


class LishCommander(Exit, ShellCommander):

    def __init__(self, kwargs):

        super(LishCommander, self).__init__()

        self.prompt = "<Lish>: "

        self._layouts = kwargs["layouts"]
        self._jobs = kwargs["jobs"]
        self._scheduler = kwargs["scheduler"]

        self._hostgroupArgs = ["list", "select"]

    def do_hostgroup(self, text):
        args = shsplit(text)

        if args[0] == "list":
            print("current active Hostgroups:\n")
            for l in self._layouts:
                if l.is_enabled():
                    print l.get_name()
                    space = 4 * " "
                    for hg in l.get_hostgroups():
                        print space + hg.get_name()
            print 3 * "\n"
        elif args[0] == "select":
            hostgroupName = args[1]
            if len(hostgroupName) == 0:
                print "must select an hostgroup"
            for layout in self._layouts:
                for lhg in layout.get_hostgroups():
                    if lhg.get_name() == hostgroupName:
                        try:
                            hgCommander = HostgroupCommander(lhg)
                            hgCommander.cmdloop("Entering Hostmode of " + hostgroupName)
                        except KeyboardInterrupt, ke:
                            pass

    def help_hostgroup(self):
        print '''
            help for Hostgroup
            '''

    def complete_hostgroup(self, text, line, begidx, endidx):
        "hostgroup + ' '"
        if begidx == 10:
            return [x for x in self._hostgroupArgs if x.startswith(text)] if len(text) > 0 else self._hostgroupArgs