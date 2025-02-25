# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2025 Kendall Starr
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# ##### END MIT LICENSE BLOCK #####

import bpy
from bpy.types import Operator
from .func import *


class GenerateRandoms(Operator):
    bl_idname = "object.generate_randoms"
    bl_label = "Generate Randoms  "
    bl_description = "Cut the spheres out of the shelled\nmap to create the randoms geometry."
    
    detail_outer = -1
    detail_inner = -1
    
    def draw(self, context):
        
        Spheres = bpy.context.scene.spheres_select
        Shell = bpy.context.scene.shell_select
        
        total_spheres = 0
        tris = 0
    
        kinda_break = "Press OK if you're heading to the bathroom."
            
        layout = self.layout
        layout.label(text="Poly Count Warning!", icon="ERROR")
                
        shell_tris = len(Shell.data.loop_triangles)
        
        if Spheres:
            for sphere in Spheres.objects:
                total_spheres += 1
                
                tris = len(sphere.data.loop_triangles)
                
                details = sphere.data.name.split("[")[1].split("]")[0].split(".")
                self.detail_outer = int(details[0])
                self.detail_inner = int(details[1])
                
                    # 3.3 = 640
                # 3.4 or 4.3 = 1600
                # 3.5 or 5.3 = 5440
                # 3.6 or 6.3 = 20800
                
                    # 4.3 = 1600
                    # 4.4 = 2560
                # 4.5 or 5.4 = 6400
                # 4.6 or 6.4 = 21760
                
                    # 5.3 = 5440
                    # 5.4 = 6400
                    # 5.5 = 10240
                # 5.6 or 6.5 = 25600
                
                    # 6.3 = 20800
                    # 6.4 = 21760
                    # 6.5 = 25600
                # 6.6 = 40960
                
                # ranges: 640, 1600, 2560, 5440, 6400, 10240, 20800, 21760, 25600, 40960
                
                # 5.4 = 6400
                if tris == 640:     # detail =  3.3
                    kinda_break = "Press OK if you're willing to unfocus your eyes for 30 seconds." # 30s
                elif tris == 1600:  # detail = 3.4 or 4.3
                    kinda_break = "Press OK if you're about to do 60 situps as fast as you can." # 45s
                elif tris == 2560:  # detail = 4.4
                    kinda_break = "Press OK if you're heading to the bathroom." # 60s
                elif tris == 5440:  # detail = 3.5 or 5.3
                    kinda_break = "Press OK if you have some emails to reply to." # 120s
                elif tris == 6400:  # detail = 4.5 or 5.4
                    kinda_break = "Press OK if you're dog needs to pee." # 180s
                elif tris == 10240: # detail = 5.5
                    kinda_break = "Press OK if you acknowledge this is a bad idea." # 240s
                elif tris == 20800: # detail = 3.6 or 6.3
                    kinda_break = "Press OK if you're about to run to the grocery store." # 360s
                elif tris == 21760: # detail = 4.6 or 6.4
                    kinda_break = "Press OK if you're about to watch a Pixar short." # 420s
                elif tris == 25600: # detail = 5.6 or 6.5
                    kinda_break = "Press OK if you're about to learn how to solve the third layer of a Rubik's cube." # 480s
                elif tris == 40960: # detail = 6.6
                    kinda_break = "Press OK if you're absolutely insane." # 600s
            
            tris_formatted = "{:,}".format(tris)
            total_tris = total_spheres * tris
            total_formatted = "{:,}".format(total_tris)
            shell_tris_formatted = "{:,}".format(shell_tris)
            
            # old
#            row = layout.row()
#            row.label(text="         You're about to boolean "+str(total_spheres)+" spheres, each with "+tris_formatted+" triangles,")
#            row = layout.row()
#            row.label(text="         for a total of "+total_formatted+" triangles, against a shell with "+shell_tris_formatted+" triangles.")
#            row = layout.row()
#            row.label(text="         Blender may stop responding during this operation!")
#            row = layout.row()
#            row.label(text="         "+kinda_break)
            
            # new
            row = layout.row()
            row.label(text="             Spheres: "+total_formatted+" Triangles ("+str(total_spheres)+" spheres × "+tris_formatted+" triangles)")
            row = layout.row()
            row.label(text="                   Shell: "+shell_tris_formatted+" Triangles")
            row = layout.row()
            row.label(text="         Blender may stop responding during this operation!")
            row = layout.row()
            row.label(text="         "+kinda_break)
            
        else: # this shouldn't happen. already protected by invoke()
            row = layout.row()
            row.label(text="         No Spheres Collection selected!")
            row = layout.row()
            row.label(text="         "+kinda_break)
            
        row = layout.row()
        
     
    def execute(self, context):       
        print("Go get a coffee.")
        sdout = self.detail_outer
        sdin = self.detail_inner
        bpy.ops.object.generate_randoms_confirm(sphere_detail_outer = sdout, sphere_detail_inner = sdin)
        return {"FINISHED"}
    
    def invoke(self, context, event):
        Spheres = bpy.context.scene.spheres_select
        spheres_collection_name = Spheres.name
        if not Spheres:
            self.report({"ERROR"},"No Spheres Collection selected!")
            return {"CANCELLED"}
        else:
            if len(Spheres.objects) == 0:
                self.report({"ERROR"},"'"+spheres_collection_name+"' collection is empty!")
                return {"CANCELLED"}
            else:
                return context.window_manager.invoke_props_dialog(self, width=400)


class GenerateRandomsConfirm(Operator):
     
    bl_idname = "object.generate_randoms_confirm"
    bl_label = "Generate Randoms  "
    bl_description = "Cut the spheres out of the shelled\nmap to create the randoms geometry."
    
    sphere_detail_outer: bpy.props.IntProperty(name="Sphere Detail Outer")
    sphere_detail_inner: bpy.props.IntProperty(name="Sphere Detail Inner")
    
    def execute(self, context):
        print("Calculating randoms...")
        
        details = str(self.sphere_detail_outer)+"."+str(self.sphere_detail_inner)
        quality = bpy.context.scene.boolean_solver_enum.boolean_solver
        
        Shell = bpy.context.scene.shell_select
        SpheresCollection = bpy.context.scene.spheres_select
        RandomsCollection = bpy.data.collections.get("Randoms")
        
        
        
        # user may have updated script, so they will have a BSP.shell, but not the
        # Randoms collection. this should fix (unless they also don't have Spawn Shop):
        if not RandomsCollection:
            SpawnShopCollection = bpy.data.collections.get("Spawn Shop")
            if not SpawnShopCollection:
                bpy.ops.wm.show_error('INVOKE_DEFAULT',message="'Spawn Shop' collection missing! Please start over.")
                return {'FINISHED'}
            
            RandomsCollection = SpawnShopCollection.children.get("Randoms")
    
            if not RandomsCollection:
                RandomsCollection = bpy.data.collections.new('Randoms')
                SpawnShopCollection.children.link(RandomsCollection)
            
        if Shell and SpheresCollection and RandomsCollection:
            print("Found Shell and Spheres!")
            bpy.ops.object.select_all(action='DESELECT') 

            # create a clone
            clone = Shell.copy()
            clone.data = Shell.data.copy()
            RandomsCollection.objects.link(clone)
            bpy.context.view_layer.objects.active = clone
            clone.select_set(True)
            clone.name = "Randoms ["+details+"]"
            
            # add the modifier
            boo = clone.modifiers.new("GenRand","BOOLEAN")
            boo.solver = quality
            boo.operand_type = 'COLLECTION'
            boo.collection = SpheresCollection
            
            # apply if user desires
            if bpy.context.scene.apply_randoms_modifier:
                bpy.ops.object.modifier_apply(modifier="GenRand")
                
            # hide the original shell
            Shell.hide_set(True)
        else:
#            print("BSP.shell not found.")
            bpy.ops.wm.show_error('INVOKE_DEFAULT',message="Please select a BSP shell and Spheres collection!")

        return {'FINISHED'}
    
    
    
classes = (
    GenerateRandoms,
    GenerateRandomsConfirm
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
