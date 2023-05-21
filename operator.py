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

import bpy

from . import config, node_analyzer as node


class CM_OT_ObjectColorFromMaterial(bpy.types.Operator):
    """Sets object color based on material."""
    bl_idname = 'object.color_from_material'
    bl_label = 'Object Color From Material'
    bl_description = 'Sets material viewport color based on material'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.selected_objects:
            for slot in obj.material_slots:
                material = slot.material

                if material.use_nodes:
                    node_tree = material.node_tree
                    output = next(node.find_outputs(node_tree), None)

                    if output is not None:
                        material.diffuse_color = node.find_color(output)
                        material.roughness = node.find_float(output, config.ROUGHNESS_MAP, 0.5)
                        material.metallic = node.find_float(output, config.METALLIC_MAP, 0.0)

        return {'FINISHED'}
