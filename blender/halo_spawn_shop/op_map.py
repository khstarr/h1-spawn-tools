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


class ShellMap(Operator):
    
    bl_idname = "object.shell_map"
    bl_label = "Shell Map     "
    bl_description = "Clones the selected BSP and\nthickens all the surfaces."
    
    def execute(self, context):
        
        print("Shelling the map...")
        
        selected_bsp = bpy.context.scene.bsp_select            
                       
        if selected_bsp is not None:
            print("found map:",selected_bsp.name)
            
            # set up shop
            SpawnShopCollection = bpy.data.collections.get("Spawn Shop")
            if(SpawnShopCollection):
                print("Spawn Shop container already exists!")
            else:
                SpawnShopCollection = bpy.data.collections.new("Spawn Shop")
                bpy.context.scene.collection.children.link(SpawnShopCollection)
                
            RandomsCollection = SpawnShopCollection.children.get("Randoms")
            if RandomsCollection:
                print("'Randoms' collection already exists!")
            else:
                RandomsCollection = bpy.data.collections.new('Randoms')
                SpawnShopCollection.children.link(RandomsCollection)
                            
            clone = selected_bsp.copy()
            clone.data = selected_bsp.data.copy()
            
            bpy.context.scene.collection.objects.link(clone)
            
            bpy.context.view_layer.objects.active = clone
            clone.select_set(True)
            
            mod = clone.modifiers.new("Solidificus","SOLIDIFY")
            
            # simple
#            mod.thickness = -10
#            bpy.ops.object.modifier_apply(modifier="Solidificus")            

            # complex
            mod.solidify_mode = "NON_MANIFOLD"
            mod.nonmanifold_thickness_mode = "CONSTRAINTS"
            mod.thickness = 2
            mod.offset = 1
            mod.thickness_clamp = 2
            if(bpy.context.scene.apply_solidify_modifier):
                bpy.ops.object.modifier_apply(modifier="Solidificus")

            ### Solidify Settings ###
            # Mode: Complex
            # Thickness Mode: Constraints
            # Boundary: None
            # Thickness: 2 m
            # Offset: 1.0000
            # Merge Threshold: 0.00001 m
            # Rim: [x] Fill
            #      [ ] Only Rim
            # Thickness Clamp:
            #      Clamp: 2.000000
            #      [ ] Angle Clamp

            # Remove all material slots 
            shelled = bpy.context.active_object           
            shelled.data.materials.clear()
            
            shell_mat = bpy.data.materials.get("Shell")
            if(shell_mat):
                print("Shell material already exists!")
            else:
                shell_mat = bpy.data.materials.new(name="Shell")
                shell_mat.use_nodes = True
            
            ntree = shell_mat.node_tree
            bsdf = ntree.nodes.get("Principled BSDF", None)
            if bsdf is None:
                bsdf = shell_mat.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
                
            bsdf = shell_mat.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
            bsdf.inputs['Base Color'].default_value = (1, 0.2, 0.9, 1) # Pink color
            bsdf.inputs['Alpha'].default_value = 0.25 # Transparency
            output = shell_mat.node_tree.nodes.get('Material Output')
            shell_mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

            shelled.data.materials.append(shell_mat)
            
            bpy.context.object.active_material.surface_render_method = 'BLENDED'
            
            clone.name = "BSP.shell"
            clone.data.name = "shell_mesh"
            
            # MOVE CLONED / SHELLED MAP TO Randoms colletion
            bpy.context.scene.collection.objects.unlink(clone)
            RandomsCollection.objects.link(clone)
            
            # select the new object for the randoms boolean
            bpy.context.scene.shell_select = clone
            
        else:
            self.report({'ERROR'}, "Please select a BSP!")
            
        return {"FINISHED"}


classes = (
    ShellMap, # not iterable unless there's a comma. wow.
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.bsp_select = bpy.props.PointerProperty(
        name = "",
        description = "Please select a perfect manifold (STL Checked)\nsealed world. No holes (or it won't shell nicely)!",
        type = bpy.types.Object
    )
    bpy.types.Scene.apply_solidify_modifier = bpy.props.BoolProperty(
        name = "Apply",
        description = "Apply the modifier when the 'Solidify' operation\ncompletes, or leave unchecked to tweak settings.",
        default = True
    )

def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
    
    del bpy.types.Scene.bsp_select
    del bpy.types.Scene.apply_solidify_modifier

