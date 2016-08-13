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

import yaml

import yamlui


def generate_ui(path):
    """Takes a path to a yaml UI definition, and generates a UI tree for it.

    :param definition: A UI definition representing the UI to be created.

    """
    with open(path, 'r') as ui_file:
        definition = yaml.safe_load(ui_file)

    root_class = yamlui.class_mapping.get(definition['object'])
    if root_class is None:
        raise Exception('ERROR: Root class is an unrecognised widget type.')

    return root_class(definition)


def parse_children(definition, widget=None):
    """Create the widgets which are children of the given widget.

    Returns a list of widgets created from the `children` list in the
    given definition.

    :param definition: The definition of the widget to parse children for.
    :param widget: The widget which will have the children.

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
        child = child_class(child_definition)
        child.parent = widget
        children.append(child)

    return children
