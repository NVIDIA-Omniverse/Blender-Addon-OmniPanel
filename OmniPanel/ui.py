import bpy
from . import functions
from .omni_blender_panel import*
from .bg_bake import bgbake_ops

import os
from os.path import join, dirname, exists
import bpy.utils.previews

from bpy.props import StringProperty, PointerProperty
from bpy.types import PropertyGroup, UIList, Operator


def get_icons_directory():

    icons_directory = join(dirname(__file__), "icons")
    return icons_directory

class OBJECT_PT_simple_bake_panel(bpy.types.Panel):
    #bl_idname = "object.simple_bake_panel"
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
        # impExpCol.operator('wm.link',
        #    text='LIVE LINK',
        #    icon_value=self.icons["OMNIBLEND"].icon_id,
        #    emboss=False)
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
        row.scale_y = 1.5
        row.operator('omni.hair_bake',
           text='Convert',
           icon='MOD_PARTICLE_INSTANCE')

        #--------PBR Bake Settings-------------------
        layout.separator()
        column = layout.column(align= True)
        header = column.row()
        header.label(text = "Material Bake", icon = 'UV_DATA')
        box = column.box()

        if(context.scene.simplebake_global_mode == "pbr_bake"):
            
            
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
                if context.scene.selected_rough or context.scene.selected_normal:
                    x=1
                
                row = column.row()
                row.prop(context.scene, "selected_trans")
                row.prop(context.scene, "selected_transrough")
                row = column.row()
                row.prop(context.scene, "selected_emission")
                row.prop(context.scene, "selected_specular")
                row = column.row()
                row.prop(context.scene, "selected_alpha")
                row = column.row()

        
        
        
        #--------Texture Settings-------------------
        
        
        
        row = box.row()
        row.label(text="Texture Resolution:")
        row.scale_y = 0.5 
        row = box.row()
        row.prop(context.scene, "texture_res", expand=True)
        row.scale_y = 1 
        
        
        if context.scene.texture_res == "Custom":
            row = box.row()
            row.prop(context.scene, "imgwidth") 
            row.prop(context.scene, "imgheight")
        

        #For now, this is CyclesBake only
        if context.scene.simplebake_global_mode == "cycles_bake":
            row = box.row()
            row.prop(context.scene, "tex_per_mat")

        if context.scene.mergedBake:
            row = box.row()
            row.prop(context.scene, "mergedBakeName")
    
        
        #--------UV Settings-------------------
        
        if bpy.context.scene.uv_mode == "udims":
            pass
        
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
        row.operator("object.simple_bake_mapbake", icon_value=self.icons["BAKE"].icon_id)
        
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
                    
            col.operator("object.simple_bake_bgbake_status", text="", icon=icon)
            col.enabled = enable
            
            # - BG import button
            
            col = row.column()
            if len(bgbake_ops.bgops_list_finished) != 0:
                enable = True
                icon = "IMPORT"
            else:
                enable = False
                icon = "IMPORT"
            
            col.operator("object.simple_bake_bgbake_import", text="", icon=icon)
            col.enabled = enable

            
            #BG erase button
            
            col = row.column()
            if len(bgbake_ops.bgops_list_finished) != 0:
                enable = True
                icon = "TRASH"
            else:
                enable = False
                icon = "TRASH"
            
            col.operator("object.simple_bake_bgbake_clear", text="", icon=icon)
            col.enabled = enable       
            
            row.alignment = 'CENTER'
            row.label(text=f"Running {len(bgbake_ops.bgops_list)} | Finished {len(bgbake_ops.bgops_list_finished)}")


        #-------------Other material options-------------------------
        layout.separator()

        column= layout.column(align= True)
        column.label(text= "Convert Material to:", icon= 'SHADING_RENDERED')
        box = column.box()

        materialCol = box.column(align=True)
        materialCol.operator('universalmaterialmap.create_template_omnipbr',
            text='OmniPBR')
        materialCol.operator('universalmaterialmap.create_template_omniglass',
            text='OmniGlass')
        
custom_icons = None       

class SimpleBakePreferences(bpy.types.AddonPreferences):
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
    ao_alias: bpy.props.StringProperty(name="AO", default="ao")
    curvature_alias: bpy.props.StringProperty(name="Curvature", default="curvature")
    thickness_alias: bpy.props.StringProperty(name="Thickness", default="thickness")
    vertexcol_alias: bpy.props.StringProperty(name="vertex Col", default="vertexcol")
    colid_alias: bpy.props.StringProperty(name="Col ID", default="colid")
    lightmap_alias: bpy.props.StringProperty(name="Lightmap", default="lightmap")
    
    @classmethod
    def reset_img_string(self):
        prefs = bpy.context.preferences.addons[__package__].preferences
        prefs.property_unset("img_name_format")
        bpy.ops.wm.save_userpref()
        
        
#---------------------Advanced object selection list -----------------------------------
class ListItem(PropertyGroup):
    """Group of properties representing an item in the list."""

    obj_point:   PointerProperty(
            name="Bake Object",
            description="An object in the scene to be baked",
            #update=obj_point_update,
            type=bpy.types.Object)

    name: StringProperty(
           name="Name",
           description="A name for this item",
           default= "Untitled")

class BAKEOBJECTS_UL_List(UIList):
    """UIList."""

    def draw_item(self, context, layout, data, item, icon, active_data,
                  active_propname, index):

        # We could write some code to decide which icon to use here...
        custom_icon = 'OBJECT_DATAMODE'

        # Make sure your code supports all 3 layout types
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.obj_point.name, icon = custom_icon)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon = custom_icon)


class LIST_OT_NewItem(Operator):
    """Add selected object(s) to the bake list"""

    bl_idname = "simplebake_bakeobjs_advanced_list.new_item"
    bl_label = "Add a new object to bake list"

    @classmethod
    def poll(cls, context):
        return len(bpy.context.selected_objects)
    
    def execute(self, context):
        #Lets get rid of the non-mesh objects
        functions.deselect_all_not_mesh()
        
        
        objs = bpy.context.selected_objects.copy()
        
        #Check all mesh. Throw error if not
        for obj in objs:
            
            if obj.type != "MESH":
                self.report({"ERROR"}, f"ERROR: Selected object '{obj.name}' is not mesh")
                return {"CANCELLED"}
        
        
        #Add if not already in the list
        for obj in objs:    
            already_present = False
            for li in context.scene.simplebake_bakeobjs_advanced_list:
                if li.obj_point == obj:
                    already_present = True
            
            if not already_present:
                #Create a new item
                n = context.scene.simplebake_bakeobjs_advanced_list.add()    
                n.obj_point = obj
                n.name = obj.name
        
        #Throw in a refresh
        functions.update_advanced_object_list()
        
        return{'FINISHED'}


class LIST_OT_DeleteItem(Operator):
    """Remove the selected object from the bake list."""

    bl_idname = "simplebake_bakeobjs_advanced_list.del_item"
    bl_label = "Deletes an item"

    @classmethod
    def poll(cls, context):
        return context.scene.simplebake_bakeobjs_advanced_list

    def execute(self, context):
        my_list = context.scene.simplebake_bakeobjs_advanced_list
        index = context.scene.simplebake_bakeobjs_advanced_list_index

        my_list.remove(index)
        context.scene.simplebake_bakeobjs_advanced_list_index = min(max(0, index - 1), len(my_list) - 1)
        
        #Throw in a refresh
        functions.update_advanced_object_list()
        
        return{'FINISHED'}


class LIST_OT_ClearAll(Operator):
    """Clear the object list"""

    bl_idname = "simplebake_bakeobjs_advanced_list.clear_all"
    bl_label = "Deletes an item"

    @classmethod
    def poll(cls, context):
        return True
        #return context.scene.simplebake_bakeobjs_advanced_list

    def execute(self, context):
        my_list = context.scene.simplebake_bakeobjs_advanced_list
        #index = context.scene.simplebake_bakeobjs_advanced_list_index
        
        #while len(context.scene.simplebake_bakeobjs_advanced_list) > 0:
            #my_list.remove(0)
        my_list.clear()
        
        #Throw in a refresh
        functions.update_advanced_object_list()
        
        
        return{'FINISHED'}



class LIST_OT_MoveItem(Operator):
    """Move an object in the list."""

    bl_idname = "simplebake_bakeobjs_advanced_list.move_item"
    bl_label = "Move an item in the list"

    direction: bpy.props.EnumProperty(items=(('UP', 'Up', ""),
                                              ('DOWN', 'Down', ""),))

    @classmethod
    def poll(cls, context):
        return context.scene.simplebake_bakeobjs_advanced_list

    def move_index(self):
        """ Move index of an item render queue while clamping it. """

        index = bpy.context.scene.simplebake_bakeobjs_advanced_list_index
        list_length = len(bpy.context.scene.simplebake_bakeobjs_advanced_list) - 1  # (index starts at 0)
        new_index = index + (-1 if self.direction == 'UP' else 1)

        bpy.context.scene.simplebake_bakeobjs_advanced_list_index = max(0, min(new_index, list_length))

    def execute(self, context):
        my_list = context.scene.simplebake_bakeobjs_advanced_list
        index = context.scene.simplebake_bakeobjs_advanced_list_index

        neighbor = index + (-1 if self.direction == 'UP' else 1)
        my_list.move(neighbor, index)
        self.move_index()
        
        #Throw in a refresh
        functions.update_advanced_object_list()
        
        return{'FINISHED'}


class LIST_OT_Refresh(Operator):
    """Refresh the list to remove objects"""

    bl_idname = "simplebake_bakeobjs_advanced_list.refresh"
    bl_label = "Refresh the list"


    @classmethod
    def poll(cls, context):
        #return context.scene.simplebake_bakeobjs_advanced_list
        return True


    def execute(self, context):
        functions.update_advanced_object_list()
        
        return{'FINISHED'}