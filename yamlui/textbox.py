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

import yamlui
from yamlui import fonts
from yamlui import util
from yamlui.widget import Widget


class TextBoxSurface(pygame.Surface):

    """The Surface used to represent the text box on screen."""

    def __init__(self, image):
        """Initialise the surface.

        :param image: The original look of the surface.

        """
        super(TextBoxSurface, self).__init__(image.get_size(),
                                             flags=pygame.SRCALPHA)
        self.original = image.convert_alpha()
        self.rect = self.get_rect()
        self.blit(self.original, (0, 0))

    def draw_content(self, content):
        """Blit the content of the text box.

        :param content: The surface containing the content.

        """
        y = (self.rect.height - content.get_height()) / 2
        self.blit(content, (5, y))

    def reset(self):
        """Redraw the original image."""
        self.blit(self.original, (0, 0))

    def draw(self, surface):
        """Blit the button onto the given surface.

        :param surface: The pygame Surface to draw on.

        """
        surface.blit(self, self.rect)


class TextBox(Widget):

    """A text box widget.

    This text box can contain an arbitrary string of text which is input
    by the user.

    Example yaml definition::

        - object: textbox
          properties:
            colour: [255, 255, 255]
            opacity: 50%
            position: [10, 10]
            display: relative
            width: 200
            height: 20
          hover-effects:
            opacity: 75%
          focus-effects:
            opacity: 100%

    """

    def __init__(self, definition):
        super(TextBox, self).__init__(definition)

        self.state = 'idle'
        self.focus = False
        self.content = ''

        self.surface = util.create_surface(self, TextBoxSurface)
        self.hover_surface = util.create_surface(
            self, TextBoxSurface,
            properties=self._properties.get('hover-effects'))
        self.focus_surface = util.create_surface(
            self, TextBoxSurface,
            properties=self._properties.get('focus-effects'))

    def _collide(self, point):
        return self.surface.rect.collidepoint(point)

    def handle_event(self, event):
        """Handle an event."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.state == 'idle':
                if not self._collide(pygame.mouse.get_pos()):
                    return False
                self.state = 'click'
                return True
            elif self.focus:
                if self._collide(pygame.mouse.get_pos()):
                    return True
            return False
        elif event.type == pygame.MOUSEBUTTONUP:
            if not self._collide(pygame.mouse.get_pos()):
                self.state = 'idle'
                self.focus = False
                return False
            if self.state == 'click':
                self.state = 'focused'
                self.focus = True
                return False
            elif self.state == 'focused':
                return True
            return False
        return False

    def set_relative_position(self):
        x, y = self.parent.surface.rect.topleft
        dx, dy = self._properties['position']
        self.surface.rect.x = x + dx
        self.surface.rect.y = y + dy
        self.hover_surface.rect.x = x + dx
        self.hover_surface.rect.y = y + dy
        self.focus_surface.rect.x = x + dx
        self.focus_surface.rect.y = y + dy

    def draw(self, surface):
        """Draw the button onto the given surface.

        :param surface: The surface to draw on.

        """
        if self._properties.get('display') == 'relative' and self.parent:
            self.set_relative_position()

        if self.focus:
            self.focus_surface.draw(surface)
        elif self._collide(pygame.mouse.get_pos()) or self.state == 'click':
            self.hover_surface.draw(surface)
        else:
            self.surface.draw(surface)