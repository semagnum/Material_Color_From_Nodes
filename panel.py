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

import bpy

from . import operator


class CM_PT_ObjectColorFromMaterial(bpy.types.Panel):
    bl_label = 'Viewport Display from Nodes'
    bl_idname = 'CM_PT_ObjectColorFromMaterial'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'material'

    def draw(self, context):
        layout = self.layout
        window_manager = context.window_manager

        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation

        col = layout.column(heading='Detect')
        col.prop(window_manager, 'cfm_analyze_metallic', text='Metallic')
        col.prop(window_manager, 'cfm_analyze_roughness', text='Roughness')

        def draw_op(layout, bl_idname, **kwargs):
            op = layout.operator(bl_idname, **kwargs)
            op.analyze_metallic = window_manager.cfm_analyze_metallic
            op.analyze_roughness = window_manager.cfm_analyze_roughness

        row = layout.row()
        draw_op(row, operator.ActiveMaterialOperator.bl_idname,
                text='Active Material', icon='MATERIAL')
        draw_op(row, operator.ActiveMaterialNodeOperator.bl_idname,
                text='Active Node', icon='NODETREE')

        draw_op(layout, operator.ActiveObjectOperator.bl_idname,
                text='Active Object', icon='OBJECT_DATA')
        draw_op(layout, operator.SelectedObjectsOperator.bl_idname,
                text='Selected Objects', icon='SCENE_DATA')
        draw_op(layout, operator.AllMaterialsOperator.bl_idname,
                text='All Materials', icon='FILE_BLEND')
