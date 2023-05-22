# Copyright (C) 2023 Spencer Magnusson
# semagnum@gmail.com
# Created by Spencer Magnusson
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

if 'config' in locals():
    import importlib
    config = importlib.reload(config)

if 'node_analyzer' in locals():
    import importlib
    node_analyzer = importlib.reload(node_analyzer)

if 'operator' in locals():
    import importlib
    operator = importlib.reload(operator)

import bpy

from . import config, node_analyzer, operator

bl_info = {
    "name": 'Material Color from Nodes',
    "author": 'Spencer Magnusson',
    "version": (0, 0, 5),
    "blender": (3, 5, 0),
    "description": 'Analyze various aspects of scene to determine complexity',
    "location": 'Object Material',
    "support": 'COMMUNITY',
    "category_icon": 'Object'
}


def register():
    bpy.utils.register_class(operator.CM_OT_ObjectColorFromMaterial)


def unregister():
    bpy.utils.unregister_class(operator.CM_OT_ObjectColorFromMaterial)


if __name__ == '__main__':
    register()
