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


class ButtonSurface(pygame.Surface):

    """The Surface used to represent the button on screen."""

    def __init__(self, image):
        """Initialise the surface.

        :param image: The original look of the surface.

        """
        super(ButtonSurface, self).__init__(image.get_size(),
                                            flags=pygame.SRCALPHA)
        self.original = image.convert_alpha()
        self.rect = self.get_rect()
        self.blit(self.original, (0, 0))

    def draw_content(self, content):
        """Blit the content of the button.

        :param content: The surface containing the content.

        """
        x = (self.rect.width - content.get_width()) / 2
        y = (self.rect.height - content.get_height()) / 2
        self.blit(content, (x, y))

    def draw(self, surface):
        """Blit the button onto the given surface.

        :param surface: The pygame Surface to draw on.

        """
        surface.blit(self, self.rect)


class Button(Widget):

    """A button widget.

    This button can contain an arbitrary string of text, and or an
    image. It normally does something when clicked on.

    Example yaml definition::

        - object: button
          properties:
            text: Start Game
            colour: [127, 127, 127]
            position: [70, 100]
            width: 200
            height: 20

    """

    def __init__(self, definition):
        super(Button, self).__init__(definition)

        self.state = 'idle'
        self.surface = util.create_surface(self, ButtonSurface)
        self.hover_surface = util.create_surface(
            self, ButtonSurface,
            properties=self._properties.get('hover-effects'))
        self.render_content()
        self.surface.draw_content(self.rendered_content)
        self.hover_surface.draw_content(self.rendered_content)

    def _render_text(self):
        font = fonts.make_font(self._properties.get('font', 'arial'),
                               self._properties.get('font-size', 12))
        if not hasattr(self, 'wrapped'):
            self.wrapped = util.wrap_text(self._properties['text'],
                                          font,
                                          self._properties.get('width'))
        colour = self._properties.get('font-colour',
            self._properties.get('font-color', (255, 255, 255)))
        return util.render_text_list(self.wrapped, font, colour)

    def render_content(self):
        if 'content-image' in self._properties:
            self.rendered_content = pygame.image.load(
                self._properties['content-image']).convert_alpha()
        elif 'text' in self._properties:
            self.rendered_content = self._render_text()

    def handle_event(self, event):
        """Handle an event."""
        if event.type == pygame.MOUSEBUTTONDOWN and self.state == 'idle':
            if not self.surface.rect.collidepoint(pygame.mouse.get_pos()):
                return False
            self.state = 'clicking'
            return True
        elif event.type == pygame.MOUSEBUTTONUP and self.state == 'clicking':
            if not self.surface.rect.collidepoint(pygame.mouse.get_pos()):
                self.state = 'idle'
                return False
            cb = yamlui.get_callback(self._properties.get('on-click'))
            if cb is None:
                return False
            self.state = 'idle'
            return cb(event, self, **self._cb_args)
        return False

    def set_relative_position(self):
        x, y = self.parent.surface.rect.topleft
        dx, dy = self._properties['position']
        self.surface.rect.x = x + dx
        self.surface.rect.y = y + dy
        self.hover_surface.rect.x = x + dx
        self.hover_surface.rect.y = y + dy

    def draw(self, surface):
        """Draw the button onto the given surface.

        :param surface: The surface to draw on.

        """
        if self._properties.get('display') == 'relative' and self.parent:
            self.set_relative_position()

        if self.surface.rect.collidepoint(pygame.mouse.get_pos())\
                or self.state == 'clicking':
            self.hover_surface.draw(surface)
        else:
            self.surface.draw(surface)
