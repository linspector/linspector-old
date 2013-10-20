"""
Lish is the Linspector Interactive Shell.

This  will become a commandline interface to Linspector. Think of a
network switch or router like those from Cisco.

Copyright (c) 2011-2013 "Johannes Findeisen and Rafael Timmerberg"

This file is part of Linspector (http://linspector.org).

Linspector is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import os
import socket
from cmd import Cmd
from shlex import split as shsplit

from linspector.frontends.frontend import Frontend

__version__ = "0.2"

PURPLE = "\033[95m"
BLUE   = "\033[94m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
RED    = "\033[91m"
END    = "\033[0m"


class LishFrontend(Frontend):
    def __init__(self, linpsectorInterface):
        super(LishFrontend, self)
        #print(kwargs)
        #self.jobs = kwargs["jobs"]

        commander = LishCommander(linpsectorInterface)
        run = True
        while run:
            try:
                commander.cmdloop(GREEN + "Lish - Linspector interactive shell (" + __version__ + ")" + END)
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

    def get_completion(self, args, text):
        if len(text) == 0:
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


class Command(object):
    def __init__(self, name, command, helpText, children=None):
        self.name = name
        self.command = command
        self.helpText = helpText
        self.children = children
        self.completion = []
        if isinstance(children, list):
            for child in children:
                self.completion.append((child.get_name()))


class CommandTree(object):
    def __init__(self, name):
        self.name = name


class LishCommander(Exit, ShellCommander, LogCommander):
    def __init__(self, linspectorInterface):

        super(LishCommander, self).__init__()

        self.prompt = BLUE + "<Lish@" + socket.gethostname() + ">: " + END

        self.interface = linspectorInterface

    def do_hostgroup(self, text):
        args = shsplit(text)

        if args[0] == "list":
            print("current active Hostgroups:\n")
            for l in self.interface.get_enabled_layouts():
                print l.get_name()
                space = 4 * " "
                for hg in l.get_hostgroutrolldrosselps():
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
                    except KeyboardInterrupt, key:
                        pass

    def complete_hostgroup(self, text, line, begidx, endidx):
        if begidx == 10:
            return self.get_completion(["list", "select"], text)

    def help_hostgroup(self):
        print '''usage:
              hostgroup list
              prints a list of all hostgroups
              hostgroup select HOSTGROUPNAME
              select a hostgroup to make changes on it
              '''

    def do_python(self, text):
        exec text

    def help_python(self):
        print "executes python using 'exec'."

    def print_color(self, color, text):
        print color + str(text) + END

    def print_dict(self, dict):
        for key, val in dict.items():
            tab = ":\t"
            if len(str(key)) < 7:
                tab += "\t"

            print GREEN + str(key) + END + tab + YELLOW + str(val) + END

    def print_jobs_infos(self, job):
        self.print_dict(self.interface.get_job_info_dict(job))

    def do_job(self, text):
        text = shsplit(text)
        job_hex = text[0]
        job = self.interface.find_job_by_hex_string(job_hex)

        if job is None:
            print RED + "first parameter must be a job hex id! get a List of all ids by typing 'jobs list'\n" + END
            self.help_job()
            return

        if len(text) == 1:
            self.print_jobs_infos(job)
            return

        cmd = text[1]
        if cmd in ["enable", "disable"]:
            job.set_enabled("n" in cmd)
        else:
            print RED + "invalid or missing parameter\n" + END
            self.help_job()

    def complete_job(self, text, line, begidx, endidx):
        if begidx == 4:
            return self.get_completion(self.interface.get_job_hex_strings(), text)
        elif begidx == 13:
            return self.get_completion(["enable", "disable"], text)

    def help_job(self):
        print '''usage:
              <ID>              prints extended information about this job
              <ID> enable:      enables a job
              <ID> disable:     disables a job
              '''

    def do_jobs(self, text):
        if text == "list":
            for job in self.interface.jobs:
                print job.pretty_string()
        else:
            print RED + "invalid or missing parameter\n" + END
            self.help_jobs()

    def help_jobs(self):
        print '''usage:
              list              lists all jobs
              '''

    def do_about(self, text):
        self.print_color(GREEN,  "Linspector Monitoring\n")
        self.print_color(YELLOW, "Developers:")
        self.print_color(BLUE,   " - Johannes Findeisen <hanez@linspector.org>")
        self.print_color(BLUE,   " - Rafael Timmerberg <ruff@linspector.org>\n")
        self.print_color(PURPLE, "(c) 2011 - 2013")
        self.print_color(PURPLE, "Web: http://linspector.org")
        self.print_color(PURPLE, "License: GNU Affero General Public License Version 3.0")

    def help_about(self):
        print '''Show information about Linspector'''

    def do_license(self, text):
        os.system("less " + os.path.dirname(os.path.abspath(__file__)) + "/../../LICENSE")

    def help_license(self):
        print '''Show license information'''

    def do_man(self, text):
        try:
            with open(os.path.dirname(os.path.abspath(__file__)) + "/../../man/" + text + ".md"):
                os.system("less " + os.path.dirname(os.path.abspath(__file__)) + "/../../man/" + text + ".md")
        except IOError:
            self.print_color(RED, "Manual page \"" + text + "\" not found.")
            self.help_man()

    def help_man(self):
        print '''usage:
              man <PAGE>        Show manual page
              '''