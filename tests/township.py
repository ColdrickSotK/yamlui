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


class Villager(object):
    def __init__(self, name):
        self.name = name

path = 'examples/testui/newgame.yaml'
villagers = [Villager('')]

def start_game(event, widget, **kwargs):
    print('Start game callback was called with:')
    print(kwargs)
    return True


def main_menu(event, widget, **kwargs):
    print('Main menu callback was called with:')
    print(kwargs)
    return True


def villager_count(event=None, widget=None, **kwargs):
    return str(len(villagers))


def add_villager(event, widget, **kwargs):
    if len(villagers) < 10:
        villagers.append(Villager('Ikadir the %dth' % len(villagers)))
    return True


def remove_villager(event, widget, **kwargs):
    if len(villagers) > 1:
        villagers.pop()
    return True


callbacks = {
    'start_game': start_game,
    'main_menu': main_menu,
    'villager_count': villager_count,
    'add_villager': add_villager,
    'remove_villager': remove_villager
}
yamlui.callbacks.update(callbacks)

pygame.init()

window = yamlui.generate_ui(path)

while True:
    for event in pygame.event.get():
        window.handle_event(event)
    window.update()
    window.draw()
