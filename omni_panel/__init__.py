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

bl_info = {
    "name": "Omni Panel",
    "author": "NVIDIA Corporation",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Toolbar > Omniverse",
    "description": "Nvidia Omniverse bake materials for export to usd",
    "warning": "",
    "doc_url": "",
    "category": "Omniverse",
}

import bpy

#Import classes	
from .material_bake.operators import (OBJECT_OT_omni_bake_mapbake, 	
OBJECT_OT_omni_bake_bgbake_status, OBJECT_OT_omni_bake_bgbake_import, OBJECT_OT_omni_bake_bgbake_clear)	
from .ui import (OBJECT_PT_omni_bake_panel, OmniBakePreferences)	
from .particle_bake.operators import(MyProperties, PARTICLES_OT_omni_hair_bake)	

#Classes list for register	
#List of all classes that will be registered	
classes = ([OBJECT_OT_omni_bake_mapbake, OBJECT_PT_omni_bake_panel, OmniBakePreferences, OBJECT_OT_omni_bake_bgbake_status, 
        OBJECT_OT_omni_bake_bgbake_import, OBJECT_OT_omni_bake_bgbake_clear, MyProperties, PARTICLES_OT_omni_hair_bake])


def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#---------------------UPDATE FUNCTIONS--------------------------------------------
def tex_per_mat_update(self, context):
    if context.scene.tex_per_mat == True:
        context.scene.prepmesh = False
        context.scene.hidesourceobjects = False
        context.scene.expand_mat_uvs = False

def expand_mat_uvs_update(self, context):
    context.scene.newUVoption = False
    context.scene.prefer_existing_sbmap = False

def prepmesh_update(self, context):
    if context.scene.prepmesh == False:
        context.scene.hidesourceobjects = False
    else:
        context.scene.hidesourceobjects = True

def texture_res_update(self, context):
    if context.scene.texture_res == "0.5k":
        context.scene.imgheight = 1024/2
        context.scene.imgwidth = 1024/2
        context.scene.render.bake.margin = 6

    elif context.scene.texture_res == "1k":
        context.scene.imgheight = 1024
        context.scene.imgwidth = 1024
        context.scene.render.bake.margin = 10
        
    elif context.scene.texture_res == "2k":
        context.scene.imgheight = 1024*2
        context.scene.imgwidth = 1024*2
        context.scene.render.bake.margin = 14
        
    elif context.scene.texture_res == "4k":
        context.scene.imgheight = 1024*4
        context.scene.imgwidth = 1024*4
        context.scene.render.bake.margin = 20

    elif context.scene.texture_res == "8k":
        context.scene.imgheight = 1024*8
        context.scene.imgwidth = 1024*8
        context.scene.render.bake.margin = 32

def newUVoption_update(self, context):
    if bpy.context.scene.newUVoption == True:
        bpy.context.scene.prefer_existing_sbmap = False

def all_maps_update(self,context):
    bpy.context.scene.selected_col = True
    bpy.context.scene.selected_metal = True
    bpy.context.scene.selected_rough = True
    bpy.context.scene.selected_normal = True
    bpy.context.scene.selected_trans = True
    bpy.context.scene.selected_transrough = True
    bpy.context.scene.selected_emission = True
    bpy.context.scene.selected_specular = True
    bpy.context.scene.selected_alpha = True
    bpy.context.scene.selected_sss = True
    bpy.context.scene.selected_ssscol = True

#-------------------END UPDATE FUNCTIONS----------------------------------------------

def register():

    #Register classes
    global classes
    for cls in classes:
        bpy.utils.register_class(cls)
    
    global bl_info
    version = bl_info["version"]
    version = str(version[0]) + str(version[1]) + str(version[2])
    
    OBJECT_PT_omni_bake_panel.version = f"{str(version[0])}.{str(version[1])}.{str(version[2])}"
    
    
    #Global variables
    
    des = "Texture Resolution"
    bpy.types.Scene.texture_res = bpy.props.EnumProperty(name="Texture Resolution", default="1k", description=des, items=[
    ("0.5k", "0.5k", f"Texture Resolution of {1024/2} x {1024/2}"),
    ("1k", "1k", f"Texture Resolution of 1024 x 1024"),
    ("2k", "2k", f"Texture Resolution of {1024*2} x {1024*2}"),
    ("4k", "4k", f"Texture Resolution of {1024*4} x {1024*4}"),
    ("8k", "8k", f"Texture Resolution of {1024*8} x {1024*8}")
    ], update = texture_res_update)

    des = "Distance to cast rays from target object to selected object(s)"
    bpy.types.Scene.ray_distance = bpy.props.FloatProperty(name="Ray Distance", default = 0.2, description=des)
    bpy.types.Scene.ray_warning_given = bpy.props.BoolProperty(default = False)
    
    des = "Normal maps are always created as 32bit float images, but this option causes all images to be created as 32bit float. Image quality is theoretically increased, but often it will not be noticable."
    bpy.types.Scene.everything32bitfloat = bpy.props.BoolProperty(name="All internal 32bit float", default = False, description=des)
    des = "Normal maps are always exported as 16bit, but this option causes all images to be exported 16bit. Not available with jpg or tga. Image quality is theoretically increased, but often it will not be noticable."
    bpy.types.Scene.everything16bit = bpy.props.BoolProperty(name="All exports 16bit", default = False, description=des)

    des = "Bake all maps (Diffuse, Metal, SSS, SSS Col. Roughness, Normal, Transmission, Transmission Roughness, Emission, Specular, Alpha, Displacement)"
    bpy.types.Scene.all_maps = bpy.props.BoolProperty(name="Bake All Maps", default = True, description=des, update = all_maps_update)

    des = "Bake a PBR Colour map"
    bpy.types.Scene.selected_col = bpy.props.BoolProperty(name="Diffuse", default = True, description=des)
    des = "Apply colour space settings (exposure, gamma etc.) from current scene when saving the diffuse image externally. Only available if you are exporting baked images. Will be ignored if exporting to EXR files as these don't support colour management"
    bpy.types.Scene.selected_applycolmantocol = bpy.props.BoolProperty(name="Export diffuse with col management settings", default = False, description=des)

    #--- MAPS -----------------------

    des = "Bake a PBR Metalness map"
    bpy.types.Scene.selected_metal = bpy.props.BoolProperty(name="Metal", description=des, default= True)
    des = "Bake a PBR Roughness or Glossy map"
    bpy.types.Scene.selected_rough = bpy.props.BoolProperty(name="Roughness", description=des, default= True)
    des = "Bake a Normal map"
    bpy.types.Scene.selected_normal = bpy.props.BoolProperty(name="Normal", description=des, default= True)
    des = "Bake a PBR Transmission map"
    bpy.types.Scene.selected_trans = bpy.props.BoolProperty(name="Transmission", description=des, default= True)
    des = "Bake a PBR Transmission Roughness map"
    bpy.types.Scene.selected_transrough = bpy.props.BoolProperty(name="TR Rough", description=des, default= True)
    des = "Bake an Emission map"
    bpy.types.Scene.selected_emission = bpy.props.BoolProperty(name="Emission", description=des, default= True)
    des = "Bake a Subsurface map"
    bpy.types.Scene.selected_sss = bpy.props.BoolProperty(name="SSS", description=des, default= True)
    des = "Bake a Subsurface colour map"
    bpy.types.Scene.selected_ssscol = bpy.props.BoolProperty(name="SSS Col", description=des, default= True)
    des = "Bake a Specular/Reflection map"
    bpy.types.Scene.selected_specular = bpy.props.BoolProperty(name="Specular", description=des, default= True)
    des = "Bake a PBR Alpha map"
    bpy.types.Scene.selected_alpha = bpy.props.BoolProperty(name="Alpha", description=des, default= True)
    
    des = "Bake each material into its own texture (for export to virtual worlds like Second Life)"
    bpy.types.Scene.tex_per_mat = bpy.props.BoolProperty(name="Texture per material", description=des, update=tex_per_mat_update)
 
    #UVs-----------
    
    des = "Use Smart UV Project to create a new UV map for your objects (or target object if baking to a target). See Blender Market FAQs for more details"
    bpy.types.Scene.newUVoption = bpy.props.BoolProperty(name="New UV(s)", description=des, update=newUVoption_update, default= False)
    des = "If one exists for the object being baked, use any existing UV maps called 'OmniBake' for baking (rather than the active UV map)"
    bpy.types.Scene.prefer_existing_sbmap = bpy.props.BoolProperty(name="Prefer existing UV maps called OmniBake", description=des)
    
    des = "New UV Method"
    bpy.types.Scene.newUVmethod = bpy.props.EnumProperty(name="New UV Method", default="SmartUVProject_Atlas", description=des, items=[
    ("SmartUVProject_Individual", "Smart UV Project (Individual)", "Each object gets a new UV map using Smart UV Project"),
    ("SmartUVProject_Atlas", "Smart UV Project (Atlas)", "Create a combined UV map (atlas map) using Smart UV Project"),
    ("CombineExisting", "Combine Active UVs (Atlas)", "Create a combined UV map (atlas map) by combining the existing, active UV maps on each object")])

    des = "If you are creating new UVs, or preferring an existing UV map called OmniBake, the UV map used for baking may not be the one you had displayed in the viewport before baking. This option restores what you had active before baking"
    bpy.types.Scene.restoreOrigUVmap = bpy.props.BoolProperty(name="Restore originally active UV map at end", description=des, default=True)
    
    des = "Margin to use when packing combined UVs into Atlas map"
    bpy.types.Scene.uvpackmargin = bpy.props.FloatProperty(name="Pack Margin", default=0.05, description=des)
    
    des = "Average the size of the UV islands when combining them into the atlas map"
    bpy.types.Scene.averageUVsize = bpy.props.BoolProperty(name="Average UV Island Size", default=True, description=des)
    
    des = "When using 'Texture per material', Create a new UV map, and expand the UVs from each material to fill that map using Smart UV Project"
    bpy.types.Scene.expand_mat_uvs = bpy.props.BoolProperty(name="New UVs per material, expanded to bounds", description=des, update=expand_mat_uvs_update)

    des = "Bake to normal UVs"
    bpy.types.Scene.uv_mode = bpy.props.EnumProperty(name="UV Mode", default="normal", description=des, items=[
    ("normal", "Normal", "Normal UV maps")])
    
    #---------------

    des = "Create a copy of your selected objects in Blender (or target object if baking to a target) and apply the baked textures to it. If you are baking in the background, this happens after you import"
    bpy.types.Scene.prepmesh = bpy.props.BoolProperty(name="Copy objects and apply bakes", default = True, description=des, update=prepmesh_update)
    des = "Hide the source object that you baked from in the viewport after baking. If you are baking in the background, this happens after you import"
    bpy.types.Scene.hidesourceobjects = bpy.props.BoolProperty(name="Hide source objects after bake", default = True, description=des)
    
    des = "Export your mesh as a .fbx file with a single texture and the UV map used for baking (i.e. ready for import somewhere else. File is saved in the folder specified below, under the folder where your blend file is saved. Not available if .blend file not saved"
    bpy.types.Scene.saveObj = bpy.props.BoolProperty(name="Export mesh", default = False, description=des)
        
    des = "Set the height of the baked image that will be produced"
    bpy.types.Scene.imgheight = bpy.props.IntProperty(name="Height", default=1024, description=des)
    des = "Set the width of the baked image that will be produced"
    bpy.types.Scene.imgwidth = bpy.props.IntProperty(name="Width", default=1024, description=des)
    
    des = "Set the height of the baked image that will be ouput"
    bpy.types.Scene.outputheight = bpy.props.IntProperty(name="Output Height", default=1024, description=des)
    des = "Set the width of the baked image that will be output"
    bpy.types.Scene.outputwidth = bpy.props.IntProperty(name="Output Width", default=1024, description=des)
    
    
    bpy.types.Scene.memLimit = bpy.props.EnumProperty(name="GPU Memory Limit", default="Off", 
        description="Limit memory usage by limiting render tile size. More memory means faster bake times, but it is possible to exceed the capabilities of your computer which will lead to a crash or slow bake times", items=[
            ("512", "Ultra Low", "Ultra Low memory usage (max 512 tile size)"),
            ("1024", "Low", "Low memory usage (max 1024 tile size)"),
            ("2048", "Medium", "Medium memory usage (max 2048 tile size)"),
            ("4096", "Normal", "Normal memory usage, for a reasonably modern computer (max 4096 tile size)"),
            ("Off", "No Limit", "Don't limit memory usage (tile size matches render image size)")
            ])
   
    des = "Margin between islands to use for Smart UV Project"
    bpy.types.Scene.unwrapmargin = bpy.props.FloatProperty(name="Margin", default=0.03, description=des)

    bpy.types.Scene.channelpackfileformat = bpy.props.EnumProperty(name="Export File Format for Channel Packing", default="OPEN_EXR", 
        description="Select the file format for exported bakes. Also applies to Sketchfab upload images", items=[
            ("PNG", "PNG", ""),
            ("TARGA", "TGA", ""),
            ("OPEN_EXR", "Open EXR", "")
            ])

    
    des="Name of the folder to create and save the bakes/mesh into. Created in the folder where you blend file is saved. NOTE: To maintain compatibility, only MS Windows acceptable characters will be used"
    bpy.types.Scene.saveFolder = bpy.props.StringProperty(name="Save folder name", description=des, default="OmniBake_Bakes", maxlen=20)
    
    des="Name to apply to these bakes (is incorporated into the bakes file name, provided you have included this in the image format string - see addon preferences). NOTE: To maintain compatibility, only MS Windows acceptable characters will be used"
    bpy.types.Scene.batchName = bpy.props.StringProperty(name="Batch name", description=des, default="Bake1", maxlen=20)
    
    des="Switch between roughness and glossiness (inverts of each other). NOTE: Roughness is the default for Blender so, if you change this, texture probably won't look right when used in Blender"
    bpy.types.Scene.rough_glossy_switch = bpy.props.EnumProperty(name="", default="rough", 
        description=des, items=[
            ("rough", "Rough", ""),
            ("glossy", "Glossy", "")
            ])
    
    des="Switch between OpenGL and DirectX formats for normal map. NOTE: Opengl is the default for Blender so, if you change this, texture probably won't look right when used in Blender"
    bpy.types.Scene.normal_format_switch = bpy.props.EnumProperty(name="", default="opengl", 
        description=des, items=[
            ("opengl", "OpenGL", ""),
            ("directx", "DirectX", "")
            ])
    
    #---------------------Channel packing-------------------------------------------

    bpy.types.Scene.bgbake = bpy.props.EnumProperty(name="Background Bake", default="fg", items=[
    ("fg", "Foreground", "Perform baking in the foreground. Blender will lock up until baking is complete"),
    ("bg", "Background", "Perform baking in the background, leaving you free to continue to work in Blender while the baking is being carried out")
    ])
   
    #---------------------Lightmap col management------------------------------------------
    des = "Apply the colour management settings you have set in the render properties panel to the lightmap. Only available when you are exporting your bakes. Will be ignored if exporting to EXR files as these don't support colour management"
    bpy.types.Scene.omnibake_lightmap_apply_colman = bpy.props.BoolProperty(name="Export with colour management settings", default=False, description=des)


    #---------------------Filehanding & Particles------------------------------------------
    
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type= MyProperties)

    #-------------------Additional Shaders-------------------------------------------

    des = "Allows for use of Add, Diffuse, Glossy, Glass, Refraction, Transparent, Anisotropic Shaders. May cause inconsistent results"
    bpy.types.Scene.more_shaders = bpy.props.BoolProperty(name="Use Additional Shader Types", default=False, description=des)
    


    


def unregister():

    #User preferences
    global classes
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.my_tool
    del bpy.types.Scene.more_shaders

    del bpy.types.Scene.saveObj
    del bpy.types.Scene.newUVoption
    del bpy.types.Scene.memLimit
    del bpy.types.Scene.prepmesh
    del bpy.types.Scene.unwrapmargin
    del bpy.types.Scene.everything32bitfloat
    del bpy.types.Scene.everything16bit
    del bpy.types.Scene.texture_res
    del bpy.types.Scene.hidesourceobjects
    del bpy.types.Scene.saveFolder
    del bpy.types.Scene.batchName
    del bpy.types.Scene.bgbake
    del bpy.types.Scene.selected_applycolmantocol
    
    del bpy.types.Scene.imgheight
    del bpy.types.Scene.imgwidth
    del bpy.types.Scene.outputwidth


if __name__ == "__main__":
    register()


