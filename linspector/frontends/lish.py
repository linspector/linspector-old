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

from linspector.frontends.frontend import Frontend
import os
from shlex import split as shsplit
from cmd import Cmd

__version__ = "0.1.1"


class LishFrontend(Frontend):
    def __init__(self, linpsectorInterface):
        super(LishFrontend, self)
        #print(kwargs)
        #self.jobs = kwargs["jobs"]

        commander = LishCommander(linpsectorInterface)
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
    def __init__(self, linspectorInterface):

        super(LishCommander, self).__init__()

        self.prompt = "<Lish>: "

        self.interface = linspectorInterface

    def do_hostgroup(self, text):
        args = shsplit(text)

        if args[0] == "list":
            print("current active Hostgroups:\n")
            for l in self.interface.get_enabled_layouts():
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
                    except KeyboardInterrupt, key:
                        pass

    def complete_hostgroup(self, text, line, begidx, endidx):
        if begidx == 10:
            return self.get_completion(["list", "select"], text)

    def help_hostgroup(self):
        print "usage:\n\t" + \
              "hostgroup list\n\t\t\t" + \
              "prints a list of all hostgroups\n\t" + \
              "hostgroup select HOSTGROUPNAME\n\t\t\t" + \
              "select a hostgroup to make changes on it"

    def do_python(self, text):
        exec text

    def help_python(self):
        print "executes python using 'exec'."

    def print_jobs_infos(self, job):
        print "Job: " + job.hex_string() + "\n" + \
              "Host: " + job.host + "\n" + \
              "Service: " + job.service.get_type() + "\n" + \
              "Members: " + str([member.name for member in job.members])

    def do_job(self, text):
        text = shsplit(text)
        job_hex = text[0]
        job = self.interface.find_job_by_hex_string(job_hex)

        if job is None:
            print "first parameter must be a job hex id! get a List of all ids by typing 'jobs list'\n"
            self.help_job()

        if len(text) == 1:
            self.print_jobs_infos(job)
            return

        cmd = text[1]
        if cmd in ["enable", "disable"]:
            job.set_enabled("n" in cmd)
        else:
            print "invalid or missing parameter\n"
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
            print "invalid or missing parameter\n"
            self.help_jobs()

    def help_jobs(self):
        print "Joblist helper functions:\n\t" + "list:\t\t\tlists all jobs"