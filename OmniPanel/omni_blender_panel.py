import time
import math
from typing import Type
import bpy
import numpy as np
import multiprocessing
from contextlib import contextmanager
import os, sys



class MyProperties(bpy.types.PropertyGroup):
    deletePSystemAfterBake: bpy.props.BoolProperty(
       name = "Delete PS after converting",
       description = "Delete selected particle system after conversion",
       default = False
    )
    progressBar: bpy.props.StringProperty(
        name = "Progress",
        description = "Progress of Particle Conversion",
        default = "RUNNING"
    )
    
# Omni Link

# Omni Import
#wm.usd_import

# Omni Export
#wm.usd_export

# Omni Texture Bake
class TEXTURE_OT_omni_texture_bake(bpy.types.Operator):
    """Bake complex blender textures for omni materials"""
    bl_idname = "omni.texture_bake"
    bl_label = "Omni Texture Bake"

    def execute(self, context):
        
        print("I DON't WARK")
        return {'FINISHED'}

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout
        

# Omni Hair Bake
class PARTICLES_OT_omni_hair_bake(bpy.types.Operator):
    """Convert blender particles for Omni scene instancing"""
    bl_idname = "omni.hair_bake"
    bl_label = "Omni Hair Bake"
    bl_options = {'REGISTER', 'UNDO'}  # create undo state

    # def colInst(self, i):
    #     print("uuuuuuuuuuuuu")
        
    #     childObj = self.dups[i]
    #     modInst = i % self.count

    #     dupColName = str(self.listInst[modInst].users_collection[0].name)
    #     loc=childObj.location
    #     rot=childObj.rotation_euler
    #     newScale = np.divide(childObj.scale, self.listInstScale[modInst])

    #     #Create Collection Instance
    #     source_collection = bpy.data.collections[dupColName]
    #     instance_obj = bpy.data.objects.new(
    #         name= "Inst_" + childObj.name, 
    #         object_data=None
    #     )
    #     instance_obj.empty_display_type = 'SINGLE_ARROW'
    #     instance_obj.empty_display_size = .1
    #     instance_obj.instance_collection = source_collection
    #     instance_obj.instance_type = 'COLLECTION'
    #     instance_obj.location = loc
    #     instance_obj.rotation_euler = rot
    #     instance_obj.scale = newScale
    #     self.parentCollection.objects.link(instance_obj)
    #     instance_obj.parent = self.o

    #     bpy.data.objects.remove(childObj, do_unlink=True)


    def execute(self, context):

        # wm = context.window_manager
        # self._timer = wm.event_timer_add(0.1, window=context.window)
        # wm.modal_handler_add(self)

        mytool = context.scene.my_tool

        startTime= time.time()

        #Deselect Non-meshes
        for obj in bpy.context.selected_objects:
            if obj.type != "MESH":
                obj.select_set(False)
                print("not mesh")

        #Do we still have an active object?
        if bpy.context.active_object == None:
            #Pick arbitary
            bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
        
        for parentObj in bpy.context.selected_objects:

            countPS = 0
            
            for currentPS in parentObj.particle_systems:

                if currentPS != None:
                    bpy.ops.object.select_all(action='DESELECT')

                    renderType = currentPS.settings.render_type
                    
                    if renderType == 'OBJECT' or renderType == 'COLLECTION':

                        count = 0
                        listInst = []
                        listInstScale = []

                        # For Object Instances
                        if renderType == 'OBJECT':
                            instObj = currentPS.settings.instance_object
                            instObj.select_set(True)

                            # Duplicate Instanced Object
                            dupInst = instObj.copy()
                            #if MakeDuplicateInstance
                                #dupInst.data = instObj.data.copy()
                            bpy.context.collection.objects.link(dupInst)
                            instObj.select_set(False)
                            dupInst.location = (0,0,0)

                            bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name="INST_"+str(dupInst.name))
                            dupInst.select_set(False)
                            count += 1
                            listInst.append(dupInst)
                            listInstScale.append(instObj.scale)

                        # For Collection Instances
                        if renderType == 'COLLECTION':
                            instCol = currentPS.settings.instance_collection.objects
                            for obj in instCol:
                                obj.select_set(True)

                                # Duplicate Instanced Object
                                dupInst = obj.copy()
                                
                                #if MakeDuplicateInstance
                                    #dupInst.data = instObj.data.copy()
                                bpy.context.collection.objects.link(dupInst)
                                obj.select_set(False)
                                dupInst.location = (0,0,0)

                                bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name="INST_"+str(dupInst.name))
                                dupInst.select_set(False)
                                count += 1
                                listInst.append(dupInst)
                                listInstScale.append(obj.scale)

                        # For Path Instances
                        if renderType == 'PATH':
                            print("path no good")
                            return {'FINISHED'}


                        if renderType == 'NONE':
                            print("no instances")
                            return {'FINISHED'}

                        #if overwriteExsisting:
                            #bpy.ops.outliner.delete(hierarchy=True)

                        # Variables
                        parentObj.select_set(True)
                        parentCollection = parentObj.users_collection[0]
                        nameP = parentObj.particle_systems[0].name # get name of object's particle system

                        # Create Empty as child
                        o = bpy.data.objects.new( "empty", None)
                        o.name = "EM_" + nameP
                        o.parent = parentObj
                        parentCollection.objects.link( o )

                        bpy.ops.object.duplicates_make_real(use_base_parent=True, use_hierarchy=True) # bake particles

                        dups = bpy.context.selected_objects
                        #dupColName = str(dupInst.users_collection[0].name)

                        lengthDups = len(dups)
                    
                        #TESTING
                        # a_pool = multiprocessing.Pool()
                        # a_pool.
                        # map(self.colInst, range(lengthDups))

                        # map(PARTICLES_OT_omni_hair_bake.makeColInst, dups)

                            # for i in range(lengthDups):

                            #     loopTime= time.time()

                            #     childObj = dups[0]
                            #     modInst = i % count

                            #     dupColName = str(listInst[modInst].users_collection[0].name)
                            #     loc=childObj.location
                            #     rot=childObj.rotation_euler
                            #     newScale = np.divide(childObj.scale, listInstScale[modInst])

                            #     #Create Collection Instance
                            #     source_collection = bpy.data.collections[dupColName]
                            #     instance_obj = bpy.data.objects.new(
                            #         name= "Inst_" + childObj.name, 
                            #         object_data=None
                            #     )

                            #     print(time.time() - loopTime)
                        
                        # Handle instances for construction of scene collections **Fast**
                        for i in range(lengthDups):

                            # loopTime= time.time()

                            childObj = dups.pop(0)
                            modInst = i % count

                            dupColName = str(listInst[modInst].users_collection[0].name)
                            loc=childObj.location
                            rot=childObj.rotation_euler
                            newScale = np.divide(childObj.scale, listInstScale[modInst])

                            #Create Collection Instance
                            source_collection = bpy.data.collections[dupColName]
                            instance_obj = bpy.data.objects.new(
                                name= "Inst_" + childObj.name, 
                                object_data=None
                            )
                            instance_obj.empty_display_type = 'SINGLE_ARROW'
                            instance_obj.empty_display_size = .1
                            instance_obj.instance_collection = source_collection
                            instance_obj.instance_type = 'COLLECTION'
                            instance_obj.location = loc
                            instance_obj.rotation_euler = rot
                            instance_obj.scale = newScale
                            parentCollection.objects.link(instance_obj)
                            instance_obj.parent = o

                            bpy.data.objects.remove(childObj, do_unlink=True)
                            
                            #OLD AND SLOW
                                # bpy.ops.object.collection_instance_add(collection= dupColName, align='WORLD', location=loc, rotation=rot)
                                

                                # active = bpy.context.active_object
                                # newScale = np.divide(childObj.scale, listInstScale[modInst])
                                # active.scale = newScale # fix scale here because scale does not work when creating instance

                                # Move Collection Instances to Parent Collection
                                # if active.users_collection[0] != parentCollection:
                                #     oldCollection = bpy.context.active_object.users_collection
                                #     parentCollection.objects.link(active)
                                #     for obj in oldCollection:
                                #             obj.objects.unlink(active) # Remove from old

                                # Parent Empty
                                # o.select_set(True)
                                # bpy.context.view_layer.objects.active = o
                                # bpy.ops.object.parent_set(keep_transform=True) # make baked particles children

                                # Delete Children
                                # bpy.ops.object.select_all(action='DESELECT') # deselect all
                                # childObj.select_set(True) # select the object
                                # with suppress_stdout():
                                #     bpy.ops.object.delete() # delete object

                                # object_to_delete = bpy.data.objects[childObj.name]

                            #Progress Bar
                                # progress = 100 + (-1* math.ceil(100 - i*(100/lengthDups)))
                                # mytool.progressBar = "progress = " + str(progress) + " %"                        
                                # print (mytool.progressBar)

                            # print(time.time() - loopTime)
                            
                    
                        for obj in listInst:
                            bpy.context.view_layer.layer_collection.children[obj.users_collection[0].name].exclude = True
                            

                        parentObj.select_set(True)
                        bpy.context.view_layer.objects.active = parentObj
                    
                        if mytool.deletePSystemAfterBake:
                            pass

                        else:
                            countI = 0
                            for mod in parentObj.modifiers:
                                if mod.type == 'PARTICLE_SYSTEM':
                                    if countPS == countI:
                                        mod.show_viewport = False
                                        mod.show_render = False
                                        break
                                    else:
                                        countI += 1

                        countPS += 1
                    
                    else:
                        print("Must be object or collection instance")

                
                else:
                    print("Object has no active particle system")
            
            if mytool.deletePSystemAfterBake:
                for i in range(len(parentObj.particle_systems)):
                    bpy.ops.object.particle_system_remove()
                


        print ("My program took", time.time() - startTime, " seconds to run") # run time
        #mytool.progressBar = "COMPLETE"
        return {'FINISHED'}