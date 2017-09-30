# Copyright (c) 2016-17 Adam Coldrick
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
import six


def update_properties(properties, updated):
    """Update a properties dict with some given values.

    :param properties: The properties dict to update.
    :param updated: The updated values to be applied.

    """
    for key, value in six.iteritems(updated):
        if key not in properties:
            properties[key] = value
            continue
        if isinstance(value, dict):
            properties[key].update(value)
        elif isinstance(value, list):
            properties[key].append(value)
        else:
            properties[key] = value
    return properties


class Widget(object):

    """Base class which all UI widgets inherit from."""

    def __init__(self, definition, style={}, parent=None):
        resolved_properties = {}
        for name in definition.get('style', []):
            resolved_properties = update_properties(
                resolved_properties, style.get(name, {}))
        resolved_properties = update_properties(
            resolved_properties, definition.get('properties', {}))

        self._properties = resolved_properties
        self._children = definition.get('children', [])
        self._cb_args = definition.get('callback-args', {})

        self.parent = parent
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
