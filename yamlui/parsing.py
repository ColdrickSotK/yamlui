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

import importlib
import os
import uuid

import yaml

import yamlui


def parse_children(definition, widget=None, style={}):
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
        child = child_class(child_definition, style=style, parent=widget)
        children.append(child)

    return children


def get_name(widget):
    """Get a unique name for the widget.

    If the widget's properties contain `name`, then use that. Otherwise
    generate it a uuid.

    :param widget: The widget to get a name for.

    """
    return widget._properties.get('name', uuid.uuid4())


def build_dictionary(root, ui_name=None):
    """Build a dictionary containing the given widget and all its descendants.

    :param root: The root widget of the UI tree to build a dictionary for.
    :param ui_name: The name of this UI tree. If not given, the name of the
    root widget will be used.

    """
    name = ui_name or get_name(root)
    if name in yamlui.trees:
        raise Exception('Duplicate UI name')

    def add_children(widget, ui_dict):
        name = get_name(widget)
        if name in ui_dict:
            raise Exception('Duplicate widget name')

        ui_dict[get_name(widget)] = widget
        if not hasattr(widget, 'children'):
            return
        for child in widget.children:
            add_children(child, ui_dict)

    ui_dict = {get_name(root): root}
    for widget in root.children:
        add_children(widget, ui_dict)

    return ui_dict


def generate_ui(path, modules=[]):
    """Takes a path to a YAML UI definition, and generates a UI tree for it.

    :param definition: A UI definition representing the UI to be created.
    :param modules: (Optional) A list of module names which need to be
        imported in order to generate the UI tree. This should include all
        module names which define custom widgets or callbacks using
        decorators that are used in the definition.

    """
    for module in modules:
        importlib.import_module(module)

    with open(path, 'r') as ui_file:
        ui = yaml.safe_load(ui_file)

    full_style = {}
    for style_path in ui.get('include', []):
        with open(style_path, 'r') as style_file:
            style = yaml.safe_load(style_file)
        for definition in style:
            full_style[definition['name']] = definition['properties']

    definition = ui['definition']
    root_class = yamlui.class_mapping.get(definition['object'])
    if root_class is None:
        raise Exception('ERROR: Root class is an unrecognised widget type.')

    root = root_class(definition, style=full_style)
    ui_name = os.path.basename(path)
    yamlui.trees[ui_name] = build_dictionary(root, ui_name)

    return root
