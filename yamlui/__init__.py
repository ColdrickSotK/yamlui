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

from yamlui.button import Button
from yamlui.container import Container
from yamlui.label import Label
from yamlui.parsing import generate_ui
from yamlui.textbox import TextBox
from yamlui.window import Window


class_mapping = {
    'window': Window,
    'container': Container,
    'label': Label,
    'button': Button,
    'textbox': TextBox
}

callbacks = {}
trees = {}

def get_callback(key=None, widget=None):
    if key is None:
        return None

    # First check for methods of objects bound to a direct
    # ancestor of the given widget.
    current = widget
    while current is not None:
        if (current.bound_object is not None and
                hasattr(current.bound_object, key)):
            return getattr(current.bound_object, key)
        current = current.parent

    # Otherwise, look in the callbacks dictionary
    return callbacks.get(key)
