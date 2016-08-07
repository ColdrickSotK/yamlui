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


def create_group(widgets):
    """Create a pygame sprite group from a set of widgets."""
    # TODO: Do a thing with surfaces not sprites
    sprites = [widget.sprite for widget in widgets
               if widget.has_sprite]
    return pygame.sprite.Group(sprites)


def create_surface(widget, surface_class=pygame.Surface):
    """Create a surface to use when drawing this widget.

    This requires one of `image` or `colour` to be set in the definition.
    If `image` is set, then that takes precedent over any `colour` that
    is also set.

    If neither is set this function returns None. This way the widget can
    be invisible, but its children can still be displayed.

    Returns None or an instance of surface_class.

    :param widget: The Widget to create a surface for.
    :param surface_class: The class to instantiate as the surface itself.

    """
    # Set image if one is defined
    if 'image' in widget._properties:
        image = pygame.image.load(
            widget._properties['image']).convert_alpha()

    # Fall back to block colour
    elif any(key in widget._properties for key in ['colour', 'color']):
        width = widget._properties['width']
        height = widget._properties['height']
        image = pygame.Surface((width, height))
        image.fill(widget._properties.get(
            'colour', widget._properties.get('color')))

    else:
        print('WARNING: Did not set surface for container.')
        return

    # Set the opacity
    if 'opacity' in widget._properties:
        percentage = int(widget._properties['opacity'].strip('%'))
        image.set_alpha(int(255 * percentage / 100))

    if surface_class == pygame.Surface:
        surface = image
    else:
        surface = surface_class(image)

    # Set initial position
    if 'position' in widget._properties:
        surface.rect.x, surface.rect.y = widget._properties['position']

    return surface


def parse_children(definition):
    """Create the widgets which are children of the given widget.

    Returns a list of widgets created from the `children` list in the
    given definition.

    """
    child_defs = definition.get('children')
    if child_defs is None:
        return []

    children = []
    for child_definition in child_defs:
        child_class = yamlui.class_mapping.get(child_definition['object'])
        if child_class is None:
            raise Exception('No class found for %s' %
                            child_definition['object'])
        children.append(child_class(child_definition))

    return children
