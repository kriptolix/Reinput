# window.py
#
# Copyright 2024 k
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk

from ...roller import command_handler, parse_command

from .dicearea import DiceArea
from .infoarea import InfoArea


@Gtk.Template(resource_path='/io/gitlab/kriptolix/'
              'Poliedros/src/gtk/ui/RollArea.ui')
class RollArea(Gtk.Box):
    __gtype_name__ = 'RollArea'

    _results = Gtk.Template.Child()
    _stack = Gtk.Template.Child()
    _dice_area = Gtk.Template.Child()
    _info_area = Gtk.Template.Child()    
    _display = Gtk.Template.Child()
    _mode_button = Gtk.Template.Child()
    _roll_button = Gtk.Template.Child()
    _clear_button = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        # d20, d12, d10, d8, d6, d4, increment
        self._command = [0, 0, 0, 0, 0, 0, 0]

        self._roll_button.connect("clicked", self._test)

        self._dice_area._d4_button.connect("clicked", self._add_elements, 5)
        self._dice_area._d6_button.connect("clicked", self._add_elements, 4)
        self._dice_area._d8_button.connect("clicked", self._add_elements, 3)
        self._dice_area._d10_button.connect("clicked", self._add_elements, 2)
        self._dice_area._d12_button.connect("clicked", self._add_elements, 1)
        self._dice_area._d20_button.connect("clicked", self._add_elements, 0)
        self._dice_area._plus_button.connect("clicked", self._add_elements, 6)
        self._dice_area._minus_button.connect("clicked", self._add_elements, 7)
        self._clear_button.connect("clicked", self._clear_diplay)
        self._mode_button.connect("toggled", self._change_mode)        

    def _update_result(self, results):
        self._results.set_text(results)

    def _clear_diplay(self, button):
        self._command = [0, 0, 0, 0, 0, 0, 0]
        self._display.set_text("")

    def _change_mode(self, button):

        placeholder = "Ex.: 2d6, 1d12+3, h2d20"
        
        if self._mode_button.get_active():
            self._stack.set_visible_child(self._info_area)
            self._display.set_editable(True)
            self._display.set_can_focus(True)
            self._display.set_placeholder_text(placeholder)
            self._display.grab_focus()
        
        if not self._mode_button.get_active():
            self._stack.set_visible_child(self._dice_area)
            self._display.set_editable(False)
            self._display.set_can_focus(False)
            self._display.set_placeholder_text('')

    def _assemble_command(self):

        add_plus = False
        display_content = ""

        for index, element in enumerate(self._command):
            if element != 0:
                if add_plus and index != 6:
                    display_content = display_content + ' + '

                add_plus = True

                match index:
                    case 0:
                        content = f"{element}d20"

                    case 1:
                        content = f"{element}d12"

                    case 2:
                        content = f"{element}d10"

                    case 3:
                        content = f"{element}d8"

                    case 4:
                        content = f"{element}d6"

                    case 5:
                        content = f"{element}d4"

                    case 6:
                        content = f" + {element}"

                        if element < 0:
                            content = f" - {abs(element)}"

                display_content = display_content + content

        print(display_content)
        self._display.set_text(display_content)

    def _add_elements(self, button, index):

        if index == 7:

            self._command[6] = self._command[6] - 1
            # print(self._command)
            self._assemble_command()
            return

        self._command[index] = self._command[index] + 1

        # print(self._command)
        self._assemble_command()

    def _test(self, button):
        input_command = self._display.get_text()
        results = parse_command(input_command)
        # results = command_handler(input_command)
        print(results)
