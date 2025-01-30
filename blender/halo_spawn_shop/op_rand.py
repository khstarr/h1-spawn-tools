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
        
#        sphere = bpy.data.objects.get("Sample Sphere")
#        SpawnShop = bpy.data.collections.get("Spawn Shop")
        Spheres = bpy.data.collections.get("Spawn Spheres")
        
        total_spheres = 0
        tris = 0
    
        kinda_break = "Press OK if you're heading to the bathroom."
        
        for sphere in Spheres.objects:
            total_spheres += 1
            
            tris = len(sphere.data.loop_triangles)
            
            details = sphere.data.name.split("[")[1].split("]")[0].split(".")
            self.detail_outer = int(details[0])
            self.detail_inner = int(details[1])
            
            # this will be broken now... if we allow inner detail adjustment
            # maybe just do triangle ranges, instead of exact?
            # 4.3 = 1600
            # 4.4 = 2560
            # 5.4 = 6400
            if tris == 640:
#                self.detail_outer = 3
                kinda_break = "Press OK if you're willing to unfocus your eyes for 30 seconds."
            elif tris == 2560:
#                self.detail_outer = 4
                kinda_break = "Press OK if you're heading to the bathroom."
            elif tris == 10240:
#                self.detail_outer = 5
                kinda_break = "Press OK if you acknowledge this is a bad idea."
            elif tris == 40960:
#                self.detail_outer = 6
                kinda_break = "Press OK if you're absolutely insane."
        
        tris_formatted = "{:,}".format(tris)
        
        layout = self.layout
        layout.label(text="Warning!", icon="ERROR")
        
#        if total_spheres > 0:
        row = layout.row()
        row.label(text="         You're about to boolean "+str(total_spheres)+" spheres, each with "+tris_formatted+" triangles.") 
        row = layout.row()
        row.label(text="         Blender may stop responding during this operation!")        
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
        Spheres = bpy.data.collections.get("Spawn Spheres")
        if not Spheres:
            self.report({"ERROR"},"Could not find 'Spawn Spheres' collection!")
            return {"CANCELLED"}
        else:
            if len(Spheres.objects) == 0:
                self.report({"ERROR"},"'Spawn Spheres' collection is empty!")
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

        detail_outer = self.sphere_detail_outer
        detail_inner = self.sphere_detail_inner
        
        found = False
        
#        SpawnShopCollection = bpy.context.scene.collection.children.get("Spawn Shop")
        SpawnShopCollection = bpy.data.collections.get("Spawn Shop")
#        SpawnSpheresCollection = SpawnShopCollection.children.get("Spawn Spheres")
        SpawnSpheresCollection = bpy.data.collections.get("Spawn Spheres")
        
#        required_collections = 2
#        found_collections = 0
        
        # the confirm box should have already protected against these not being found        
#        if SpawnShopCollection is not None:
#            print("'Spawn Shop' collection already exists, which is good. Proceeding.")
#            found_collections += 1
#        else:
#            self.report({'ERROR'}, "Could not find 'Spawn Shop' collection!\nPlease run 'Shell Map' and 'Populate All Spawns' first.")
#        
#        if(SpawnSpheresCollection):
#            print("'Spawn Spheres' collection already exists. Proceeding.")
#            found_collections += 1
#        else:
#            self.report({'ERROR'}, "Could not find 'Spawn Spheres' collection!\nPlease run 'Shell Map' and 'Populate All Spawns' first.")
#            
#        if(found_collections == required_collections):
#            print("Found all collections. Can proceed.")
#        else:
#            print("Some collections missing. Cannot proceed.")
        
        shelled_bsp = None
        for obx in SpawnShopCollection.objects:
            if obx.name == "BSP.shell":
                bpy.context.view_layer.objects.active = obx
                obx.select_set(True)
                shelled_bsp = obx
                
        quality = bpy.context.scene.boolean_solver_enum.boolean_solver
#        if(bpy.context.scene.use_exact):
#            quality = 'EXACT'
        
        
        if(shelled_bsp is not None):
            print("Found shelled!")
            bpy.ops.object.select_all(action='DESELECT')           
            found = True
            bpy.context.view_layer.objects.active = shelled_bsp
            shelled_bsp.select_set(True)
            boo = shelled_bsp.modifiers.new("Bootilt","BOOLEAN")
            boo.solver = quality
            boo.operand_type = 'COLLECTION'
            boo.collection = SpawnSpheresCollection
            shelled_bsp.name = "BSP.shell.rand."+str(detail_outer)+"."+str(detail_inner)
            if(bpy.context.scene.apply_randoms_modifier):
                bpy.ops.object.modifier_apply(modifier="Bootilt")
        else:
#            print("BSP.shell not found.")
            bpy.ops.wm.show_error('INVOKE_DEFAULT',message="'BSP.shell' not found! Please run [Shell Map] first.")

            
        
        return {'FINISHED'}
    
    
    
classes = (
    GenerateRandoms,
    GenerateRandomsConfirm
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    
    bpy.types.Scene.apply_randoms_modifier = bpy.props.BoolProperty(
        name = "Apply",
        description = "Apply the modifier when the boolean operation\ncompletes, or leave unchecked to tweak settings.",
        default = True
    )
    bpy.types.Scene.shell_select = bpy.props.PointerProperty(
        name = "",
        description = "Select the shelled BSP created in Step 1",
        type = bpy.types.Object
    )
    bpy.types.Scene.spheres_select = bpy.props.PointerProperty(
        name = "",
        description = "Select the collection of Spawn Spheres to cut from the shell.",
        type = bpy.types.Collection
    )
    
#    bpy.types.Scene.use_exact = bpy.props.BoolProperty(
#        name = "Exact",
#        description = "Uncheck for testing in 'Fast' mode, which\nis much quicker, but notably unreliable.",
#        default = True
#    )

def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
        
    del bpy.types.Scene.apply_randoms_modifier
    del bpy.types.Scene.spheres_select
    del bpy.types.Scene.shell_select
#    del bpy.types.Scene.use_exact
