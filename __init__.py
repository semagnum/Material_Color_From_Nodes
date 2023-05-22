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

if 'panel' in locals():
    import importlib
    panel = importlib.reload(panel)

import bpy

from . import config, node_analyzer, operator, panel



bl_info = {
    "name": 'Material Color from Nodes',
    "author": 'Spencer Magnusson',
    "version": (0, 0, 6),
    "blender": (3, 5, 0),
    "description": 'Analyze various aspects of scene to determine complexity',
    "location": 'Object Material',
    "support": 'COMMUNITY',
    "category_icon": 'Object'
}


def register():
    bpy.utils.register_class(operator.CM_OT_SetAllMaterialDisplayProperties)
    bpy.utils.register_class(operator.CM_OT_SetActiveObjectDisplayMaterialProperties)
    bpy.utils.register_class(operator.CM_OT_SetAllSelectedObjectsViewportDisplayMaterialProperties)
    bpy.utils.register_class(operator.CM_OT_SetActiveMaterialViewportDisplayMaterialProperties)

    bpy.utils.register_class(panel.CM_PT_ObjectColorFromMaterial)


def unregister():
    bpy.utils.unregister_class(panel.CM_PT_ObjectColorFromMaterial)

    bpy.utils.unregister_class(operator.CM_OT_SetAllMaterialDisplayProperties)
    bpy.utils.unregister_class(operator.CM_OT_SetActiveObjectDisplayMaterialProperties)
    bpy.utils.unregister_class(operator.CM_OT_SetAllSelectedObjectsViewportDisplayMaterialProperties)
    bpy.utils.unregister_class(operator.CM_OT_SetActiveMaterialViewportDisplayMaterialProperties)


if __name__ == '__main__':
    register()
