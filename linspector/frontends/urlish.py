"""
urlish is the urwid based Linspector Interactive Shell.

Uses: http://excess.org/urwid/

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

import urwid

from logging import getLogger

from linspector.frontends.frontend import Frontend

__version__ = "0.1.1"

logger = getLogger(__name__)


class JobWidget(urwid.FlowWidget):
    def __init__(self):
        pass


class JobListBox(urwid.WidgetWrap):
    def __init__(self):
        self.body = urwid.SimpleListWalker([])
        self.listbox = urwid.ListBox(self.body)
        urwid.WidgetWrap.__init__(self, self.listbox)

    def keypress(self, size, key):
        if key == ':':
            main_frame.set_focus('footer')
            command_prompt.set_caption(':')
        else:
            return self.listbox.keypress(size, key)


class CommandPrompt(urwid.Edit):
    def __init__(self):
        urwid.Edit.__init__(self, '')
        self.current_command = None
        self.history = []
        self.history_offset = 0

    def clear(self):
        self.set_caption('')
        self.set_edit_text('')

    def keypress(self, size, key):
        if key == 'backspace':
            if self.edit_text == '':
                self.set_caption('')
                loop.draw_screen()
                main_frame.set_focus('body')
            else:
                return urwid.Edit.keypress(self, size, key)

        elif key == 'enter' and not self.get_edit_text() == '':
            command = self.get_edit_text()
            self.history.append(command)
            self.history_offset = 0
            command = command.split(' ')

            if command[0] in ('log', 'l'):
                if 2 <= len(command):
                    if command[1] in ('debug', 'info', 'error', 'warning'):
                        self.clear()
                        interface.set_log_level(command[1])
                        status_bar.set_text(" Set log level to: " + command[1])
                        main_frame.set_focus('body')
                    else:
                        status_bar.set_text(" Log level \"" + command[1] + "\" not available")
                else:
                    status_bar.set_text(" Command argument missing. Args are: debug, info, error and warning")

            elif command[0] in ('quit', 'q'):
                self.clear()
                status_bar.set_text(" Stopping Linspector...")
                raise urwid.ExitMainLoop()

            elif command[0] in ('version', 'v'):
                self.clear()
                status_bar.set_text(" Linspector " + str(interface.get_version()) + ", urlish " + __version__)
                main_frame.set_focus('body')

            else:
                msg = 'Error: There is no command named "' + command[0] + '"'
                status_bar.set_text(' ' + msg)
                logger.debug(msg)
                pass

        elif key in ('ctrl x', 'esc'):
            main_frame.set_focus('body')
            self.history_offset = 0
            self.clear()

        elif key in ('ctrl p', 'up'):
            if self.get_edit_text() not in self.history:
                self.current_command = self.get_edit_text()
            try:
                self.history_offset -= 1
                command = self.history[self.history_offset]
                self.set_edit_text(command)
                self.set_edit_pos(len(command))
            except IndexError:
                self.history_offset += 1

        elif key in ('ctrl n', 'down'):
            if self.get_edit_text() not in self.history:
                self.current_command = self.get_edit_text()
            try:
                self.history_offset += 1
                if self.history_offset == 0:
                    command = self.current_command
                elif self.history_offset < 0:
                    command = self.history[self.history_offset]
                else:
                    raise IndexError
                self.set_edit_text(command)
                self.set_edit_pos(len(command))
            except IndexError:
                self.history_offset -= 1

        else:
            return urwid.Edit.keypress(self, size, key)


def update(main_loop, user_data):
    thread_count = interface.get_thread_count()
    header_bar.set_text(" Linspector,"
                        " Jobs: " + str(interface.get_job_count()) +
                        " Threads: " + str(thread_count["Num Threads"]) +
                        "/" + str(thread_count["Max Threads"]))
    main_loop.set_alarm_in(1, update)


class UrlishFrontend(Frontend):
    def __init__(self, linspector_interface):
        super(UrlishFrontend, self)

        global job_list_box
        global command_prompt
        global header_bar
        global status_bar
        global main_frame
        global loop
        global interface

        palette = [('top', 'white', 'dark red'),
                   ('status', 'white', 'dark blue'),
                   ('prompt', 'white', 'black')]

        interface = linspector_interface

        header_message = ' Linspector (' + str(linspector_interface.get_version()) + ')'
        header_bar = urwid.Text(header_message, align='left')
        header = urwid.Pile([urwid.AttrMap(header_bar, 'top')])

        command_prompt = CommandPrompt()

        welcome_message = ' Type ":h <Enter>" for help, ":q <Enter>" to quit'
        status_bar = urwid.Text(welcome_message, align='left')
        footer = urwid.Pile([urwid.AttrMap(status_bar, 'status'), urwid.AttrMap(command_prompt, 'prompt')])

        job_list_box = JobListBox()

        main_frame = urwid.Frame(body=job_list_box, header=header, footer=footer)

        loop = urwid.MainLoop(main_frame, palette)
        loop.set_alarm_in(0, update)
        loop.run()