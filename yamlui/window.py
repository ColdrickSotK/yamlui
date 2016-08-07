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

import sys

import pygame

from yamlui.util import create_surface, parse_children


class Window(object):

    """A window to display on screen.

    This window is the place where the rest of the UI is drawn.

    Example yaml definition::

        - object: window
          properties:
            text: Window Title
            colour: [255, 255, 255]
            width: 400
            height: 600
          children:
          - object: container
            properties:
              opacity: 75%
              colour: [0, 0, 0]
              position: [10, 10]
              width: 380
              height: 580

    """

    def __init__(self, definition):
        self._properties = definition['properties']
        self._children = definition.get('children', [])

        self.state = 'idle'
        dimensions = [self._properties.get('width', 1000),
                      self._properties.get('height', 500)]
        self.surface = pygame.display.set_mode(dimensions)
        pygame.display.set_caption(self._properties['text'])

        self.image = create_surface(self)
        self.children = parse_children(definition)

    def handle_event(self, event):
        """Handle an event that occurred in the window."""
        # TODO: Handle passing events through to children
        if event.type == pygame.QUIT:
            sys.exit(0)

    def update(self):
        """Update the window, and all its child widgets."""
        for widget in self.children:
            widget.update()

    def draw(self):
        """Draw the window and its contents, then refresh the display."""
        self.surface.blit(self.image, (0, 0))
        for widget in self.children:
            widget.draw(self.surface)

        pygame.display.flip()
