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

if not pygame.font.get_init():
    pygame.font.init()

_font_cache = {}

def make_font(name, size):
    cache_name = '%s_%d' % (name, size)
    if cache_name in _font_cache:
        return _font_cache[cache_name]

    try:
        font = pygame.font.Font(name, size)
    except IOError:
        font = pygame.font.SysFont(name, size)
    _font_cache[cache_name] = font
    return font
