#!/usr/bin/env python
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


def start_game(event, **kwargs):
    print('Start game callback was called with:')
    print(kwargs)
    return True


def main_menu(event, **kwargs):
    print('Main menu callback was called with:')
    print(kwargs)
    return True


callbacks = {
    'start_game': start_game,
    'main_menu': main_menu
}
yamlui.callbacks.update(callbacks)

pygame.init()

window = yamlui.generate_ui('examples/testui.yaml')

while True:
    for event in pygame.event.get():
        window.handle_event(event)
    window.update()
    window.draw()
