bl_info = {
    "name": "Omni Panel",
    "author": "NVIDIA Corporation",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Toolbar > Omni",
    "description": "Nvidia Omniverse bake materials for export to usd",
    "warning": "",
    "doc_url": "",
    "category": "OMNIVERSE",
}


import bpy


#Import classes
from .operators import (OBJECT_OT_simple_bake_mapbake, OBJECT_OT_simple_bake_selectall, OBJECT_OT_simple_bake_selectnone, OBJECT_OT_simple_bake_default_imgname_string,
OBJECT_OT_simple_bake_default_aliases, OBJECT_OT_simple_bake_bgbake_status, OBJECT_OT_simple_bake_bgbake_import, OBJECT_OT_simple_bake_bgbake_clear, OBJECT_OT_simple_bake_protect_clear, OBJECT_OT_simple_bake_import_special_mats)
from .ui import (OBJECT_PT_simple_bake_panel, SimpleBakePreferences, ListItem, BAKEOBJECTS_UL_List,
LIST_OT_NewItem, LIST_OT_DeleteItem, LIST_OT_MoveItem, LIST_OT_ClearAll, LIST_OT_Refresh)
from .omni_blender_panel import(MyProperties, TEXTURE_OT_omni_texture_bake, PARTICLES_OT_omni_hair_bake)


#Classes list for register
#List of all classes that will be registered
classes = ([OBJECT_OT_simple_bake_mapbake, OBJECT_OT_simple_bake_selectall, OBJECT_OT_simple_bake_selectnone,
        OBJECT_PT_simple_bake_panel, SimpleBakePreferences, OBJECT_OT_simple_bake_default_imgname_string, 
        OBJECT_OT_simple_bake_default_aliases, OBJECT_OT_simple_bake_bgbake_status, OBJECT_OT_simple_bake_bgbake_import, OBJECT_OT_simple_bake_bgbake_clear, OBJECT_OT_simple_bake_protect_clear,
        ListItem, BAKEOBJECTS_UL_List, LIST_OT_NewItem, LIST_OT_DeleteItem, LIST_OT_MoveItem, LIST_OT_ClearAll, LIST_OT_Refresh, OBJECT_OT_simple_bake_import_special_mats, 
        MyProperties, TEXTURE_OT_omni_texture_bake, PARTICLES_OT_omni_hair_bake
        ])


def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)


#---------------------UPDATE FUNCTIONS--------------------------------------------
def tex_per_mat_update(self, context):
    if context.scene.tex_per_mat == True:
        context.scene.prepmesh = False
        context.scene.hidesourceobjects = False
        #context.scene.mergedBake = False
        context.scene.expand_mat_uvs = False
        
    
def expand_mat_uvs_update(self, context):
    context.scene.newUVoption = False
    context.scene.prefer_existing_sbmap = False

def prepmesh_update(self, context):
    if context.scene.prepmesh == False:
        context.scene.hidesourceobjects = False
    else:
        context.scene.hidesourceobjects = True
    
def exportfileformat_update(self,context):
    if context.scene.exportfileformat == "JPEG" or context.scene.exportfileformat == "TARGA":
        context.scene.everything16bit = False

def texture_res_update(self, context):
    if context.scene.texture_res == "Test":
        context.scene.imgheight = 128
        context.scene.imgwidth = 128
        context.scene.render.bake.margin = 2

    elif context.scene.texture_res == "0.5k":
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
        
    elif context.scene.texture_res == "3k":
        context.scene.imgheight = 1024*3
        context.scene.imgwidth = 1024*3
        context.scene.render.bake.margin = 18
        
    elif context.scene.texture_res == "4k":
        context.scene.imgheight = 1024*4
        context.scene.imgwidth = 1024*4
        context.scene.render.bake.margin = 20

    elif context.scene.texture_res == "5k":
        context.scene.imgheight = 1024*5
        context.scene.imgwidth = 1024*5
        context.scene.render.bake.margin = 24

    elif context.scene.texture_res == "6k":
        context.scene.imgheight = 1024*6
        context.scene.imgwidth = 1024*6
        context.scene.render.bake.margin = 28

    elif context.scene.texture_res == "8k":
        context.scene.imgheight = 1024*8
        context.scene.imgwidth = 1024*8
        context.scene.render.bake.margin = 32
    
    context.scene.output_res = context.scene.texture_res

def output_res_update(self, context):
    if context.scene.output_res == "Test":
        context.scene.outputheight = 128
        context.scene.outputwidth = 128
        #context.scene.render.bake.margin = 2

    elif context.scene.output_res == "0.5k":
        context.scene.outputheight = 1024/2
        context.scene.outputheight = 1024/2
        #context.scene.render.bake.margin = 6

    elif context.scene.output_res == "1k":
        context.scene.outputheight = 1024
        context.scene.outputwidth = 1024
        #context.scene.render.bake.margin = 10
        
    elif context.scene.output_res == "2k":
        context.scene.outputheight = 1024*2
        context.scene.outputwidth = 1024*2
        #context.scene.render.bake.margin = 14
        
    elif context.scene.output_res == "3k":
        context.scene.outputheight = 1024*3
        context.scene.outputwidth = 1024*3
        #context.scene.render.bake.margin = 18
        
    elif context.scene.output_res == "4k":
        context.scene.outputheight = 1024*4
        context.scene.outputwidth = 1024*4
        #context.scene.render.bake.margin = 20

    elif context.scene.output_res == "5k":
        context.scene.outputheight = 1024*5
        context.scene.outputwidth = 1024*5
        #context.scene.render.bake.margin = 24

    elif context.scene.output_res == "6k":
        context.scene.outputheight = 1024*6
        context.scene.outputwidth = 1024*6
        #context.scene.render.bake.margin = 28
    
    elif context.scene.output_res == "8k":
        context.scene.outputheight = 1024*8
        context.scene.outputwidth = 1024*8
        #context.scene.render.bake.margin = 32
        
        
def alpha_update(self, context):
    pass
    #bpy.context.scene.mergedBake = False
    
def s2a_update(self, context):
    #bpy.context.scene.mergedBake = False
    pass
    
def repackUVs_update(self, context):
    pass

def newUVoption_update(self, context):
    if bpy.context.scene.newUVoption == True:
        bpy.context.scene.prefer_existing_sbmap = False
        #bpy.context.scene.repackUVs = False

def prefer_existing_sbmap_update(self, context):
    pass

def ray_distance_update(self, context):
    pass

def mergedBake_update(self, context):
    #if bpy.context.scene.newUVmethod == "SmartUVProject_Individual" and bpy.context.scene.mergedBake:
        #ShowMessageBox("This combination of options probably isn't what you want. You are unwrapping multiple objects individually, and then baking them all to one texture. The bakes will be on top of each other.", "Warning", "MONKEY")
    pass

def newUVmethod_update(self, context):
    pass
    #if bpy.context.scene.newUVmethod == "SmartUVProject_Individual" and bpy.context.scene.mergedBake:
        #ShowMessageBox("This combination of options probably isn't what you want. You are unwrapping multiple objects individually, and then baking them all to one texture. The bakes will be on top of each other.", "Warning", "MONKEY")


def global_mode_update(self, context):
    
    
    if not bpy.context.scene.simplebake_global_mode == "pbr_bake":
        bpy.context.scene.selected_s2a = False
        bpy.context.scene.selected_lightmap_denoise = False
        bpy.context.scene.targetobj_cycles = None


def cycles_s2a_update(self, context):
    if context.scene.cycles_s2a:
        #context.scene.mergedBake = False  
        pass


def pack_master_switch_update(self,context):
    #Turn off all packing
    if not context.scene.pack_master_switch:
        context.scene.unity_lit_shader = False
        #context.scene.pack_gloss2metal_alpha = False


def selected_rough_update(self,context):
    if context.scene.selected_rough == False:
        context.scene.unity_lit_shader = False
        #context.scene.pack_gloss2metal_alpha = False


def selected_metal_update(self,context):
    if context.scene.selected_metal == False:
        context.scene.unity_lit_shader = False
        #context.scene.pack_gloss2metal_alpha = False
        
def bgbake_update(self,context):
    pass
    
    
def uv_mode_update(self, context):
    if context.scene.uv_mode == "udims":
        context.scene.newUVoption = False
        
 
def selected_ao_update(self, context):
    if not context.scene.selected_ao:
        context.scene.unity_lit_shader = False
        

def simplebake_dospecials_update(self,context):
    #Deselect all specials
    if not context.scene.simplebake_dospecials:
        context.scene.selected_col_mats = False
        context.scene.selected_col_vertex = False
        context.scene.selected_ao = False
        context.scene.selected_thickness = False
        context.scene.selected_curvature = False
        context.scene.selected_lightmap = False
    
def selected_col_update(self, context):
    if not context.scene.selected_col:
        context.scene.diffuse_plus_spec_in_alpha = False

def selected_specular_update(self, context):
    if not context.scene.selected_specular:
        context.scene.diffuse_plus_spec_in_alpha = False

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
    
    OBJECT_PT_simple_bake_panel.version = f"{str(version[0])}.{str(version[1])}.{str(version[2])}"
    
    
    #Global variables
    des = "Global Baking Mode"
    bpy.types.Scene.simplebake_global_mode = bpy.props.EnumProperty(
        name="Bake Mode", 
        default="pbr_bake", 
        description=des, 
        items=[ ("pbr_bake", "PBR Bake", "Bake PBR maps from materials created around the Principled BSDF and Emission shaders")], 
        update = global_mode_update)
    
    des = "Texture Resolution"
    bpy.types.Scene.texture_res = bpy.props.EnumProperty(name="Texture Resolution", default="1k", description=des, items=[
    ("0.5k", "0.5k", f"Texture Resolution of {1024/2} x {1024/2}"),
    ("1k", "1k", f"Texture Resolution of 1024 x 1024"),
    ("2k", "2k", f"Texture Resolution of {1024*2} x {1024*2}"),
    ("4k", "4k", f"Texture Resolution of {1024*4} x {1024*4}"),
    ("8k", "8k", f"Texture Resolution of {1024*8} x {1024*8}")
    ], update = texture_res_update)

    des = "Output Resolution"
    bpy.types.Scene.output_res = bpy.props.EnumProperty(name="Output Resolution", default="1k", description=des, items=[
    ("0.5k", "0.5k", f"Texture Resolution of {1024/2} x {1024/2}"),
    ("1k", "1k", f"Texture Resolution of 1024 x 1024"),
    ("2k", "2k", f"Texture Resolution of {1024*2} x {1024*2}"),
    ("4k", "4k", f"Texture Resolution of {1024*4} x {1024*4}"),
    ("8k", "8k", f"Texture Resolution of {1024*8} x {1024*8}")
    ], update = output_res_update)


    des = "Distance to cast rays from target object to selected object(s)"
    bpy.types.Scene.ray_distance = bpy.props.FloatProperty(name="Ray Distance", default = 0.2, description=des, update=ray_distance_update)
    bpy.types.Scene.ray_warning_given = bpy.props.BoolProperty(default = False)
    
    des = "Normal maps are always created as 32bit float images, but this option causes all images to be created as 32bit float. Image quality is theoretically increased, but often it will not be noticable."
    bpy.types.Scene.everything32bitfloat = bpy.props.BoolProperty(name="All internal 32bit float", default = False, description=des)
    des = "Normal maps are always exported as 16bit, but this option causes all images to be exported 16bit. Not available with jpg or tga. Image quality is theoretically increased, but often it will not be noticable."
    bpy.types.Scene.everything16bit = bpy.props.BoolProperty(name="All exports 16bit", default = False, description=des)
    

    des = "Bake all maps (Diffuse, Metal, SSS, SSS Col. Roughness, Normal, Transmission, Transmission Roughness, Emission, Specular, Alpha, Displacement)"
    bpy.types.Scene.all_maps = bpy.props.BoolProperty(name="Bake All Maps", default = True, description=des, update = all_maps_update)

    des = "Bake a PBR Colour map"
    bpy.types.Scene.selected_col = bpy.props.BoolProperty(name="Diffuse", default = True, description=des, update=selected_col_update)
    des = "Apply colour space settings (exposure, gamma etc.) from current scene when saving the diffuse image externally. Only available if you are exporting baked images. Will be ignored if exporting to EXR files as these don't support colour management"
    bpy.types.Scene.selected_applycolmantocol = bpy.props.BoolProperty(name="Export diffuse with col management settings", default = False, description=des)


    des = "Bake a PBR Metalness map"
    bpy.types.Scene.selected_metal = bpy.props.BoolProperty(name="Metal", description=des, update=selected_metal_update)
    des = "Bake a PBR Roughness or Glossy map"
    bpy.types.Scene.selected_rough = bpy.props.BoolProperty(name="Roughness", description=des, update=selected_rough_update)
    des = "Bake a Normal map"
    bpy.types.Scene.selected_normal = bpy.props.BoolProperty(name="Normal", description=des)
    des = "Bake a PBR Transmission map"
    bpy.types.Scene.selected_trans = bpy.props.BoolProperty(name="Transmission", description=des)
    des = "Bake a PBR Transmission Roughness map"
    bpy.types.Scene.selected_transrough = bpy.props.BoolProperty(name="TR Rough", description=des)
    des = "Bake an Emission map"
    bpy.types.Scene.selected_emission = bpy.props.BoolProperty(name="Emission", description=des)
    
    
    
    
    des = "Bake a Subsurface map"
    bpy.types.Scene.selected_sss = bpy.props.BoolProperty(name="SSS", description=des)
    des = "Bake a Subsurface colour map"
    bpy.types.Scene.selected_ssscol = bpy.props.BoolProperty(name="SSS Col", description=des)
    des = "Bake a Specular/Reflection map"
    bpy.types.Scene.selected_specular = bpy.props.BoolProperty(name="Specular", description=des, update=selected_specular_update)
    des = "Bake a PBR Alpha map"
    bpy.types.Scene.selected_alpha = bpy.props.BoolProperty(name="Alpha", description=des)
    
    des = "Bake each material into its own texture (for export to virtual worlds like Second Life"
    bpy.types.Scene.tex_per_mat = bpy.props.BoolProperty(name="Texture per material", description=des, update=tex_per_mat_update)
    
    
    #-----------Specials-------------------------------------------
    des = "ColourID Map based on random colour per material"
    bpy.types.Scene.selected_col_mats = bpy.props.BoolProperty(name="Col ID (Mats)", description=des)
    des = "Bake the active vertex colours to a texture"
    bpy.types.Scene.selected_col_vertex = bpy.props.BoolProperty(name="Vertex Colours", description=des)
    des = "Ambient Occlusion"
    bpy.types.Scene.selected_ao = bpy.props.BoolProperty(name="AO", description=des, update=selected_ao_update)
    des = "Thickness map"
    bpy.types.Scene.selected_thickness = bpy.props.BoolProperty(name="Thickness", description=des)
    des = "Curvature map"
    bpy.types.Scene.selected_curvature = bpy.props.BoolProperty(name="Curvature", description=des)
    des = "Lightmap map"
    bpy.types.Scene.selected_lightmap = bpy.props.BoolProperty(name="Lightmap", description=des)
    des = "Run lightmap through the compositor denoise node, only available when you are exporting you bakes"
    bpy.types.Scene.selected_lightmap_denoise = bpy.props.BoolProperty(name="Denoise Lightmap", description=des)
    
    
    des = "Bake maps from one or more  source objects (usually high poly) to a single target object (usually low poly). Source and target objects must be in the same location (overlapping). See Blender documentation on selected to active baking for more details"
    bpy.types.Scene.selected_s2a = bpy.props.BoolProperty(name="Bake selected objects to target object", update = s2a_update, description=des)
    des = "Specify the target object for the baking. Note, this need not be part of your selection in the viewport (though it can be)"
    bpy.types.Scene.targetobj = bpy.props.PointerProperty(name="Target Object", description=des, type=bpy.types.Object)
    
    
    #UVs-----------
    
    des = "Use Smart UV Project to create a new UV map for your objects (or target object if baking to a target). See Blender Market FAQs for more details"
    bpy.types.Scene.newUVoption = bpy.props.BoolProperty(name="New UV(s)", description=des, update=newUVoption_update, default= False)
    des = "If one exists for the object being baked, use any existing UV maps called 'SimpleBake' for baking (rather than the active UV map)"
    bpy.types.Scene.prefer_existing_sbmap = bpy.props.BoolProperty(name="Prefer existing UV maps called SimpleBake", description=des, update=prefer_existing_sbmap_update)
    
    des = "New UV Method"
    bpy.types.Scene.newUVmethod = bpy.props.EnumProperty(name="New UV Method", default="SmartUVProject_Atlas", description=des, items=[
    ("SmartUVProject_Individual", "Smart UV Project (Individual)", "Each object gets a new UV map using Smart UV Project"),
    ("SmartUVProject_Atlas", "Smart UV Project (Atlas)", "Create a combined UV map (atlas map) using Smart UV Project"),
    ("CombineExisting", "Combine Active UVs (Atlas)", "Create a combined UV map (atlas map) by combining the existing, active UV maps on each object")
    ], update=newUVmethod_update)
    
    des = "If you are creating new UVs, or preferring an existing UV map called SimpleBake, the UV map used for baking may not be the one you had displayed in the viewport before baking. This option restores what you had active before baking"
    bpy.types.Scene.restoreOrigUVmap = bpy.props.BoolProperty(name="Restore originally active UV map at end", description=des, default=True)
    
    des = "Margin to use when packing combined UVs into Atlas map"
    bpy.types.Scene.uvpackmargin = bpy.props.FloatProperty(name="Pack Margin", default=0.05, description=des)
    
    des = "Average the size of the UV islands when combining them into the atlas map"
    bpy.types.Scene.averageUVsize = bpy.props.BoolProperty(name="Average UV Island Size", default=True, description=des)
    
    des = "When using 'Texture per material', Create a new UV map, and expand the UVs from each material to fill that map using Smart UV Project"
    bpy.types.Scene.expand_mat_uvs = bpy.props.BoolProperty(name="New UVs per material, expanded to bounds", description=des, update=expand_mat_uvs_update)


    des = "Bake to UDIMs or normal UVs. You must be exporting your bakes to use UDIMs. You must manually create your UDIM UVs (this cannot be automated)"
    bpy.types.Scene.uv_mode = bpy.props.EnumProperty(name="UV Mode", default="normal", description=des, items=[
    ("normal", "Normal", "Normal UV maps"),
    ("udims", "UDIMs", "UDIM UV maps")
    ], update = uv_mode_update)
    
    des = "Set the number of tiles that your UV map has used"
    bpy.types.Scene.udim_tiles = bpy.props.IntProperty(name="UDIM Tiles", default=2, description=des)

    
    
    #---------------
    
    des = "Create a sub-folder for the textures of each baked object. Only available if you are exporting bakes."
    bpy.types.Scene.exportFolderPerObject = bpy.props.BoolProperty(name="Sub-folder for bakes per object", default = False, description=des)
    
    des = "Create a copy of your selected objects in Blender (or target object if baking to a target) and apply the baked textures to it. If you are baking in the background, this happens after you import"
    bpy.types.Scene.prepmesh = bpy.props.BoolProperty(name="Copy objects and apply bakes", default = True, description=des, update=prepmesh_update)
    des = "Hide the source object that you baked from in the viewport after baking. If you are baking in the background, this happens after you import"
    bpy.types.Scene.hidesourceobjects = bpy.props.BoolProperty(name="Hide source objects after bake", default = True, description=des)
    
    des = "Export your mesh as a .fbx file with a single texture and the UV map used for baking (i.e. ready for import somewhere else. File is saved in the folder specified below, under the folder where your blend file is saved. Not available if .blend file not saved"
    bpy.types.Scene.saveObj = bpy.props.BoolProperty(name="Export mesh", default = False, description=des)
    des = "File name of the fbx. NOTE: To maintain compatibility, only MS Windows acceptable characters will be used"
    bpy.types.Scene.fbxName = bpy.props.StringProperty(name="FBX name", description=des, default="Export", maxlen=20)
    
    
    des = "Baked images have a transparent background (else Black)"
    bpy.types.Scene.useAlpha = bpy.props.BoolProperty(name="Use Alpha", default = False, update = alpha_update, description=des)
    des = "Bake multiple objects to one set of textures. Not available with 'Use Alpha' (limitation of Blender) or with 'Bake maps to target object' (would not make sense). You must have more than one object selected for baking"
    bpy.types.Scene.mergedBake = bpy.props.BoolProperty(name="Multiple objects to one texture set", default = False, description=des, update = mergedBake_update)
    des = "When baking one object at a time, the object's name is used in the texture name. Baking multiple objects to one texture set, however requires you to proivde a name for the textures"
    bpy.types.Scene.mergedBakeName = bpy.props.StringProperty(name="Texture name for multiple bake", default = "MergedBake", description=des)
        
    des = "Set the height of the baked image that will be produced"
    bpy.types.Scene.imgheight = bpy.props.IntProperty(name="Height", default=1024, description=des)
    des = "Set the width of the baked image that will be produced"
    bpy.types.Scene.imgwidth = bpy.props.IntProperty(name="Width", default=1024, description=des)
    
    des = "Set the height of the baked image that will be ouput"
    bpy.types.Scene.outputheight = bpy.props.IntProperty(name="Output Height", default=1024, description=des)
    des = "Set the width of the baked image that will be output"
    bpy.types.Scene.outputwidth = bpy.props.IntProperty(name="Output Width", default=1024, description=des)
    
    #des = "Set the colour space of the images created for cycles bakes"
    #bpy.types.Scene.cyclescolspace = bpy.props.EnumProperty(name="CyclesBake Col Space", default="sRGB", description=des, items=[
    #("sRGB", "sRGB", "Use the sRGB colour space for CyclesBakes"),
    #("Filmic Log", "Filmic", "Use the filmic log colour space for CyclesBakes")
    #])
    
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
    
    des = "Bake using the Cycles selected to active option"
    bpy.types.Scene.cycles_s2a = bpy.props.BoolProperty(name="Selected to Active", description=des, update = cycles_s2a_update)

    bpy.types.Scene.exportfileformat = bpy.props.EnumProperty(name="Export File Format", update=exportfileformat_update, default="PNG", 
        description="Select the file format for exported bakes. Also applies to Sketchfab upload images", items=[
            ("PNG", "PNG", ""),
            ("JPEG", "JPG", ""),
            ("TIFF", "TIFF", ""),
            ("TARGA", "TGA", ""),
            ("OPEN_EXR", "Open EXR", "")
            ])

    bpy.types.Scene.channelpackfileformat = bpy.props.EnumProperty(name="Export File Format for Channel Packing", default="OPEN_EXR", 
        description="Select the file format for exported bakes. Also applies to Sketchfab upload images", items=[
            ("PNG", "PNG", ""),
            ("TARGA", "TGA", ""),
            ("OPEN_EXR", "Open EXR", "")
            ])

    
    des="Name of the folder to create and save the bakes/mesh into. Created in the folder where you blend file is saved. NOTE: To maintain compatibility, only MS Windows acceptable characters will be used"
    bpy.types.Scene.saveFolder = bpy.props.StringProperty(name="Save folder name", description=des, default="SimpleBake_Bakes", maxlen=20)
    
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
    
    des="Display channel packing options (for game engines). Only available when Export Bakes option is used. Packed image will be exported only (no internal Blender image)."
    bpy.types.Scene.pack_master_switch = bpy.props.BoolProperty(name="Channel Packing", description=des, update=pack_master_switch_update)

    
    des="Create a channel packed image suitable for the Unity Lit shader. You must be baking all the required components i.e. metallic, AO and smoothness. You must be exporting bakes. PNG only for now."
    bpy.types.Scene.unity_lit_shader = bpy.props.BoolProperty(name="Unity Lit Shader", description=des)
    
    des="Create a packed image which is diffuse plus specular in the alpha channel. You must be baking diffuse and specular"
    bpy.types.Scene.diffuse_plus_spec_in_alpha = bpy.props.BoolProperty(name="Diffuse + specular in alpha", description=des)
    
    #des="Pack glossy/roughness (whatever you baked) into alpha and metalness in the blue channel"
    #bpy.types.Scene.pack_gloss2metal_alpha = bpy.props.BoolProperty(name="Pack roughness/glossy into metal", description=des)
    
    bpy.types.Scene.bgbake = bpy.props.EnumProperty(name="Background Bake", default="fg", items=[
    ("fg", "Foreground", "Perform baking in the foreground. Blender will lock up until baking is complete"),
    ("bg", "Background", "Perform baking in the background, leaving you free to continue to work in Blender while the baking is being carried out")
    ], update=bgbake_update)
    
    des="Append date and time to folder name. If you turn this off there is a risk that you will accidentally overwrite bakes you did before if you forget to change the folder name"
    bpy.types.Scene.folderdatetime = bpy.props.BoolProperty(name="Append date and time to folder", description=des, default=True)
    
    des="Run baked images through the compositor. Your blend file must be saved, and you must be exporting your bakes"
    bpy.types.Scene.rundenoise = bpy.props.BoolProperty(name="Denoise", description=des, default=False)
    
    #Global show tips on or off
    bpy.types.Scene.simplebake_showtips = bpy.props.BoolProperty(name="Show Tips", default=False)
    
    
    #---------------------Advanced object selection------------------------------------------
    
    #Advanced object selection
    des="When turned on, you will bake the objects added to the bake list. When turned off, you will bake objects selected in the viewport"
    bpy.types.Scene.simplebake_advancedobjectselection = bpy.props.BoolProperty(name="Use advanced object selection", default=False, description=des)
    bpy.types.Scene.simplebake_bakeobjs_advanced_list = bpy.props.CollectionProperty(type = ListItem)
    bpy.types.Scene.simplebake_bakeobjs_advanced_list_index = bpy.props.IntProperty(name = "Index for bake objects list", default = 0)
    
    #Cycles selected to active object selection
    des = "Specify the target object to bake to (this would be the active object with vanilla Blender baking)"
    bpy.types.Scene.targetobj_cycles = bpy.props.PointerProperty(name="Target Object", description=des, type=bpy.types.Object)

    #Also bake specials
    bpy.types.Scene.simplebake_dospecials = bpy.props.BoolProperty(name="Also bake special maps", default=False, update=simplebake_dospecials_update)
    
    
    #---------------------Lightmap col management------------------------------------------
    des = "Apply the colour management settings you have set in the render properties panel to the lightmap. Only available when you are exporting your bakes. Will be ignored if exporting to EXR files as these don't support colour management"
    bpy.types.Scene.simplebake_lightmap_apply_colman = bpy.props.BoolProperty(name="Export with colour management settings", default=False, description=des)


    #---------------------Filehanding & Particles------------------------------------------
    
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type= MyProperties)

    #-------------------------custom icons -------------------------------------

    


def unregister():

    #------------------
    #-----------------------

    #User preferences
    global classes
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.my_tool

    del bpy.types.Scene.saveObj
    del bpy.types.Scene.newUVoption
    del bpy.types.Scene.memLimit
    del bpy.types.Scene.useAlpha
    del bpy.types.Scene.prepmesh
    del bpy.types.Scene.unwrapmargin
    del bpy.types.Scene.everything32bitfloat
    del bpy.types.Scene.everything16bit
    del bpy.types.Scene.texture_res
    del bpy.types.Scene.output_res
    del bpy.types.Scene.hidesourceobjects
    del bpy.types.Scene.saveFolder
    del bpy.types.Scene.batchName
    del bpy.types.Scene.fbxName
    del bpy.types.Scene.bgbake
    del bpy.types.Scene.folderdatetime
    del bpy.types.Scene.rundenoise
    del bpy.types.Scene.exportFolderPerObject
    del bpy.types.Scene.simplebake_showtips
    del bpy.types.Scene.simplebake_advancedobjectselection
    del bpy.types.Scene.simplebake_bakeobjs_advanced_list
    del bpy.types.Scene.simplebake_bakeobjs_advanced_list_index
    del bpy.types.Scene.targetobj_cycles
    del bpy.types.Scene.simplebake_dospecials
    del bpy.types.Scene.simplebake_global_mode
    del bpy.types.Scene.selected_lightmap_denoise
    del bpy.types.Scene.unity_lit_shader
    del bpy.types.Scene.selected_applycolmantocol
    
    del bpy.types.Scene.imgheight
    del bpy.types.Scene.imgwidth
    del bpy.types.Scene.outputwidth
    
    del bpy.types.Scene.selected_col_mats
    del bpy.types.Scene.selected_col_vertex
    del bpy.types.Scene.selected_ao
    del bpy.types.Scene.selected_thickness
    del bpy.types.Scene.selected_curvature        
    

if __name__ == "__main__":
    register()


