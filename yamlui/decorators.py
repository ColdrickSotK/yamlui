# Copyright (c) 2018 Adam Coldrick
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


"""Convenience decorators to automate population of yamlui dictionaries.

yamlui has some dictionaries which are used when parsing definitions, mapping
strings in the YAML definition to callable objects, either widget types,
callback functions, or bindable classes for use with ``bind-object``.

"""


import yamlui


def callback(name):
    """Return a decorator to indicate the decorated object is a callback.

    This function returns a decorator used to decorate a callback function
    which is used in a YAML definition. It takes a name parameter, which is
    the name used to refer to the function in a definition.

    This function can also be used to decorate a class intended for use with
    ``bind-object``. At the moment there is no separate decorator for that
    type of callback.

    :param name: The callback name to map to the decorated function for use
        within YAML definitions.
    :returns: A decorator which registers the callback with yamlui's internal
        representation of available callbacks.

    """
    def _decorator(fn):
        yamlui.callbacks[name] = fn
        return fn
    return _decorator


def widget(name):
    """Return a decorator to indicate the decorated object is a widget.

    This function returns a decorator used to decorate a custom widget class
    which is used in a YAML definition. It takes a name parameter, which is
    the name used to refer to the class in a definition.

    The decorated class does not need to be a subclass of ``yamlui.Widget``,
    providing it implements the same interface. However, use like this is not
    recommended.

    :param name: The callback name to map to the decorated widget type for use
        within YAML definitions.
    :returns: A decorator which registers the callback with yamlui's internal
        representation of available widget types.

    """
    def _decorator(fn):
        yamlui.class_mapping[name] = fn
        return fn
    return _decorator
