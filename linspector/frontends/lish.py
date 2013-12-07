"""
Lish is the Linspector Interactive Shell.

This  will become a commandline interface to Linspector. Think of a
network switch or router like those from Cisco.

Copyright (c) 2011-2013 by Johannes Findeisen and Rafael Timmerberg

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
from logging import getLogger
from shlex import split as shsplit

from linspector.frontends.frontend import Frontend

__version__ = "0.3"

PURPLE = "\033[95m"
BLUE   = "\033[94m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
RED    = "\033[91m"
END    = "\033[0m"

logger = getLogger(__name__)


class LishFrontend(Frontend):
    def __init__(self, linspectorInterface):
        super(LishFrontend, self)
        commander = LishCommander(linspectorInterface)

        print("Type \"help\" to view available commands or \"help COMMAND\" to view the commands help")

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
        print('''
Exits Linspector
''')


class BaseCommand(object):

    def set_command(self, cmd):
        self.command = cmd

    def can_execute(self):
        if self.command.children is not None:
            return False
        else:
            return True

    def execute(self, text):
        text = shsplit(text)
        if len(text) == 0 and self.can_execute():
            self.do_action()
        else:
            pass

    def do_action(self):
        pass


def get_list():
    return []


class Command(Cmd, object):
    def __init__(self, alias, interface, shortHelp=None, extendedHelp=None, completion=get_list, func=None, children=None):
        super(Command, self).__init__()
        self.interface = interface
        self.alias = alias
        self.shortHelp = shortHelp
        self.completion = completion
        self.extendedHelp = extendedHelp
        self.func = func
        self.children = children

    def get_short_help(self):
        if self.shortHelp is not None:
            return str(self.shortHelp)
        else:
            return "undocumented. see help %s for further information." % str(self.alias)

    def get_children(self):
        if self.children is None:
            self.children = []
        return self.children

    def find_child_by_alias(self, alias):
        pass

    def get_extended_help(self):
        return self.extendedHelp

    def print_help(self):
        help = self.get_extended_help()
        if help is not None:
            print help
        elif len(self.get_children()) > 0:
            print "%s usage:\n" % str(self.alias)
            for child in self.get_children():
                print child.alias + "\t\t" + child.short_help() + "\n"
        else:
            print "invalid or unsupported syntax"
        print "\n"

    def default(self, line):
        if len(line) == 0:
            if self.func is not None:
                return self.func(self.interface)
            else:
                self.print_help()
        else:
            line = shsplit(line)

            if len(line) > 0 and line[0] in [child.alias for child in self.get_children()]:
                pass

    def completenames(self, text, *ignored):
        ret = super(Command, self).completenames(text, *ignored)
        if len(self.get_children()) > 0:
            func = lambda alias: True
            if len(text) > 0:
                func = lambda alias:  alias.startswith(text)
            ret.extend([cmd.alias for cmd in self.children if func(cmd.alias)])
        return ret

    def completedefault(self, text, *ignored):
        pass

    def do_help(self, arg):
        if arg:
            pass
        else:
            pass


class CommandTree(object):
    def __init__(self, name):
        self.name = name


class LishCommander(Exit):
    def __init__(self, linspector_interface):
        super(LishCommander, self).__init__()

        self.prompt = BLUE + "<Lish@" + socket.gethostname() + ">: " + END
        self.interface = linspector_interface

    def do_python(self, text):
        exec text

    def help_python(self):
        print('''
Executes Python code using 'exec'
''')

    def print_color(self, color, text):
        print(color + str(text) + END)

    def print_dict(self, dict):
        for key, val in dict.items():
            tab = ":\t"
            if len(str(key)) < 7:
                tab += "\t"

            print(GREEN + str(key) + END + tab + YELLOW + str(val) + END)

    def print_jobs_infos(self, job):
        self.print_dict(self.interface.get_job_info_dict(job))

    def do_job(self, text):
        text = shsplit(text)
        job_hex = text[0]
        job = self.interface.find_job_by_hex_string(job_hex)

        if job is None:
            self.print_color(RED, "First parameter must be a job ID. Get a List of all IDs by typing 'jobs list'")
            self.help_job()
            return

        if len(text) == 1:
            self.print_jobs_infos(job)
            return

        cmd = text[1]
        if cmd in ["enable", "disable"]:
            job.set_enabled("n" in cmd)
        else:
            self.print_color(RED, "Invalid or missing parameter")
            self.help_job()

    def complete_job(self, text, line, begidx, endidx):
        if begidx == 4:
            return self.get_completion(self.interface.get_job_hex_strings(), text)
        elif begidx == 13:
            return self.get_completion(["enable", "disable"], text)

    def help_job(self):
        print('''
Usage:
  <ID>          Prints extended information about this job
  <ID> enable   Enables a job
  <ID> disable  Disables a job
''')

    def do_jobs(self, text):
        if text == "list":
            for job in self.interface.jobs:
                job_dict = self.interface.get_job_info_dict(job)
                print GREEN + job_dict["Job"] + END + ": " + \
                    PURPLE + "Hostgroup" + END + ": " + job_dict["Hostgroup"] + \
                    PURPLE + " Host" + END + ": " + job_dict["Host"] + \
                    PURPLE + " Service" + END + ": " + job_dict["Service"] + \
                    PURPLE + " Next run" + END + ": " + job_dict["Next run"] + \
                    PURPLE + " Runs" + END + ": " + job_dict["Runs"] + \
                    PURPLE + " Fails" + END + ": " + job_dict["Fails"] + \
                    PURPLE + " Status" + END + ": " + job_dict["Status"] + \
                    PURPLE + " Enabled" + END + ": " + job_dict["Enabled"]
        elif text == "count":
            print GREEN + "Job Count" + END + ":\t" + str(self.interface.get_job_count())
        else:
            self.print_color(RED, "Invalid or missing parameter")
            self.help_jobs()

    def help_jobs(self):
        print('''
Usage:
  count  Show count of all jobs
  list   Lists all jobs
''')

    def do_gui(self, text):
        try:
            from linspector.frontends.lishgui import LishGui
            gui = LishGui(self.interface)
            gui.run()
        except Exception, err:
            self.print_color(RED, "Error: " + str(err) + ", no GUI support!")

    def help_gui(self):
        print('''
Usage:
  gui  start the graphical user interface
''')

    def do_host(self, text):
        pass

    def help_host(self):
        print('''
Usage:
  <HOST>          Prints extended information about <HOST>
  <HOST> enable   Enables all jobs for <HOST>
  <HOST> disable  Disables all jobs for <HOST>
  <HOST> list     Lists all jobs for <HOST>
''')

    def do_hostgroup(self, text):
        pass

    def help_hostgroup(self):
        print('''
Usage:
  <HOSTGROUP>          Prints extended information about <HOSTGROUP>
  <HOSTGROUP> enable   Enables all jobs for <HOSTGROUP>
  <HOSTGROUP> disable  Disables all jobs for <HOSTGROUP>
  <HOSTGROUP> list     Lists all jobs for <HOSTGROUP>
''')

    def do_hostgrouphost(self, text):
        pass

    def help_hostgrouphost(self):
        print('''
Usage:
  <HOSTGROUP> <HOST>          Prints extended information about <HOST> in <HOSTGROUP>
  <HOSTGROUP> <HOST> enable   Enables all jobs for <HOST> in <HOSTGROUP>
  <HOSTGROUP> <HOST> disable  Disables all jobs for <HOST> in <HOSTGROUP>
  <HOSTGROUP> <HOST> list     Lists all jobs for <HOST> in <HOSTGROUP>
''')

    def do_hostgroupmember(self, text):
        pass

    def help_hostgroupmember(self):
        print('''
Usage:
  <HOSTGROUP> <MEMBER>  Prints extended information about <MEMBER> in <HOSTGROUP>
''')

    def do_shell(self, text):
        os.system(text)

    def help_shell(self):
        print("Execute any shell command. Can also be achieved by a '!' prefix")

    def complete_shell(self, text, line, begidx, endidx):
        try:
            PATH = os.environ['PATH'].split(os.pathsep)
            bins = []
            for p in PATH:
                bins.extend(os.listdir(p))

            return self.get_completion(bins, text, False)
        except:
            pass

    def do_log(self, text):
        text = shsplit(text)

        if text[0] == "less":
            try:
                # TODO: do the less on the logfile set by args and not a static path
                with open(os.path.dirname(os.path.abspath(__file__)) + "/../../log/linspector.log"):
                    os.system("less " + os.path.dirname(os.path.abspath(__file__)) + "/../../log/linspector.log")
            except IOError:
                self.print_color(RED, "Logfile not found.")
                self.help_log()
        elif text[0] == "level":
            if text[1] in ["debug", "error", "info", "warning"]:
                self.interface.set_log_level(text[1])
                self.print_color(GREEN, "Setting log level to: " + text[1])
            else:
                self.print_color(RED, "Log level " + text[1] + " not supported")
        elif text[0] == "more":
            try:
                # TODO: do the more on the logfile set by args and not a static path
                with open(os.path.dirname(os.path.abspath(__file__)) + "/../../log/linspector.log"):
                    os.system("more " + os.path.dirname(os.path.abspath(__file__)) + "/../../log/linspector.log")
            except IOError:
                self.print_color(RED, "Logfile not found.")
                self.help_log()
        elif text[0] == "tail":
            try:
                # TODO: do the tail on the logfile set by args and not a static path
                with open(os.path.dirname(os.path.abspath(__file__)) + "/../../log/linspector.log"):
                    os.system("tail -F " + os.path.dirname(os.path.abspath(__file__)) + "/../../log/linspector.log")
            except IOError:
                self.print_color(RED, "Logfile not found.")
                self.help_log()

    def help_log(self):
        print('''
Usage:
  less          less on the linspector logfile (press "q" to exit)
  level <LEVEL> set the log level to <LEVEL>
                supported levels are debug, error, info, warning
  more          more on the linspector logfile (press "q" to exit)
  tail          tail (-F) on the linspector logfile (Ctrl+C to exit)
''')

    def do_status(self, text):
        # TODO: print instance name from core config
        print GREEN + "Hostname" + END + ":\t" + socket.gethostname()
        # TODO: print instance uptime
        print GREEN + "Job Count" + END + ":\t" + str(self.interface.get_job_count())
        thread_info = self.interface.get_thread_count()
        print GREEN + "Threads" + END + ":\t" + str(thread_info["Num Threads"]) + "/" + str(thread_info["Max Threads"])
        print GREEN + "Core Version" + END + ":\t" + self.interface.get_version()
        print GREEN + "Lish Version" + END + ":\t" + __version__

    def help_status(self):
        print('''
Show status information about the Linspector instance
''')

    def do_about(self, text):
        self.print_color(GREEN,  "Linspector Monitoring\n")
        self.print_color(YELLOW, "Developers:")
        self.print_color(BLUE,   " - Johannes Findeisen <hanez@linspector.org>")
        self.print_color(BLUE,   " - Rafael Timmerberg <ruff@linspector.org>\n")
        self.print_color(PURPLE, "(c) 2011 - 2013")
        self.print_color(PURPLE, "Web: http://linspector.org")
        self.print_color(PURPLE, "License: GNU Affero General Public License Version 3.0")

    def help_about(self):
        print('''
Show information about Linspector
''')

    def do_license(self, text):
        os.system("less " + os.path.dirname(os.path.abspath(__file__)) + "/../../LICENSE")

    def help_license(self):
        print('''
Show license information
''')

    def do_man(self, text):
        try:
            with open(os.path.dirname(os.path.abspath(__file__)) + "/../../man/" + text + ".md"):
                #TODO: maybe convert markdown to plain text before displaying it and write own pager in pure Python
                os.system("less " + os.path.dirname(os.path.abspath(__file__)) + "/../../man/" + text + ".md")
        except IOError:
            self.print_color(RED, "Manual page \"" + text + "\" not found.")
            self.help_man()

    def help_man(self):
        print('''
Usage:
  <PAGE>  Show manual page <PAGE>
''')
