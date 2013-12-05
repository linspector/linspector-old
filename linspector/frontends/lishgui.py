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

"""
TODO:

 General:

 - think about if a simple scrollable list of jobs may be a lot easier to use
   in combination with some tabs for job list, hostgroup jobs, host jobs etc.
   i think this is a lot more flexible when reloading data. using the current
   we have to rebuild the complete tree on reloading. or figure out how to
   rebuild only selected nodes on reload. when using a tab/list based solution
   we could even build a tab that on shows current errors, one for warnings etc.
   these could we rebuild on access or on key stroke. these lists then only need
   some action handlers for disabling/enabling or for showing detailed
   information about the selected job. i think the tab/list approach is much
   easier to handle then jumping like a monkey through a tree structure... ;)

 For the tree based solution:

 - remove all this global stuff and set needed stuff as arguments

 - fix mouse handling; nice feature to select stuff using the mouse. currently
   it raises an exception.
"""

import urwid

from logging import getLogger

logger = getLogger(__name__)


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
                status_bar.set_text(" Linspector " + str(interface.get_version()))
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


class ExampleTreeWidget(urwid.TreeWidget):
    def __init__(self, node):
        self.__super.__init__(node)
        #self.expanded = False
        #self.update_expanded_icon()

    def get_display_text(self):
        return self.get_node().get_value()['name']


class ExampleNode(urwid.TreeNode):
    def load_widget(self):
        return ExampleTreeWidget(self)


class ServiceParentNode(urwid.ParentNode):
    def load_widget(self):
        return ExampleTreeWidget(self)

    def load_child_keys(self):
        data = self.get_value()
        return range(len(data['children']))

    def load_child_node(self, key):
        childdata = self.get_value()['children'][key]
        childdepth = self.get_depth() + 1
        if 'children' in childdata:
            childclass = ServiceParentNode
        else:
            childclass = ExampleNode
        return childclass(childdata, parent=self, key=key, depth=childdepth)


class HostParentNode(urwid.ParentNode):
    def load_widget(self):
        return ExampleTreeWidget(self)

    def load_child_keys(self):
        data = self.get_value()
        return range(len(data['children']))

    def load_child_node(self, key):
        childdata = self.get_value()['children'][key]
        childdepth = self.get_depth() + 1
        if 'children' in childdata:
            childclass = ServiceParentNode
        else:
            childclass = ExampleNode
        return childclass(childdata, parent=self, key=key, depth=childdepth)


class HostgroupParentNode(urwid.ParentNode):
    def load_widget(self):
        return ExampleTreeWidget(self)

    def load_child_keys(self):
        data = self.get_value()
        return range(len(data['children']))

    def load_child_node(self, key):
        childdata = self.get_value()['children'][key]
        childdepth = self.get_depth() + 1
        if 'children' in childdata:
            childclass = HostParentNode
        else:
            childclass = ExampleNode
        return childclass(childdata, parent=self, key=key, depth=childdepth)


class RootParentNode(urwid.ParentNode):
    def load_widget(self):
        return ExampleTreeWidget(self)

    def load_child_keys(self):
        data = self.get_value()
        return range(len(data['children']))

    def load_child_node(self, key):
        childdata = self.get_value()['children'][key]
        childdepth = self.get_depth() + 1
        if 'children' in childdata:
            childclass = HostgroupParentNode
        else:
            childclass = ExampleNode
        return childclass(childdata, parent=self, key=key, depth=childdepth)


class LishGui():
    def __init__(self, linspector_interface):
        self.interface = linspector_interface

    @staticmethod
    def unhandled_input(key):
        if key in (':'):
            main_frame.set_focus('footer')
            command_prompt.set_caption(':')
        elif key in ('c'):
            #collapse all children of current node
            pass
        elif key in ('C'):
            #collapse all nodes
            pass
        elif key in ('d'):
            #disable all jobs for current node
            pass
        elif key in ('e'):
            #enable all jobs for current node
            pass
        elif key in ('r'):
            #reload child data of current node
            pass
        elif key in ('R'):
            #reload child data of all nodes
            pass
        elif key in ('x'):
            #expand all children of current node
            pass
        elif key in ('X'):
            #expand all nodes
            pass

    def run(self):
        global job_list_box
        global command_prompt
        global header_bar
        global status_bar
        global main_frame
        global loop
        global interface

        palette = [('body', 'white', 'black'),
                   ('foot_bar', 'white', 'black'),
                   ('top', 'white', 'dark red'),
                   ('status', 'white', 'dark blue'),
                   ('prompt', 'white', 'black')]

        foot_text = [('title', "Navigation:"), "    ",
                     ('key', "UP"), ",", ('key', "DOWN"), ",",
                     ('key', "PAGE UP"), ",", ('key', "PAGE DOWN"),
                     "  ",
                     ('key', "+"), ",",
                     ('key', "-"), "  ",
                     ('key', "LEFT"), "  ",
                     ('key', "HOME"), "  ",
                     ('key', "END")]

        interface = self.interface

        top_node = RootParentNode(get_example_tree())
        job_list_box = urwid.TreeListBox(urwid.TreeWalker(top_node))
        job_list_box.offset_rows = 1

        header_message = ' Linspector (' + str(self.interface.get_version()) + ')'
        header_bar = urwid.Text(header_message, align='left')
        header = urwid.Pile([urwid.AttrMap(header_bar, 'top')])

        command_prompt = CommandPrompt()

        foot_bar = urwid.Text(foot_text, align='left')

        welcome_message = ' Type ":h <Enter>" for help, ":q <Enter>" to quit'
        status_bar = urwid.Text(welcome_message, align='left')
        footer = urwid.Pile([urwid.AttrMap(foot_bar, 'foot_bar'),
                             urwid.AttrMap(status_bar, 'status'),
                             urwid.AttrMap(command_prompt, 'prompt')])

        main_frame = urwid.Frame(body=job_list_box, header=header, footer=footer)

        loop = urwid.MainLoop(main_frame, palette, unhandled_input=self.unhandled_input, handle_mouse=False)
        loop.set_alarm_in(0, update)
        loop.run()


def update(main_loop, user_data):
    thread_count = interface.get_thread_count()
    header_bar.set_text(" Linspector,"
                        " Jobs: " + str(interface.get_job_count()) +
                        " Threads: " + str(thread_count["Num Threads"]) +
                        "/" + str(thread_count["Max Threads"]))
    main_loop.set_alarm_in(1, update)


def get_example_tree():
    retval = {"name": "ROOT", "children": []}
    for i in range(10):
        retval['children'].append({"name": "HOSTGROUP " + str(i)})
        retval['children'][i]['children'] = []
        for j in range(5):
            retval['children'][i]['children'].append({"name": "HOST " + str(i) + "." + str(j)})
            retval['children'][i]['children'][j]['children'] = []
            for k in range(3):
                retval['children'][i]['children'][j]['children'].append({"name": "SERVICE " + str(i) +
                                                                                 "." + str(j) +
                                                                                 "." + str(k)})
    return retval