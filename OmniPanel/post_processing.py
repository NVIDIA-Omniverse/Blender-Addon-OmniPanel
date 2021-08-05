import bpy
from pathlib import Path
import tempfile
import shutil
import os


def post_process(internal_img_name, path_dir="", path_filename="", file_format="OPEN_EXR", save=False, mode="3to1", **args):
    
    #Import the compositing scene that we need
    path = os.path.dirname(__file__) + "/compositing/compositing.blend\\Scene\\"
    
    if mode == "1to1":
        bpy.ops.wm.append(filename="SBCompositing_1to1", directory=path)
        
        scene = bpy.data.scenes["SBCompositing_1to1"]
        nodes = scene.node_tree.nodes
        
        #Set the input
        nodes["input_img"].image = args["input_img"]
        
        #The inverts all start muted
        if "invert_r_input" in args and args["invert_r_input"]: nodes["invert_r_input"].mute = False
        if "invert_g_input" in args and args["invert_g_input"]: nodes["invert_g_input"].mute = False
        if "invert_b_input" in args and args["invert_b_input"]: nodes["invert_b_input"].mute = False
        if "invert_a_input" in args and args["invert_a_input"]: nodes["invert_a_input"].mute = False
        
        if "invert_combined" in args and args["invert_combined"]: nodes["invert_combined"].mute=False
        
    
    if mode == "3to1":
        bpy.ops.wm.append(filename="SBCompositing_3to1", directory=path)
        
        scene = bpy.data.scenes["SBCompositing_3to1"]
        node_tree = scene.node_tree
        nodes = node_tree.nodes
        
        #Set the inputs
        if "input_r" in args: nodes["input_r"].image = args["input_r"]
        if "input_g" in args: nodes["input_g"].image = args["input_g"]
        if "input_b" in args: nodes["input_b"].image = args["input_b"]
        if "input_a" in args: nodes["input_a"].image = args["input_a"]
        
        #Alpha Premul
        if "alpha_convert" in args and args["alpha_convert"] == "straight":
            nodes["alpha_convert"].mute = False
            nodes["alpha_convert"].mapping = "PREMUL_TO_STRAIGHT"
        elif "alpha_convert" in args and args["alpha_convert"] == "premul":
            nodes["alpha_convert"].mute = False
            nodes["alpha_convert"].mapping = "STRAIGHT_TO_PREMUL"
        else:
            #Leave it muted
            pass
            
        
        #The inverts all start muted
        if "invert_r_input_r" in args and args["invert_r_input_r"]: nodes["invert_r_input_r"].mute = False
        if "invert_r_input_g" in args and args["invert_r_input_g"]: nodes["invert_r_input_g"].mute = False
        if "invert_r_input_b" in args and args["invert_r_input_b"]: nodes["invert_r_input_b"].mute = False
        if "invert_r_input_a" in args and args["invert_r_input_a"]: nodes["invert_r_input_a"].mute = False
        
        if "invert_g_input_r" in args and args["invert_g_input_r"]: nodes["invert_g_input_r"].mute = False
        if "invert_g_input_g" in args and args["invert_g_input_g"]: nodes["invert_g_input_g"].mute = False
        if "invert_g_input_b" in args and args["invert_g_input_b"]: nodes["invert_g_input_b"].mute = False
        if "invert_g_input_a" in args and args["invert_g_input_a"]: nodes["invert_g_input_a"].mute = False
        
        if "invert_b_input_r" in args and args["invert_b_input_r"]: nodes["invert_b_input_r"].mute = False
        if "invert_b_input_g" in args and args["invert_b_input_g"]: nodes["invert_b_input_g"].mute = False
        if "invert_b_input_b" in args and args["invert_b_input_b"]: nodes["invert_b_input_b"].mute = False
        if "invert_b_input_a" in args and args["invert_b_input_a"]: nodes["invert_b_input_a"].mute = False
        
        if "invert_a_input_r" in args and args["invert_a_input_r"]: nodes["invert_a_input_r"].mute = False
        if "invert_a_input_g" in args and args["invert_a_input_g"]: nodes["invert_a_input_g"].mute = False
        if "invert_a_input_b" in args and args["invert_a_input_b"]: nodes["invert_a_input_b"].mute = False
        if "invert_a_input_a" in args and args["invert_a_input_a"]: nodes["invert_a_input_a"].mute = False
        
        #Isolate the input channels
        if "isolate_input_r" in args and args["isolate_input_r"]:
            node_tree.links.remove(nodes["Combine RGBA.002"].inputs["G"].links[0])
            node_tree.links.remove(nodes["Combine RGBA.002"].inputs["B"].links[0])
            node_tree.links.remove(nodes["Combine RGBA.002"].inputs["A"].links[0])
            nodes["Combine RGBA.002"].mute=True
        if "isolate_input_g" in args and args["isolate_input_g"]:
            node_tree.links.remove(nodes["Combine RGBA.003"].inputs["R"].links[0])
            node_tree.links.remove(nodes["Combine RGBA.003"].inputs["B"].links[0])
            node_tree.links.remove(nodes["Combine RGBA.003"].inputs["A"].links[0])
            nodes["Combine RGBA.003"].mute=True
        if "isolate_input_b" in args and args["isolate_input_b"]:
            node_tree.links.remove(nodes["Combine RGBA.004"].inputs["R"].links[0])
            node_tree.links.remove(nodes["Combine RGBA.004"].inputs["G"].links[0])
            node_tree.links.remove(nodes["Combine RGBA.004"].inputs["A"].links[0])
            nodes["Combine RGBA.004"].mute=True
    
    #Disable the BW nodes
    if "mute_bws" in args and args["mute_bws"]:
        bw_nodes = [node for node in nodes if node.bl_idname == "CompositorNodeRGBToBW"]
        for node in bw_nodes:
            node.mute=True
        
        
    #Set the output resolution of the scene to the texture size we are using
    scene.render.resolution_y = bpy.context.scene.imgheight
    scene.render.resolution_x = bpy.context.scene.imgwidth
        
    
    #Render to temp file for the internal image
    tmpdir = Path(tempfile.mkdtemp())
    scene.render.filepath = str(tmpdir / path_filename)
    #Let's always do this an EXR
    scene.render.image_settings.file_format = "OPEN_EXR"
    bpy.ops.render.render(animation=False, write_still=True, use_viewport=False, scene=scene.name)


    #Reload the temp file into an internal image again
    img = bpy.data.images.load(str(tmpdir / path_filename)+"."+"exr")

    #Make sure that image is non-color for now
    img.colorspace_settings.name = "Non-Color"

    #Pack image, so we don't lose it when we delete the temp file
    img.pack()

    #Rename internal image
    img.name = internal_img_name

    #Delete the external tmp file
    shutil.rmtree(str(tmpdir))    

    if save:
        #Render to output file, if we are saving extnerally
        scene.render.filepath = str(path_dir / path_filename)
        
        #Set file format to requested
        scene.render.image_settings.file_format = file_format
        
        #Turn off compression and adjust other settings
        scene.render.image_settings.color_mode = "RGBA"
        
        #Always use the max bit depth that we can
        if file_format == "OPEN_EXR":
            scene.render.image_settings.color_depth = "32"
            
        elif file_format != "TARGA": #Tga cannot be 16bit. But PNG can.
            scene.render.image_settings.color_depth = "16"
        scene.render.image_settings.compression = 0
        
        #Save
        bpy.ops.render.render(animation=False, write_still=True, use_viewport=False, scene=scene.name)


    #Delete the new scene
    bpy.data.scenes.remove(scene)
    
    
    return True
    
    
    
    

