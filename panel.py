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

        layout.operator(operator.CM_OT_SetActiveMaterialViewportDisplayMaterialProperties.bl_idname,
                        text='Active Material', icon='MATERIAL')
        layout.operator(operator.CM_OT_SetActiveObjectDisplayMaterialProperties.bl_idname,
                        text='Active Object', icon='OBJECT_DATA')
        layout.operator(operator.CM_OT_SetAllSelectedObjectsViewportDisplayMaterialProperties.bl_idname,
                        text='All Selected Objects', icon='SCENE_DATA')
        layout.operator(operator.CM_OT_SetAllMaterialDisplayProperties.bl_idname,
                        text='All Materials', icon='FILE_BLEND')
