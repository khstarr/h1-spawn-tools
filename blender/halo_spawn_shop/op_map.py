# License

import bpy
from bpy.types import Operator

from .func import *


class ShellMap(Operator):
    
    bl_idname = "object.shell_map"
    bl_label = "Shell Map     "
    bl_description = "Clones the selected BSP and\nthickens all the surfaces."
    
    def execute(self, context):
        
        print("Heller from the sheller!")
        
        selected_bsp = bpy.context.scene.bsp_select            
                       
        if selected_bsp is not None:
            print("found map:",selected_bsp.name)
            
            # set up shop
            SpawnShopCollection = bpy.context.scene.collection.children.get("Spawn Shop")
            
            if(SpawnShopCollection):
                print("Spawn Shop container already exists!")
            else:
                SpawnShopCollection = bpy.data.collections.new("Spawn Shop")
                bpy.context.scene.collection.children.link(SpawnShopCollection)
                            
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
            
            pink = bpy.data.materials.new(name="PinkShell")
            pink.use_nodes = True
            prin = pink.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
            prin.inputs['Base Color'].default_value = (1, 0.2, 0.9, 1) # Pink color
            prin.inputs['Alpha'].default_value = 0.25 # Transparency
            mo = pink.node_tree.nodes.get('Material Output')
            pink.node_tree.links.new(prin.outputs['BSDF'], mo.inputs['Surface'])

            shelled.data.materials.append(pink)
            
            bpy.context.object.active_material.surface_render_method = 'BLENDED'
            
            clone.name = "BSP.shell"
            clone.data.name = "BSP_Mesh"
            
            # MOVE CLONED / SHELLED MAP TO Spawn Shop
            bpy.context.scene.collection.objects.unlink(clone)
            SpawnShopCollection.objects.link(clone)
        else:
            self.report({'ERROR'}, "Please select a BSP!")
            
        return {"FINISHED"}



######################################################################################################################
###
###   GENERATE RANDOMS GEOMETRY
###







######################################################################################################################
###
###   EXTRA BUTTONS
###   
  

    







classes = (
#    SpawnScenery,
    ShellMap,
#    GenerateRandoms,
#    GenerateRandomsConfirm
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
#    bpy.types.Scene.apply_randoms_modifier = bpy.props.BoolProperty(
#        name = "Apply",
#        description = "Apply the modifier when the boolean operation\ncompletes, or leave unchecked to tweak settings.",
#        default = True
#    )
#    bpy.types.Scene.use_exact = bpy.props.BoolProperty(
#        name = "Exact",
#        description = "Uncheck for testing in 'Fast' mode, which\nis much quicker, but notably unreliable.",
#        default = True
#    )

def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
    
    del bpy.types.Scene.bsp_select
    del bpy.types.Scene.apply_solidify_modifier
    
#    del bpy.types.Scene.apply_randoms_modifier
#    del bpy.types.Scene.use_exact
