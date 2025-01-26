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

class HowTo(Operator):
    
    bl_idname = "object.how_to"
    bl_label = "How To...   "
    bl_description = "Click for Instructions..."
    
    def execute(self, context):
    
        bpy.ops.wm.howto('INVOKE_DEFAULT')
        
        return {"FINISHED"}


class WM_HowTo(Operator):
    bl_label = "Spawn Shop v0.7.8 - Guide"
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
        row.label(text="  or otherwise have in your Scene a sealed BSP and a 'Player Starting Locations' (PSL) collection full of Slayer spawns.")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  With that set up, clone your level geometry, remove all glass, ladders, floating panels, and any other non-collision")
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
        
        # old
#        box = layout.box()
#        row = box.row()
#        row.label(text="2. Add Spawn Spheres & Markers")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  Spawn Spheres are necessary for calculating the randoms. Spawn Markers make it easier to see during 'Gameplay")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  Simulation'. You may add a single object (to 0,0,0 in the scene), or populate every spawn point with a Marker and")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  Sphere all at once. They will be linked to their respective spawn, so if you move the parent 'Player Starting Location',")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  the Sphere and Marker will move with it. Be careful, as the inverse is not true: moving a Sphere or Marker manually")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  will not move its parent 'Player Starting Location'.")
#        row = box.row()
#        row.scale_y = 0.5
        
        box = layout.box()
        row = box.row()
        row.label(text="2. Populate The Map")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  Spawn Spheres are necessary for calculating the randoms. If you're designing a new map, you can add a single")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  Sphere (to see how the influence radius fits into your level) and a single Marker (to help identify a spawn's location")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  and orientation). Link each to a spawn point (i.e., select the new sphere, then select a 'Player Starting Location', then")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  press CTRL+P, and select 'Object (Without Inverse') so the sphere adopts that spawn point's transform). If you've")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  imported a map, or left this step until after placing spawn points, click 'Populate All Spawns' to add and link Spheres")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  and Markers to every PSL.")
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
        row.label(text="  If everything went well, you'll have a group of semi-transparent spheres and markers, and some pink surfaces")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  depicting the random zones. The last thing you need is a group of 4 Spartans to demonstrate Halo's spawn engine.")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  Click the 'Generate Spartans' button to add 2 \"players\" to each team. Then, with 'Real Time Tracking' enabled, you")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  can manually move the Spartans around the map, and watch as the Spheres (and Markers) fade in and out. You can")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  also 'kill' and respawn any player, and see how the actual game would select a spawn point. Use these features to")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  visualize team and enemy influence in 2v2 Team Slayer, and help with designing new, competitive maps.")
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