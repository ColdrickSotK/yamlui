#/usr/bin/env python
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
import yaml

import yamlui


pygame.init()

with open('examples/minimal.yaml', 'r') as f:
    window = yamlui.Window(yaml.load(f))

running = True
while running:
    for event in pygame.event.get():
        window.handle_event(event)
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_d:
            window.children[0].state = 'drag'
        elif event.type == pygame.KEYUP and event.key == pygame.K_a:
            window.children[0].state = 'idle'

    window.update()
    window.draw()
