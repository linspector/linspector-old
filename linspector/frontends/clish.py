"""
cLish is the Curses based Linspector Interactive Shell.

This will become a curses based commandline interface to Linspector.

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

import curses

from logging import getLogger

from linspector.frontends.frontend import Frontend

__version__ = "0.0.0"

logger = getLogger(__name__)


class ClishFrontend(Frontend):
    def __init__(self, linpsector_interface):
        super(ClishFrontend, self)

        self.screen = curses.initscr()

        self.screen.border(0)
        self.screen.addstr(12, 25, "Linspector with curses... yeah!")
        self.screen.refresh()
        self.screen.getch()

        curses.endwin()
        pass