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
    
#    def draw(self, context):
#        layout = self.layout
#        box = layout.box()
#        row = box.row()
#        row.label(text="Prepare Your Environment")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  This add-on assumes you've imported a Halo 1 scenario using the \"Halo-Asset-Blender-Development-Toolset\",")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  or otherwise have in your Scene a sealed BSP and a 'Player Starting Locations' (PSL) collection full of Slayer spawns.")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  With that set up, clone your level geometry, remove all glass, ladders, floating panels, and any other non-collision")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  surfaces. Make sure the model is STL Checked (perfectly sealed, all vertices welded) with no clutter! Name this")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  stripped down BSP whatever you like, and place it wherever you like.")
#        row = box.row()
#        row.scale_y = 0.5
#        
#        box = layout.box()
#        row = box.row()
#        row.label(text="1. Shell The Map")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  Select your sealed BSP using the object picker and click the \"Shell Map\" button. This will clone your BSP again, turn")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  it into a pink skin covering all the surfaces, and place it in a new collection called 'Spawn Shop'.")
#        row = box.row()
#        row.scale_y = 0.5
#        
#        # old
##        box = layout.box()
##        row = box.row()
##        row.label(text="2. Add Spawn Spheres & Markers")
##        row = box.row()
##        row.scale_y = 0.5
##        row.label(text="  Spawn Spheres are necessary for calculating the randoms. Spawn Markers make it easier to see during 'Gameplay")
##        row = box.row()
##        row.scale_y = 0.5
##        row.label(text="  Simulation'. You may add a single object (to 0,0,0 in the scene), or populate every spawn point with a Marker and")
##        row = box.row()
##        row.scale_y = 0.5
##        row.label(text="  Sphere all at once. They will be linked to their respective spawn, so if you move the parent 'Player Starting Location',")
##        row = box.row()
##        row.scale_y = 0.5
##        row.label(text="  the Sphere and Marker will move with it. Be careful, as the inverse is not true: moving a Sphere or Marker manually")
##        row = box.row()
##        row.scale_y = 0.5
##        row.label(text="  will not move its parent 'Player Starting Location'.")
##        row = box.row()
##        row.scale_y = 0.5
#        
#        box = layout.box()
#        row = box.row()
#        row.label(text="2. Populate The Map")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  Spawn Spheres are necessary for calculating the randoms. If you're designing a new map, you can add a single")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  Sphere (to see how the influence radius fits in your level) and a single Marker (to help identify a spawn's location")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  and orientation). Link each to a spawn point (i.e., select the new sphere, then select a 'Player Starting Location', then")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  press CTRL+P, and select 'Object (Without Inverse)') so the sphere adopts that spawn point's transform. If you've")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  imported a map, or left this step until after placing spawn points, click 'Populate All Spawns' to add and link Spheres")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  and Markers to every PSL. If things get messy, delete the sphere and marker collections, click the 'Purge Orphans'")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  button to clean up the leftover mesh, and start over.")
#        row = box.row()
#        row.scale_y = 0.5
#        
#        box = layout.box()
#        row = box.row()
#        row.label(text="3. Generate Randoms")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  With the above steps completed, click the \"Generate Randoms\" button. By default, the boolean operation will use")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  'Exact' mode, which can take a couple minutes if your spheres are high-poly. 'Fast' mode has a habit of completely")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  ignoring some spheres, so unless you're just testing the process, it's highly recommended to leave 'Exact' mode")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  selected. Don't be alarmed if Blender stops responding during this step.")
#        row = box.row()
#        row.scale_y = 0.5
#        
#        box = layout.box()
#        row = box.row()
#        row.label(text="4. Gameplay Simulation")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  If everything went well, you'll have transparent spheres and markers at every spawn point, and some pink surfaces")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  depicting the random zones. The last thing you need is a group of 4 Spartans to demonstrate Halo's spawn engine.")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  Click the 'Generate Spartans' button (next to 'Auto-respawn') to add 2 \"players\" to each team.")
#        row = box.row()
#        row.scale_y = 0.5
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  Visualizing Spawn Prediction:")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  Manually hide P2 and P4 (or disable 'Auto-respawn' and 'kill' them with the provided ghost button), enable")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  'Real Time Prediction', then move P1 and P3 around the map to see how the spheres and markers fade in and out.")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  The more opaque, the more likely that location will be chosen for a spawning teammate. Note: In prediction,")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  only one team perspective can be used at a time.")
#        row = box.row()
#        row.scale_y = 0.5
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  Realistic Spawn Engine:")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  To simulate actual spawn selection, you can respawn the hidden/dead players (with the provided 'Respawn Spartan'")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  buttons) and watch where they reappear. Use these features to get a full understanding of team and enemy spawn")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  influence while designing new, competitive 2v2 maps.")
#        row = box.row()
#        row.scale_y = 0.5
##        row.label(text="  can manually move a Spartan around the map, and watch as the Spheres (and Markers) fade in and out. You can")
##        row = box.row()
##        row.scale_y = 0.5
##        row.label(text="  also 'kill' (with the provided ghost button) and respawn any player, to see how the actual game would select a")
##        row = box.row()
##        row.scale_y = 0.5
##        row.label(text="  spawn point. If you want to simplify the experience, you can manually hide 3 of the Spartans, which will remove")
##        row = box.row()
##        row.scale_y = 0.5
##        row.label(text="  them from consideration when calculating spawns, as if they are dead. These features allow you to visualize team")
##        row = box.row()
##        row.scale_y = 0.5
##        row.label(text="  and enemy spawn influence while designing new, competitive 2v2 maps.")
##        row = box.row()
##        row.scale_y = 0.5
#        
#        #  If everything went well, you'll have transparent spheres and markers at every spawn point, and some pink surfaces 
#        #  depicting the random zones. The last thing you need is a group of 4 Spartans to demonstrate Halo's spawn engine.
#        #  Click the 'Generate Spartans' button to add 2 \"players\" to each team.

#        # Visualizing Prediction:
#        #      Manually hide P2 and P4 (or disable 'Auto-respawn' and 'kill' them with the provided ghost button), enable
#        #      'Real Time Prediction', then move P1 and P3 around the map to see how the spheres and markers fade in and out.
#        #      The more opaque, the more likely that location will be chosen for a spawning teammate. Note: In prediction,
#        #      only one team perspective can be used at a time.

#        # Spawn Engine
#        #      To simulate actual spawn selection, you can respawn the hidden/dead players (with the provided 'Respawn Spartan'
#        #      buttons) and watch where they reappear. Use these features to get a full understanding of team and enemy spawn
#        #      influence while designing new, competitive 2v2 maps.
#    
#    def execute(self, context):
#        
#        print("Thanks for coming to my TED Talk")
#        
#        return {"FINISHED"}
#    
#    def invoke(self, context, event):
#        
#        return context.window_manager.invoke_props_dialog(self, width=640)
    
    def draw(self, context):
        layout = self.layout
        box = layout.box()
        row = box.row()
        row.label(text="Prepare Your Environment")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  This add-on assumes you've imported a Halo 1 scenario using the \"Halo-Asset-Blender-Development-Toolset\", or otherwise have")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  in your Scene a sealed BSP and a 'Player Starting Locations' (PSL) collection full of Slayer spawns. With that setup, clone your level")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  geometry, remove all glass, ladders, floating panels, and any other non-collision surfaces. Make sure the model is STL Checked")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  (perfectly sealed, all vertices welded) with no clutter! Name this stripped down BSP whatever you like, and place it wherever you like.")
        row = box.row()
        row.scale_y = 0.5
        
        box = layout.box()
        row = box.row()
        row.label(text="1. Shell The Map")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  Select your sealed BSP using the object picker and click the \"Shell Map\" button. This will clone your BSP again, turn it into a pink")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  skin covering all the surfaces, and place it in a new collection called 'Spawn Shop'.")
        row = box.row()
        row.scale_y = 0.5
        
        box = layout.box()
        row = box.row()
        row.label(text="2. Populate The Map")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  Spawn Spheres are necessary for calculating the randoms. If you're designing a new map, you can add a single Sphere (to see how")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  the influence radius fits in your level) and a single Marker (to help identify a spawn's location and orientation). Link them to a spawn")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  point: select the sphere or marker first, then select a 'Player Starting Location', press CTRL+P, choose 'Object (Without Inverse)'.")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  The sphere will adopt that spawn point's transform. If you've imported a map, or left this step until after placing spawn points,")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  click 'Populate All Spawns' to add and link Spheres and Markers to every PSL. If things get messy, delete the sphere and marker")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  collections, click the 'Purge Orphans' button to clean up the leftover mesh, and start over.")
        row = box.row()
        row.scale_y = 0.5
        
        box = layout.box()
        row = box.row()
        row.label(text="3. Generate Randoms")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  With the above steps completed, click the \"Generate Randoms\" button. By default, the boolean operation will use 'Exact' mode, which can")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  take a couple minutes if your spheres are high-poly. 'Fast' mode has a habit of completely ignoring some spheres, so unless you're just")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  the process, it's highly recommended to leave 'Exact' mode selected. Don't be alarmed if Blender stops responding during this step.")
        row = box.row()
        row.scale_y = 0.5
        
        box = layout.box()
        row = box.row()
        row.label(text="4. Gameplay Simulation")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  If everything went well, you'll have transparent spheres and markers at every spawn point, and some pink surfaces depicting the")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  random zones. The last thing you need is a group of 4 Spartans to demonstrate Halo's spawn engine. Click the 'Generate Spartans'")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  button (next to 'Auto-respawn') to add 2 \"players\" to each team.")
        row = box.row()
        row.scale_y = 0.5
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  Visualizing Spawn Prediction:")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  Manually hide P2 and P4 (or disable 'Auto-respawn' and 'kill' them with the provided ghost buttons), enable 'Real Time Prediction',")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  then move P1 and P3 around the map to see how the spheres and markers fade in and out. The more opaque, the more likely that")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  location will be chosen for a spawning teammate. Note: In prediction mode, only one team perspective can be used at a time.")
        row = box.row()
        row.scale_y = 0.5
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  Realistic Spawn Engine:")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  To see actual spawn selection in action, you can respawn the dead (hidden) players (with the provided 'Respawn' buttons) and")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  watch where they reappear. Use these features to get a full understanding of team and enemy spawn influence while designing")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  new, competitive 2v2 maps.")
        row = box.row()
        row.scale_y = 0.5
#        row.label(text="  also 'kill' (with the provided ghost button) and respawn any player, to see how the actual game would select a")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  spawn point. If you want to simplify the experience, you can manually hide 3 of the Spartans, which will remove")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  them from consideration when calculating spawns, as if they are dead. These features allow you to visualize team")
#        row = box.row()
#        row.scale_y = 0.5
#        row.label(text="  and enemy spawn influence while designing new, competitive 2v2 maps.")
#        row = box.row()
#        row.scale_y = 0.5
        
        #  If everything went well, you'll have transparent spheres and markers at every spawn point, and some pink surfaces 
        #  depicting the random zones. The last thing you need is a group of 4 Spartans to demonstrate Halo's spawn engine.
        #  Click the 'Generate Spartans' button to add 2 \"players\" to each team.

        # Visualizing Prediction:
        #      Manually hide P2 and P4 (or disable 'Auto-respawn' and 'kill' them with the provided ghost button), enable
        #      'Real Time Prediction', then move P1 and P3 around the map to see how the spheres and markers fade in and out.
        #      The more opaque, the more likely that location will be chosen for a spawning teammate. Note: In prediction,
        #      only one team perspective can be used at a time.

        # Spawn Engine
        #      To simulate actual spawn selection, you can respawn the hidden/dead players (with the provided 'Respawn Spartan'
        #      buttons) and watch where they reappear. Use these features to get a full understanding of team and enemy spawn
        #      influence while designing new, competitive 2v2 maps.
    
    def execute(self, context):
        
        print("Thanks for coming to my TED Talk")
        
        return {"FINISHED"}
    
    def invoke(self, context, event):
        
        return context.window_manager.invoke_props_dialog(self, width=724)


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