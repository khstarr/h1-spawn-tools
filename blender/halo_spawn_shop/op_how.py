import bpy
from bpy.types import Operator

class HowTo(Operator):
    
    bl_idname = "object.how_to"
    bl_label = "How To...   "
    bl_description = "Click for Instructions..."
    
    def execute(self, context):
        
        print("do we have a scale model selected?",bpy.context.scene.scale_model.halo_one_scale_model_char)
        i = int(bpy.context.scene.scale_model.halo_one_scale_model_char)
        ch = str(i+1)
        bpy.context.scene.scale_model.halo_one_scale_model_char = ch
    
        bpy.ops.wm.howto('INVOKE_DEFAULT')
        
        return {"FINISHED"}


class WM_HowTo(Operator):
    bl_label = "Spawn Shop v0.7.0 - Guide"
    bl_idname = "wm.howto"
    
    def draw(self, context):
        layout = self.layout
        box = layout.box()
        row = box.row()
        row.label(text="Prepare Your Environment")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  This add-on assumes you've imported a Halo 1 scenario using the \"Halo-Asset-Blender-Development-Toolset\",")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  or otherwise have in your Scene a sealed BSP, a 'Player Starting Locations' collection full of Slayer spawns, and two")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  scale model Spartans (which can be generated using the \"Scale Model Helper\" in the aforementioned toolset). Once")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  you have that, clone your level geometry, remove all glass, ladders, floating panels, and any other non-collision")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  surfaces. Make sure the model is STL Checked (perfectly sealed, all vertices welded) with no clutter! Name this")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  stripped down BSP whatever you like, and place it wherever you like.")
        row = box.row()
        row.scale_y = 0.5
        
        box = layout.box()
        row = box.row()
        row.label(text="1. Shell The Map")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  Select your sealed BSP using the object picker and click the \"Shell Map\" button. This will clone your BSP again, turn")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  it into a pink shell covering all the surfaces, and place it in a new collection called 'Spawn Shop'.")
        row = box.row()
        row.scale_y = 0.5
        
        box = layout.box()
        row = box.row()
        row.label(text="2. Add Spawn Spheres & Markers")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  Spawn Spheres are necessary for calculating the randoms. Spawn Markers make it easier to see during 'Gameplay")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  Simulation'. You may add a single object (to 0,0,0 in the scene), or populate every spawn point with a Marker and")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  Sphere all at once. They will be linked to their respective spawn, so if you move the parent 'Player Starting Location',")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  the Sphere and Marker will move with it. Be careful, as the inverse is not true: moving a Sphere or Marker manually")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  will not move its parent 'Player Starting Location'.")
        row = box.row()
        row.scale_y = 0.5
        
        box = layout.box()
        row = box.row()
        row.label(text="3. Generate Randoms")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  With the above steps completed, click the \"Generate Randoms\" button. By default, the boolean operation will use")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  'Exact' mode, which can take a couple minutes if your spheres are high-poly. 'Fast' mode has a habit of completely")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  ignoring some spheres, so unless you're just testing the process, it's highly recommended to leave 'Exact' mode")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  selected. Don't be alarmed if Blender stops responding during this step.")
        row = box.row()
        row.scale_y = 0.5
        
        box = layout.box()
        row = box.row()
        row.label(text="4. Gameplay Simulation")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  If everything went well, you'll have a bunch of semi-transparent spheres, and some pink surfaces depicting the")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  random zones. Select your 'Team' and 'Enemy' Spartan objects (Hint: name them 'blue_player' and 'red_player' and")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  hit the \"Paint Spartans\" button), then move them around the map with the 'Real Time Tracking' option selected.")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  You should see the Spheres and Markers fading in and out in correspondence with the Spartan locations. Use this")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  feature to visualize teammate and enemy spawn influence in 2v2 Team Slayer, and to help with designing new")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  competitive maps.")
        row = box.row()
        row.scale_y = 0.5    
    
    def execute(self, context):
        
        print("Thanks for coming to my TED Talk")
        
        return {"FINISHED"}
    
    def invoke(self, context, event):
        
        return context.window_manager.invoke_props_dialog(self, width=640)


classes = (
    HowTo,
    WM_HowTo
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
        
def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)