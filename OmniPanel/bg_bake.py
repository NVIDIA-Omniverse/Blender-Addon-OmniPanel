import bpy
import os

#p list
#   object representing the OS process
#   bool copy object and apply
#   bool hide objects


class bgbake_ops():
    bgops_list = []
    bgops_list_last = []
    bgops_list_finished = []

def remove_dead():
    
    #Remove dead processes from current list
    for p in bgbake_ops.bgops_list:
        if p[0].poll() == 0:
            #if p[1] is True:
                #Only go to finished list if true (i.e. prepmesh was selected)
                #bgbake_ops.bgops_list_finished.append(p)
            
            bgbake_ops.bgops_list_finished.append(p)
            bgbake_ops.bgops_list.remove(p)
    
    return 1 #1 second timer
    
bpy.app.timers.register(remove_dead, persistent=True)


# def check_merged_bake_setting():
    
    # if bpy.context.scene.simplebake_advancedobjectselection:
        # if len(bpy.context.scene.simplebake_bakeobjs_advanced_list) < 2 and bpy.context.scene.mergedBake == True:
            # bpy.context.scene.mergedBake = False

    
    # else:
        # if len(bpy.context.selected_objects)<2 and bpy.context.scene.mergedBake == True:
            # bpy.context.scene.mergedBake = False

    # return 1 #1 second timer

# bpy.app.timers.register(check_merged_bake_setting, persistent=True)

def check_export_col_setting():
    
    if (bpy.context.scene.cycles.bake_type == "NORMAL" or not bpy.context.scene.saveExternal) and bpy.context.scene.exportcyclescolspace:
        bpy.context.scene.exportcyclescolspace = False

    return 1 #1 second timer

bpy.app.timers.register(check_export_col_setting, persistent=True)

