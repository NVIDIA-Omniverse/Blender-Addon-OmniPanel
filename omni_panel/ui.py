# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.

import bpy
from .particle_bake.operators import*
from .material_bake.background_bake import bgbake_ops
from os.path import join, dirname
import bpy.utils.previews


def get_icons_directory():

    icons_directory = join(dirname(__file__), "icons")
    return icons_directory

class OBJECT_PT_omni_bake_panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "OMNI"
    bl_label = "NVIDIA OMNIVERSE"
    
    current = True
    version = "0.0.0"

    """
    @classmethod
    def poll(cls, context):
        return (context.object is not None)
    """

    icons = bpy.utils.previews.new()
    icons_directory = get_icons_directory()
    icons.load("OMNIBLEND", join(icons_directory, "BlenderOMNI.png"), 'IMAGE')
    icons.load("OMNI", join(icons_directory, "ICON.png"), 'IMAGE')
    icons.load("BAKE",join(icons_directory, "Oven.png"), 'IMAGE')


    def draw(self, context):
        
        layout = self.layout

        #--------File Handling-------------------
        layout.label(text="Omniverse", icon_value=self.icons["OMNI"].icon_id)

        impExpCol = self.layout.column(align=True)
        impExpCol.label(text= "File Handling",
            icon='FILEBROWSER')
        impExpCol.operator('wm.usd_import',
           text='Import USD',
           icon='IMPORT')
        impExpCol.operator('wm.usd_export',
           text='Export USD',
           icon='EXPORT')

        #--------Particle Collection Instancing-------------------
        layout.separator()
        mytool = context.scene.my_tool

        particleCol = self.layout.column(align=True)
        particleCol.label(text = "Omni Particles",
            icon='PARTICLES')
        box = particleCol.box()
        column= box.column(align= True)
        column.prop(mytool, "deletePSystemAfterBake")

        row = column.row()
        row.prop(mytool, "animateData")
        if mytool.animateData:
            row = column.row(align=True)
            row.prop(mytool, "selectedStartFrame")
            row.prop(mytool, "selectedEndFrame")
            # print(mytool.selectedStartFrame)
            # if mytool.selectedStartFrame > mytool.selectedEndFrame:
            #     print("Go Time")
            #     fixEndFrame()
            row = column.row()
            row.enabled = False
            row.label(text="Increased Calculation Time", icon= 'ERROR')
        
        row = column.row()
        row.scale_y = 1.5
        row.operator('omni.hair_bake',
           text='Convert',
           icon='MOD_PARTICLE_INSTANCE')

        # row = column.row()
        # row.scale_y = 1.2
        # row.prop(mytool, "progressBar")

        #--------PBR Bake Settings-------------------
        layout.separator()
        column = layout.column(align= True)
        header = column.row()
        header.label(text = "Material Bake", icon = 'UV_DATA')
        box = column.box()

        if(context.scene.omnibake_global_mode == "pbr_bake"):
            
            row = box.row()
            if context.scene.all_maps == True:
                row.prop(context.scene, "all_maps", icon = 'CHECKBOX_HLT')

            
            if context.scene.all_maps == False:
                row.prop(context.scene, "all_maps", icon = 'CHECKBOX_DEHLT')

                column = box.column(align= True)
                row = column.row()
                
                row.prop(context.scene, "selected_col")
                row.prop(context.scene, "selected_metal")
                
                row = column.row()
                row.prop(context.scene, "selected_sss")
                row.prop(context.scene, "selected_ssscol")
                
                row = column.row()
                row.prop(context.scene, "selected_rough")
                row.prop(context.scene, "selected_normal")
                
                row = column.row()
                row.prop(context.scene, "selected_trans")
                row.prop(context.scene, "selected_transrough")
                row = column.row()
                row.prop(context.scene, "selected_emission")
                row.prop(context.scene, "selected_specular")
                row = column.row()
                row.prop(context.scene, "selected_alpha")
                row = column.row()
            
            colm = box.column(align=True)
            colm.prop(context.scene, "more_shaders")
            row = colm.row()
            row.enabled = False
            if context.scene.more_shaders:
                row.label(text="Inconsistent Results", icon= 'ERROR')
        
        #--------Texture Settings-------------------
        
        row = box.row()
        row.label(text="Texture Resolution:")
        row.scale_y = 0.5 
        row = box.row()
        row.prop(context.scene, "texture_res", expand=True)
        row.scale_y = 1 
        if context.scene.texture_res == "8k" or context.scene.texture_res == "4k":
            row = box.row()
            row.enabled = False
            row.label(text="Long Bake Times", icon= 'ERROR')
        
        #--------UV Settings-------------------
        elif not context.scene.tex_per_mat:
            column = box.column(align = True)
            row = column.row()
            row.prop(context.scene, "newUVoption")
            row.prop(context.scene, "unwrapmargin")
        else:
            row = box.row()
            row.prop(context.scene, "expand_mat_uvs")
        
        #--------Other Settings-------------------

        column= box.column(align=True)
        row = column.row()
        if bpy.context.scene.bgbake == "fg":
            text = "Copy objects and apply bakes"
        else:
            text = "Copy objects and apply bakes (after import)"
        
        row.prop(context.scene, "prepmesh", text=text)
        if context.scene.tex_per_mat:
            row.enabled = False
        
        if (context.scene.prepmesh == True):
            if bpy.context.scene.bgbake == "fg":
                text = "Hide source objects after bake"
            else:
                text = "Hide source objects after bake (after import)"
            row = column.row()
            row.prop(context.scene, "hidesourceobjects", text=text)
        
        #-------------Buttons-------------------------
        
        row = box.row()
        row.scale_y = 1.5
        row.operator("object.omni_bake_mapbake", icon_value=self.icons["BAKE"].icon_id)
        
        row = column.row()
        row.scale_y = 1
        row.prop(context.scene, "bgbake", expand=True)         

        if context.scene.bgbake == "bg":
            row = column.row(align= True) 
            
            # - BG status button
            col = row.column()
            if len(bgbake_ops.bgops_list) == 0:
                enable = False
                icon = "TIME"
            else:
                enable = True
                icon = "TIME"
                    
            col.operator("object.omni_bake_bgbake_status", text="", icon=icon)
            col.enabled = enable
            
            # - BG import button
            
            col = row.column()
            if len(bgbake_ops.bgops_list_finished) != 0:
                enable = True
                icon = "IMPORT"
            else:
                enable = False
                icon = "IMPORT"
            
            col.operator("object.omni_bake_bgbake_import", text="", icon=icon)
            col.enabled = enable
            
            #BG erase button
            
            col = row.column()
            if len(bgbake_ops.bgops_list_finished) != 0:
                enable = True
                icon = "TRASH"
            else:
                enable = False
                icon = "TRASH"
            
            col.operator("object.omni_bake_bgbake_clear", text="", icon=icon)
            col.enabled = enable       
            
            row.alignment = 'CENTER'
            row.label(text=f"Running {len(bgbake_ops.bgops_list)} | Finished {len(bgbake_ops.bgops_list_finished)}")

        #-------------Other material options-------------------------
        if len(bpy.context.selected_objects) != 0 and bpy.context.active_object.select_get() and bpy.context.active_object.type == "MESH":
            layout.separator()

            column= layout.column(align= True)
            column.label(text= "Convert Material to:", icon= 'SHADING_RENDERED')
            box = column.box()

            materialCol = box.column(align=True)
            materialCol.operator('universalmaterialmap.create_template_omnipbr',
                text='OmniPBR')
            materialCol.operator('universalmaterialmap.create_template_omniglass',
                text='OmniGlass')
    

class OmniBakePreferences(bpy.types.AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__

    apikey: bpy.props.StringProperty(name="Sketchfab API Key: ")
    img_name_format: bpy.props.StringProperty(name="Image format string",
        default="%OBJ%_%BATCH%_%BAKEMODE%_%BAKETYPE%")
    
    justupdated = False
    
    #Aliases
    diffuse_alias: bpy.props.StringProperty(name="Diffuse", default="diffuse")
    metal_alias: bpy.props.StringProperty(name="Metal", default="metalness")
    roughness_alias: bpy.props.StringProperty(name="Roughness", default="roughness")
    glossy_alias: bpy.props.StringProperty(name="Glossy", default="glossy")
    normal_alias: bpy.props.StringProperty(name="Normal", default="normal")
    transmission_alias: bpy.props.StringProperty(name="Transmission", default="transparency")
    transmissionrough_alias: bpy.props.StringProperty(name="Transmission Roughness", default="transparencyroughness")
    clearcoat_alias: bpy.props.StringProperty(name="Clearcost", default="clearcoat")
    clearcoatrough_alias: bpy.props.StringProperty(name="Clearcoat Roughness", default="clearcoatroughness")
    emission_alias: bpy.props.StringProperty(name="Emission", default="emission")
    specular_alias: bpy.props.StringProperty(name="Specular", default="specular")
    alpha_alias: bpy.props.StringProperty(name="Alpha", default="alpha")    
    sss_alias: bpy.props.StringProperty(name="SSS", default="sss")
    ssscol_alias: bpy.props.StringProperty(name="SSS Colour", default="ssscol")

    @classmethod
    def reset_img_string(self):
        prefs = bpy.context.preferences.addons[__package__].preferences
        prefs.property_unset("img_name_format")
        bpy.ops.wm.save_userpref()