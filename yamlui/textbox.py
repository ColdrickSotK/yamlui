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

import string

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

    def redraw(self, content=None):
        """Redraw the original image."""
        self.fill((0, 0, 0, 0))
        self.blit(self.original, (0, 0))
        if content is not None:
            self.draw_content(content)

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

    def __init__(self, definition, style={}, parent=None):
        super(TextBox, self).__init__(definition, style=style, parent=parent)

        self.state = 'idle'
        self.bound = False
        self.old_content = None
        self.content = ''
        if 'content-bind' in self._properties:
            self.bound = 'one-way'
            self.bound_content = yamlui.get_callback(
                self._properties['content-bind'], self)
            if callable(self.bound_content):
                self.content = self.bound_content()
            else:
                self.content = self.bound_content
                self.bound = 'two-way'

        self.focus = False
        self.valid = string.ascii_letters + string.digits + \
                     string.punctuation + ' '
        self.timer = 0
        self.blink = False
        self.rendered = self.render_text()

        self.surface = util.create_surface(self, TextBoxSurface)
        self.hover_surface = util.create_surface(
            self, TextBoxSurface,
            properties=self._properties.get('hover-effects'))
        self.focus_surface = util.create_surface(
            self, TextBoxSurface,
            properties=self._properties.get('focus-effects'))
        self.redraw_text()

    def _collide(self, point):
        return self.surface.rect.collidepoint(point)

    def redraw_text(self):
        self.surface.redraw(self.rendered)
        self.hover_surface.redraw(self.rendered)
        self.focus_surface.redraw(self.rendered)

    def handle_input(self, event):
        if event.unicode in self.valid:
            self.content += event.unicode
            if self.bound == 'two-way':
                yamlui.two_way_callback(
                    self._properties['content-bind'], self,
                    'set', self.content)
            self.rendered = self.render_text()
        elif event.key == pygame.K_BACKSPACE:
            self.content = self.content[:-1]
            if self.bound == 'two-way':
                yamlui.two_way_callback(
                    self._properties['content-bind'], self,
                    'set', self.content)
            self.rendered = self.render_text()
            self.state = 'deleting'
        elif event.key == pygame.K_ESCAPE:
            self.state = 'idle'
            self.focus = False
        self.redraw_text()

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
        elif event.type == pygame.KEYDOWN and self.focus:
            self.handle_input(event)
            return True
        elif event.type == pygame.KEYUP and self.focus:
            if event.key == pygame.K_BACKSPACE:
                self.state = 'focused'
                return True
            return False
        return False

    def render_text(self):
        font = fonts.make_font(self._properties.get('font', 'arial'),
                               self._properties.get('font-size', 12))
        colour = self._properties.get('font-colour',
            self._properties.get('font-color', (0, 0, 0)))
        return util.render_text_list([self.content], font, colour)

    def update(self):
        if pygame.time.get_ticks() - self.timer > 750:
            self.blink = not self.blink
            self.timer = pygame.time.get_ticks()
            self.focus_surface.redraw(self.rendered)

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
            colour = self._properties.get('font-colour',
                self._properties.get('font-color', (0, 0, 0)))
            if self.blink:
                if self.rendered is None:
                    self.focus_surface.fill(colour,
                        (7, 5, 1, self.focus_surface.get_height() - 10))
                else:
                    self.focus_surface.fill(colour,
                        (self.rendered.get_rect().right + 7, 5, 1,
                         self.rendered.get_rect().height))
        elif self._collide(pygame.mouse.get_pos()) or self.state == 'click':
            self.hover_surface.draw(surface)
        else:
            self.surface.draw(surface)
