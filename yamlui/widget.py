# Copyright (c) 2016 Adam Coldrick
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygame


class Widget(object):

    """Base class which all UI widgets inherit from."""

    def __init__(self, definition):
        self._properties = definition['properties']
        self._childredn = definition.get('children', [])
        self._cb_args = definition.get('callback-args', {})

    def handle_event(self, event):
        """Handle an event that has occurred somewhere.

        This is not implemented here, and should be overridden in subclasses
        to correctly handle events relevant to themselves.

        :param event: The event that has occurred.
        :returns: True if event is handled by this function, False otherwise.

        """
        return False

    def update(self):
        """Update the widget.

        Not implemented here, subclasses should override this to be useful.

        """
        pass

    def draw(self):
        """Draw the widget.

        Not implemented here, subclasses should override this to be useful.

        """
        pass
