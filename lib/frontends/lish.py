"""
Lish is the Linspector Interactive Shell...

This  will become a commandline interface to Linspector. Think of a network switch or router like those from Cisco.
"""


from lib.frontends.frontend import Frontend
import os
from shlex import split as shsplit
from cmd import Cmd

__version__ = "0.1"


class LishFrontend(Frontend):
    def __init__(self, **kwargs):

        #print(kwargs)
        #self.jobs = kwargs["jobs"]

        commander = LishCommander(kwargs)
        run = True
        while run:
            try:
                commander.cmdloop("Lish - Linspector interactive shell (" + __version__ + ")")
            except KeyboardInterrupt, ki:
                run = False
            except Exception, err:
                print(err)

            if commander.can_exit():
                run = False


class CommandBase(Cmd, object):
    def __init__(self):
        super(CommandBase, self).__init__()
        self._needs_update = False

    def get_completion(self, args, text, showOnZeroText=True):
        if len(text) == 0 and showOnZeroText:
            return args
        else:
            return [x for x in args if x.startswith(text)]


class Exit(CommandBase, object):
    def __init__(self):
        super(Exit, self).__init__()
        self.set_can_exit(False)

    def set_can_exit(self, canExit=True):
        self._canExit = canExit

    def can_exit(self):
        return self._canExit

    def do_exit(self, text):
        self.set_can_exit()
        return self.can_exit()

    def help_exit(self):
        print("exits linspector")

    do_EOF = do_exit
    help_EOF = help_exit


class LogCommander(Cmd, object):
    def do_log(self, text):
        print("executed %s" % text)

    def help_log(self):
        print("manage logging")


class ShellCommander(CommandBase, object):
    def do_shell(self, text):
        os.system(text)

    def help_shell(self):
        print("execute any shell command. Can also be achieved by a '!' prefix")

    def complete_shell(self, text, line, begidx, endidx):
        try:
            PATH = os.environ['PATH'].split(os.pathsep)
            bins = []
            for p in PATH:
                bins.extend(os.listdir(p))

            return self.get_completion(bins, text, False)
        except:
            pass


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


class LishCommander(Exit, ShellCommander, LogCommander):

    def __init__(self, kwargs):

        super(LishCommander, self).__init__()

        self.prompt = "<Lish>: "

        self._linConf = kwargs["linspectorConfig"]
        self._jobs = kwargs["jobs"]
        self._scheduler = kwargs["scheduler"]

        self._hostgroupArgs = ["list", "select"]

    def do_hostgroup(self, text):
        args = shsplit(text)

        if args[0] == "list":
            print("current active Hostgroups:\n")
            for l in self._linConf.get_enabled_layouts():
                print l.get_name()
                space = 4 * " "
                for hg in l.get_hostgroups():
                    print space + hg.get_name()
            print 3 * "\n"
        elif args[0] == "select":
            if len(args) < 2 or len(args[1]) == 0:
                print("must select an hostgroup")
            else:
                hgName = args[1]
                hg = self._linConf.get_hostgroup_by_name(hgName)
                if hg is None:
                    print("unknown hostgroup %s! type hostgroup list to get a list of hostgroups" % hgName)
                else:
                    try:
                        hgCommander = HostgroupCommander(hg)
                        hgCommander.cmdloop("Entering Hostmode of " + hgName + ":\n")
                    except KeyboardInterrupt, ke:
                        pass

    def do_python(self, text):
        exec text

    def help_python(self):
        print '''
            executes python using 'exec'.
            '''

    def help_hostgroup(self):
        print '''
            usage:
                hostgroup list
                                prints a list of all hostgroups
                hostgroup select HOSTGROUPNAME
                                select a hostgroup to make changes on it
            '''

    def complete_hostgroup(self, text, line, begidx, endidx):
        if begidx == 10:
            return [x for x in self._hostgroupArgs if x.startswith(text)] if len(text) > 0 else self._hostgroupArgs