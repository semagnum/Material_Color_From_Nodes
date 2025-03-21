# Copyright (C) 2024 Spencer Magnusson
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

if 'bpy' in locals():
    import importlib
    reloadable_modules = [
        'util',
        'node_eval',
        'custom_node_eval',
        'config',
        'operator',
        'panel'
    ]
    for module_name in reloadable_modules:
        if module_name in locals():
            importlib.reload(locals()[module_name])

import bpy

from . import config, node_eval, custom_node_eval, operator, panel, util



bl_info = {
    "name": 'Material Viewport Color from Nodes',
    "author": 'Spencer Magnusson',
    "version": (0, 1, 4),
    "blender": (3, 5, 0),
    "description": 'Sets material viewport display attributes based on the node tree',
    "location": 'Object Material Properties',
    "support": 'COMMUNITY',
    "category": 'Material'
}

addon_classes = [
    operator.AllMaterialsOperator,
    operator.ActiveObjectOperator,
    operator.SelectedObjectsOperator,
    operator.ActiveMaterialOperator,
    operator.ActiveMaterialNodeOperator,
    panel.CM_PT_ObjectColorFromMaterial,
]


def register():
    """Registers operators and properties."""

    bpy.types.WindowManager.cfm_analyze_metallic = bpy.props.BoolProperty(
        name='Detect Metallic',
        description='Detects potential values for viewport material\'s metallic property',
        default=True,
    )
    bpy.types.WindowManager.cfm_analyze_roughness = bpy.props.BoolProperty(
        name='Detect Roughness',
        description='Detects potential values for viewport material\'s roughness property',
        default=True,
    )

    for cls in addon_classes:
        bpy.utils.register_class(cls)


def unregister():
    """Unregisters operators and properties."""

    for cls in addon_classes[::-1]:
        bpy.utils.unregister_class(cls)

    del bpy.types.WindowManager.cfm_analyze_metallic
    del bpy.types.WindowManager.cfm_analyze_roughness


if __name__ == '__main__':
    register()
