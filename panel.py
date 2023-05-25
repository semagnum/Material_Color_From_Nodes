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

from . import operator


class CM_PT_ObjectColorFromMaterial(bpy.types.Panel):
    bl_label = 'Viewport Display from Nodes'
    bl_idname = 'CM_PT_ObjectColorFromMaterial'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'material'

    def draw(self, _context):
        layout = self.layout

        row = layout.row()
        row.operator(operator.CM_OT_SetActiveMaterialViewportDisplayMaterialProperties.bl_idname,
                     text='Active Material', icon='MATERIAL')
        row.operator(operator.CM_OT_SetMaterialDisplayPropertiesFromActiveNode.bl_idname,
                     text='Active Node', icon='NODETREE')

        layout.operator(operator.CM_OT_SetActiveObjectDisplayMaterialProperties.bl_idname,
                        text='Active Object', icon='OBJECT_DATA')
        layout.operator(operator.CM_OT_SetAllSelectedObjectsViewportDisplayMaterialProperties.bl_idname,
                        text='Selected Objects', icon='SCENE_DATA')
        layout.operator(operator.CM_OT_SetAllMaterialDisplayProperties.bl_idname,
                        text='All Materials', icon='FILE_BLEND')
