"""
The shell service. This is for executing local shell commands and retrieve the output.

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

from linspector.services.service import Service


class ShellService(Service):
    def __init__(self, **kwargs):
        super(ShellService, self).__init__(**kwargs)
        
        args = self.get_arguments()
        if "command" in args:
            self.command = args["command"] 
        else:
            raise Exception("There is no command argument")
        
    def needs_arguments(self):
        return True 

    def execute(self):
        self.command.call()


def create(kwargs):
    return ShellService(**kwargs)