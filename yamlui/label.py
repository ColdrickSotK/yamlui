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
from yamlui.fonts import arial_18pt


class LabelSurface(pygame.Surface):

    """The Surface used to represent the label on screen."""

    def __init__(self, image):
        """Initialise the surface.

        :params image: The original look of the surface.

        """
        dimensions = (image.get_rect().width, image.get_rect().height)
        super(LabelSurface, self).__init__(dimensions, flags=pygame.SRCALPHA)

        self.original = image

        self.rect = self.get_rect()
        self.blit(self.original, (0, 0))

    def render_text(self, text, font):
        # TODO(SotK): configurable colour
        self.text = font.render(text, True, (255, 255, 255, 255))
        self.blit(self.text, (0, 0))

    def draw(self, surface):
        """Blit the label onto the given surface.

        :param surface: The pygame Surface to draw on.

        """
        # TODO(SotK): Handle relative positioning
        surface.blit(self, self.rect)


class Label(object):

    """A text label widget.

    This label can contain an arbitrary string of text to display on screen.

    Example yaml definition::

        - object: label
          properties:
            text: Test Label
            colour: [0, 0, 0, 0]
            position: [20, 20]
            width: 200
            height: 20

    """

    def __init__(self, definition):
        self._properties = definition['properties']
        self._children = definition.get('children', [])

        self.state = 'idle'
        self.surface = create_surface(self, LabelSurface,
                                      alpha=pygame.SRCALPHA)
        # TODO(SotK): Configurable font
        self.surface.render_text(self._properties['text'], arial_18pt)

    def set_relative_position(self):
        x, y = self.parent.surface.rect.topleft
        dx, dy = self._properties['position']
        self.surface.rect.x = x + dx
        self.surface.rect.y = y + dy

    def draw(self, surface):
        """Draw the container and its contents on the given surface."""
        if self._properties.get('display') == 'relative' and self.parent:
            self.set_relative_position()
        self.surface.draw(surface)
