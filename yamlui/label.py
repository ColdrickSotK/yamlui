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

from yamlui import fonts
from yamlui.util import render_text_list
from yamlui.util import wrap_text
from yamlui.widget import Widget


def create_label_surface(widget):
    font = fonts.make_font(widget._properties.get('font', 'arial'),
                           widget._properties.get('font-size', 12))

    word_wrap = widget._properties.get('wrap', False)
    width = widget._properties.get('width')
    height = widget._properties.get('height')

    if any(dimension is None for dimension in [width, height]):
        if 'text' in widget._properties:
            widget.wrapped = wrap_text(
                widget._properties['text'], font, width)
            w, h = render_text_list(widget.wrapped, font).get_size()
            if width is None:
                width = w
            if height is None:
                height = h
        else:
            if width is None:
                width = 0
            if height is None:
                height = 0

    if any(key in widget._properties for key in ['colour', 'color']):
        background = widget._properties.get(
            'colour', widget._properties.get('color'))
        image = pygame.Surface((width, height))
        image.fill(background)
        if 'opacity' in widget._properties:
            percentage = int(widget._properties['opacity'].strip('%'))
            image.set_alpha(int(255 * percentage / 100))
        image = image.convert_alpha()
    else:
        image = pygame.Surface((width, height)).convert_alpha()
        image.fill((0, 0, 0, 0))

    surface = LabelSurface(image)

    if 'position' in widget._properties:
        surface.rect.x, surface.rect.y = widget._properties['position']

    return surface


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

    def draw_text(self, text):
        self.blit(text, (0, 0))

    def draw(self, surface):
        """Blit the label onto the given surface.

        :param surface: The pygame Surface to draw on.

        """
        surface.blit(self, self.rect)


class Label(Widget):

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
        super(Label, self).__init__(definition)

        self.state = 'idle'
        self.surface = create_label_surface(self)
        self.render_text()
        self.surface.draw_text(self.rendered_text)

    def render_text(self):
        font = fonts.make_font(self._properties.get('font', 'arial'),
                               self._properties.get('font-size', 12))
        if not hasattr(self, 'wrapped'):
            self.wrapped = wrap_text(self._properties['text'],
                                     font,
                                     self._properties.get('width'))
        colour = self._properties.get('font-colour',
            self._properties.get('font-color', (255, 255, 255)))
        self.rendered_text = render_text_list(self.wrapped, font, colour)

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
