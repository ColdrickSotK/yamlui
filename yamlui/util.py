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


def create_surface(widget, surface_class=pygame.Surface, alpha=0,
                   properties=None):
    """Create a surface to use when drawing this widget.

    This requires one of `image` or `colour` to be set in the definition.
    If `image` is set, then that takes precedent over any `colour` that
    is also set.

    If neither is set this function returns None. This way the widget can
    be invisible, but its children can still be displayed.

    Returns None or an instance of surface_class.

    :param widget: The Widget to create a surface for.
    :param surface_class: The class to instantiate as the surface itself.
    :param alpha: The alpha mode to use for the surface.
    :param properties: The properties dict for this widget.

    """
    if properties is not None:
        temp = widget._properties
        temp.update(properties)
        properties = temp
    else:
        properties = widget._properties

    # Set image if one is defined
    if 'image' in properties:
        image = pygame.image.load(properties['image']).convert_alpha()

    # Fall back to block colour
    elif any(key in properties for key in ['colour', 'color']):
        width = properties['width']
        height = properties['height']
        background = properties.get('colour', properties.get('color'))
        if len(background) < 4 and alpha == pygame.SRCALPHA:
            background.append(255)
        image = pygame.Surface((width, height), flags=alpha)
        image.fill(background)

    else:
        print properties
        print('WARNING: Did not set surface for %s' % properties['name'])
        return

    # Set the opacity
    if 'opacity' in properties:
        percentage = int(properties['opacity'].strip('%'))
        image.set_alpha(int(255 * percentage / 100))

    if surface_class == pygame.Surface:
        surface = image
    else:
        surface = surface_class(image)

    # Set initial position
    if 'position' in properties:
        surface.rect.x, surface.rect.y = properties['position']

    return surface


def wrap_text(text, font, width):
    """Wrap text to fit inside a given width when rendered.

    :param text: The text to be wrapped.
    :param font: The font the text will be rendered in.
    :param width: The width to wrap to.

    """
    text_lines = text.replace('\t', '    ').split('\n')
    if width is None or width == 0:
        return text_lines

    wrapped_lines = []
    for line in text_lines:
        line = line.rstrip() + ' '
        if line == ' ':
            wrapped_lines.append(line)
            continue

        # Get the leftmost space ignoring leading whitespace
        start = len(line) - len(line.lstrip())
        start = line.index(' ', start)
        while start + 1 < len(line):
            # Get the next potential splitting point
            next = line.index(' ', start + 1)
            if font.size(line[:next])[0] <= width:
                start = next
            else:
                wrapped_lines.append(line[:start])
                line = line[start+1:]
                start = line.index(' ')
        line = line[:-1]
        if line:
            wrapped_lines.append(line)
    return wrapped_lines


def render_text_list(lines, font, colour=(255, 255, 255)):
    """Draw multiline text to a single surface with a transparent background.

    Draw multiple lines of text in the given font onto a single surface
    with no background colour, and return the result.

    :param lines: The lines of text to render.
    :param font: The font to render in.
    :param colour: The colour to render the font in, default is white.

    """
    rendered = [font.render(line, True, colour).convert_alpha()
                for line in lines]

    line_height = font.get_linesize()
    width = max(line.get_width() for line in rendered)
    tops = [int(round(i * line_height)) for i in range(len(rendered))]
    height = tops[-1] + font.get_height()

    surface = pygame.Surface((width, height)).convert_alpha()
    surface.fill((0, 0, 0, 0))
    for y, line in zip(tops, rendered):
        surface.blit(line, (0, y))

    return surface
