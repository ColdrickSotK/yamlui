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

from yamlui.util import create_surface
from yamlui.parsing import parse_children


class ContainerSurface(pygame.Surface):

    """The Surface used to represent the container on screen."""

    def __init__(self, image):
        """Initialise the sprite.

        :params image: The original look of the surface.

        """
        dimensions = (image.get_rect().width, image.get_rect().height)
        super(ContainerSurface, self).__init__(dimensions)

        self.original = image

        self.rect = self.get_rect()
        self.set_alpha(image.get_alpha())
        self.blit(self.original, (0, 0))

    def draw(self, surface):
        """Blit the container onto the given surface.

        :param surface: The pygame Surface to draw on.

        """
        # TODO(SotK): Handle relative positioning
        surface.blit(self, self.rect)


class Container(object):

    """A container to hold a set of widgets.

    This container can contain an arbitrary set of widgets to
    display on screen. Containers can be nested as much as
    required.

    Example yaml definition::

        - object: container
          properties:
            opacity: 75%
            colour: (0, 0, 0)
            position: (10, 10)
            width: 100
            height: 100
          children:
          - object: label
            properties:
              text: Test Label
              position: (10, 10)
              display: relative

    """

    def __init__(self, definition):
        self._properties = definition['properties']
        self._children = definition.get('children', [])

        self.state = 'idle'
        self.surface = create_surface(self, ContainerSurface)
        self.children = parse_children(definition, self)

    def handle_event(self, event):
        """Handle an event."""
        handled = False
        for child in self.children:
            try:
                handled = child.handle_event(event)
            except AttributeError:
                pass
            if handled:
                return handled

        if not handled:
            if self.surface.rect.collidepoint(pygame.mouse.get_pos()) > 0:
                if event.type == pygame.MOUSEBUTTONDOWN and self.state == 'idle':
                    self.state = 'drag'
                    return True
                elif event.type == pygame.MOUSEBUTTONUP and self.state != 'idle':
                    self.state = 'idle'
                    return True
                return False

    def update(self):
        """Update the container and its contents."""
        if self.state == 'dragging':
            dx, dy = pygame.mouse.get_rel()
            self.surface.rect.x += dx
            self.surface.rect.y += dy
        elif self.state == 'drag':
            pygame.mouse.get_rel()
            self.state = 'dragging'

    def draw(self, surface):
        """Draw the container and its contents on the given surface."""
        self.surface.draw(surface)

        for child in self.children:
            child.draw(surface)
