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
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption('Minimal UI test')

with open('examples/minimal.yaml', 'r') as f:
    state = yaml.load(f)

elements = []
for element in state:
    if element['object'] == 'container':
        elements.append(yamlui.Container(element))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_d:
            elements[0].state = 'drag'
        elif event.type == pygame.KEYUP and event.key == pygame.K_a:
            elements[0].state = 'idle'

    screen.fill((255, 255, 255))
    for element in elements:
        element.update()
        element.draw(screen)

    pygame.display.flip()
