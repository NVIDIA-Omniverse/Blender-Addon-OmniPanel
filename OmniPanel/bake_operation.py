import bpy

def bakestolist(justcount = False):
    #Assemble properties into list
    selectedbakes = []
    selectedbakes.append("diffuse") if bpy.context.scene.selected_col else False
    selectedbakes.append("metalness") if bpy.context.scene.selected_metal else False
    selectedbakes.append("roughness") if bpy.context.scene.selected_rough else False
    selectedbakes.append("normal") if bpy.context.scene.selected_normal else False
    selectedbakes.append("transparency") if bpy.context.scene.selected_trans else False
    selectedbakes.append("transparencyroughness") if bpy.context.scene.selected_transrough else False
    selectedbakes.append("emission") if bpy.context.scene.selected_emission else False
    selectedbakes.append("specular") if bpy.context.scene.selected_specular else False
    selectedbakes.append("alpha") if bpy.context.scene.selected_alpha else False
    
    selectedbakes.append("sss") if bpy.context.scene.selected_sss else False
    selectedbakes.append("ssscol") if bpy.context.scene.selected_ssscol else False
    
    if justcount:
        return len(selectedbakes)
    else:
        return selectedbakes

class BakeOperation:
    
    #Constants
    PBR = "pbr"
    PBRS2A = "pbrs2a"
    CYCLESBAKE = "cyclesbake"
    SPECIALS = "specials"
    SPECIALS_PBR_TARGET_ONLY = "specials_pbr_targetonly"
    SPECIALS_CYCLES_TARGET_ONLY = "specials_cycles_targetonly"
    
    #Specials names
    THICKNESS = "thickness"
    AO = "ambientocclusion"
    CURVATURE = "curvature"
    COLOURID = "colid"
    VERTEXCOL = "vertexcol"
    LIGHTMAP = "lightmap"
    
    
    def __init__(self):
        self.udim_counter = 0
        
        
        #Mapping of object name to active UVs
        self.bake_mode = BakeOperation.PBR #So the example in the user prefs will work
        self.bake_objects = []
        self.active_object = None
        self.sb_target_object = None
        self.sb_target_object_cycles = None
    
        #normal, udims
        self.uv_mode = "normal"
        
        #pbr stuff
        self.pbr_selected_bake_types = []
        
        #cycles stuff
        self.cycles_bake_type = bpy.context.scene.cycles.bake_type
        
    def assemble_pbr_bake_list(self):
        self.pbr_selected_bake_types = bakestolist()
        
class MasterOperation:
    
    current_bake_operation = None
    total_bake_operations = 0
    this_bake_operation_num = 0
    
    orig_UVs_dict = {}
    baked_textures = []
    prepared_mesh_objects = []
    
    merged_bake = False
    merged_bake_name = ""
    batch_name = ""
    
    orig_s2A = False
    orig_objects = []
    orig_active_object = ""
    orig_engine = "CYCLES"
    orig_sample_count = 0
    orig_tile_x = 0
    orig_tile_y = 0
    
    
    def clear():
        MasterOperation.orig_UVs_dict = {}
        MasterOperation.total_bake_operations = 0
        MasterOperation.current_bake_operation = None
        MasterOperation.this_bake_operation_num = 0
        MasterOperation.prepared_mesh_objects = []
        MasterOperation.baked_textures = []
        MasterOperation.merged_bake = False
        MasterOperation.merged_bake_name = ""
        MasterOperation.batch_name = ""
        
        MasterOperation.orig_s2A = False
        MasterOperation.orig_objects = []
        MasterOperation.orig_active_object = ""
        MasterOperation.orig_engine = "CYCLES"
        MasterOperation.orig_sample_count = 0
        MasterOperation.orig_tile_x = 0
        MasterOperation.orig_tile_y = 0
        
        return True
    
    
class BakeStatus:
    total_maps = 0
    current_map = 0
    
        
