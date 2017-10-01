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

    def __repr__(self):
        return self.name


class GameSetup(object):

    villagers = [Villager('Riofaal the Magnificent')]

    def __init__(self, event, widget):
        super(GameSetup, self).__init__()

    def chieftain(self, event, widget, **kwargs):
        return self.villagers[0]

    def start_game(self, event, widget, **kwargs):
        print('Start game callback was called with:')
        print(kwargs)
        return True

    def main_menu(self, event, widget, **kwargs):
        print('Main menu callback was called with:')
        print(kwargs)
        return True

    def villager_count(self, event=None, widget=None, **kwargs):
        return str(len(self.villagers))

    def add_villager(self, event, widget, **kwargs):
        if len(self.villagers) < 10:
            self.villagers.append(
                Villager('Ikadir the %dth' % len(self.villagers)))
        return True

    def remove_villager(self, event, widget, **kwargs):
        if len(self.villagers) > 1:
            self.villagers.pop()
        return True


path = 'examples/testui/newgame.yaml'
callbacks = {
    'get_setup': GameSetup
}
yamlui.callbacks.update(callbacks)

pygame.init()

window = yamlui.generate_ui(path)

while True:
    for event in pygame.event.get():
        window.handle_event(event)
    window.update()
    window.draw()
