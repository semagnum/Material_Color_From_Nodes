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
from mathutils import Vector

from . import config, node_eval as node, util


def set_material(material):
    if material.use_nodes:
        node_tree = material.node_tree
        output = next(util.find_outputs(node_tree), None)

        if output is not None:
            material.diffuse_color = node.assert_color(node.get_from_node(output, config.ALBEDO_MAP,
                                                                          Vector((0.8, 0.8, 0.8, 1.0))
                                                                          ))
            material.roughness = node.assert_float(node.get_from_node(output, config.ROUGHNESS_MAP, 0.5))
            material.metallic = node.assert_float(node.get_from_node(output, config.METALLIC_MAP, 0.0))


class CM_OT_SetAllSelectedObjectsViewportDisplayMaterialProperties(bpy.types.Operator):
    """Sets all selected object's viewport display properties."""
    bl_idname = 'object.selected_objects_nodes_to_viewport'
    bl_label = 'Set Selected Objects\' Nodes To Viewport Display'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        materials = {slot.material
                     for obj in context.selected_objects
                     for slot in obj.material_slots
                     if slot.material is not None}

        for material in materials:
            set_material(material)

        return {'FINISHED'}


class CM_OT_SetActiveMaterialViewportDisplayMaterialProperties(bpy.types.Operator):
    """Sets current object's active material's viewport display properties."""
    bl_idname = 'object.active_material_nodes_to_viewport'
    bl_label = 'Active Material Nodes To Viewport Display'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object.active_material is not None and context.active_object.active_material.use_nodes

    def execute(self, context):
        set_material(context.active_object.active_material)

        return {'FINISHED'}


class CM_OT_SetActiveObjectDisplayMaterialProperties(bpy.types.Operator):
    """Sets current object's material's viewport display properties."""
    bl_idname = 'object.active_object_nodes_to_viewport'
    bl_label = 'Active Objects\' Material Nodes To Viewport Display'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        materials = {slot.material
                     for slot in context.active_object.material_slots
                     if slot.material is not None}

        for material in materials:
            set_material(material)

        return {'FINISHED'}


class CM_OT_SetAllMaterialDisplayProperties(bpy.types.Operator):
    """Sets all materials' viewport display properties."""
    bl_idname = 'object.all_material_nodes_to_viewport'
    bl_label = 'All Material Nodes To Viewport Display'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _context):
        for material in bpy.data.materials:
            set_material(material)

        return {'FINISHED'}
