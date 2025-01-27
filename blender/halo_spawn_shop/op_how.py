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
    bl_label = "Spawn Shop v0.8.4 - Guide"
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
        row.label(text="  or otherwise have in your Scene a sealed BSP and a 'Player Starting Locations' collection full of Slayer spawns. The")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  basic process for producing spawn spheres and 'randoms' geometry is outlined below. For a more in-depth look")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  and detailed explanations, click the (?) icon to the right of each section of the Add-on panel.")
        row = box.row()
        row.scale_y = 0.5
        
#        header, panel = layout.panel("stm", default_closed=True)
#        header.label(text="1. Shell The Map")
#        if panel:
#            box = panel.box()
#            row = box.row()
#            row = box.row()
#            row.scale_y = 0.5
#            row.label(text="  Select your sealed BSP using the object picker and click the [Shell Map] button. This will clone your BSP again, turn it into a pink")
#            row = box.row()
#            row.scale_y = 0.5
#            row.label(text="  skin covering all the surfaces, and place it in a new collection called 'Spawn Shop'.")
#            row = box.row()
#            row.scale_y = 0.5
            
                    
        header, panel = layout.panel("stm", default_closed=True)
        header.label(text="1. Shell The Map")
        if panel:
            box = panel.box()
            row = box.row()
            row = box.row()
            row.scale_y = 0.5
            row.label(text="  Clone and simplify your level geometry by removing ladders, glass, and non-collision surfaces. Weld all clusters")
            row = box.row()
            row.scale_y = 0.5
            row.label(text="  and vertices together. 'Shell' the BSP to paint it pink.")
            row = box.row()
            row.scale_y = 0.5

        
#        header, panel = layout.panel("ptm", default_closed=True)
#        header.label(text="2. Populate The Map")
#        if panel:
#            box = panel.box()
#            row = box.row()
#            row = box.row()
#            row.scale_y = 0.5
#            row.label(text="  Spawn Spheres are necessary for calculating the randoms. If you're designing a new map, you can add single Spheres and Markers")
#            row = box.row()
#            row.scale_y = 0.5
#            row.label(text="  (to see how the influence radius fits in your level, and to help identify a spawn's location and orientation), and link them to a spawn")
#            row = box.row()
#            row.scale_y = 0.5
#            row.label(text="  point (select the sphere or marker first, then select a 'Player Starting Location', press CTRL+P, choose 'Object (Without Inverse)').")
#            row = box.row()
#            row.scale_y = 0.5
#            row.label(text="  The objects will adopt that spawn point's transform. If you've imported a map, or left this step until after placing spawn points,")
#            row = box.row()
#            row.scale_y = 0.5
#            row.label(text="  click [Populate All Spawns] to add and link Spheres and Markers to every PSL. If things get messy, delete the created collections,")
#            row = box.row()
#            row.scale_y = 0.5
#            row.label(text="  click the [Purge Orphans </3] button to clean up the leftover mesh, and start over.")
#            row = box.row()
#            row.scale_y = 0.5
        
        header, panel = layout.panel("ptm", default_closed=True)
        header.label(text="2. Populate The Map")
        if panel:
            box = panel.box()
            row = box.row()
            row = box.row()
            row.scale_y = 0.5
            row.label(text="  Add Spawn Spheres and Markers to all the PSLs. Sphere detail increases exponentially with each option, considerably")
            row = box.row()
            row.scale_y = 0.5
            row.label(text="  increasing the time to calculate 'Randoms', so use caution adjusting it above 4.")
            row = box.row()
            row.scale_y = 0.5
            
            
#        header, panel = layout.panel("gr", default_closed=True)
#        header.label(text="3. Generate Randoms")
#        if panel:
#            box = panel.box()
#            row = box.row()
#            row = box.row()
#            row.scale_y = 0.5
#            row.label(text="  With the above steps completed, click the [Generate Randoms] button. By default, this operation will use 'Exact' boolean, which can")
#            row = box.row()
#            row.scale_y = 0.5
#            row.label(text="  take a couple few if your spheres are high-detail. 'Fast' mode has a habit of ignoring some spheres, so unless you're just testing")
#            row = box.row()
#            row.scale_y = 0.5
#            row.label(text="  the process, it's highly recommended to leave 'Exact' mode selected. Don't be alarmed if Blender stops responding during this step.")
#            row = box.row()
#            row.scale_y = 0.5


        header, panel = layout.panel("gr", default_closed=True)
        header.label(text="3. Generate Randoms")
        if panel:
            box = panel.box()
            row = box.row()
            row = box.row()
            row.scale_y = 0.5
            row.label(text="  With a pink shell and a bunch of Spawn Spheres, click [Generate Randoms], and then wait. The spheres will carve")
            row = box.row()
            row.scale_y = 0.5
            row.label(text="  circles out of the shell, leaving an overlay depicting the random zones. Export this geometry as a .scenery and add")
            row = box.row()
            row.scale_y = 0.5
            row.label(text="  it to your .scenario.")
            row = box.row()
            row.scale_y = 0.5
        
#        header, panel = layout.panel("gs", default_closed=True)
#        header.label(text="4. Gameplay Simulation")
#        if panel:
#            box = panel.box()
#            row = box.row()
#            row = box.row()
#            row.scale_y = 0.5
#            row.label(text="  If everything went well, you'll have transparent spheres and markers at every spawn point, and some pink surfaces depicting the")
#            row = box.row()
#            row.scale_y = 0.5
#            row.label(text="  random zones. The last thing you need is a group of 4 Spartans to demonstrate Halo's spawn engine. Click the [Generate Spartans]")
#            row = box.row()
#            row.scale_y = 0.5
#            row.label(text="  button (next to 'Auto-respawn') to add 2 \"players\" to each team.")
#            row = box.row()
#            row.scale_y = 0.5
#            row = box.row()
#            row.scale_y = 0.5
#            row.label(text="  Visualizing Spawn Prediction:")
#            row = box.row()
#            row.scale_y = 0.5
#            row.label(text="    Manually hide P2 and P4 (or disable 'Auto-respawn' and 'kill' them with the provided ghost buttons), enable 'Real Time Prediction',")
#            row = box.row()
#            row.scale_y = 0.5
#            row.label(text="    then move P1 and P3 around the map to see how the spheres and markers fade in and out. The more opaque, the more likely that")
#            row = box.row()
#            row.scale_y = 0.5
#            row.label(text="    spawn will be chosen for a teammate. Note: Only one team perspective can be used at a time.")
#            row = box.row()
#            row.scale_y = 0.5
#            row = box.row()
#            row.scale_y = 0.5
#            row.label(text="  Realistic Spawn Engine:")
#            row = box.row()
#            row.scale_y = 0.5
#            row.label(text="    To see actual spawn selection in action, you can respawn the dead (hidden) players (with the provided 🗘 buttons) and watch")
#            row = box.row()
#            row.scale_y = 0.5
#            row.label(text="    where they reappear. Use these features to get a full understanding of team and enemy spawn influence while designing new,")
#            row = box.row()
#            row.scale_y = 0.5
#            row.label(text="    competitive 2v2 maps.")
#            row = box.row()
#            row.scale_y = 0.5
            
        header, panel = layout.panel("gs", default_closed=True)
        header.label(text="4. Gameplay Simulation")
        if panel:
            box = panel.box()
            row = box.row()
            row = box.row()
            row.scale_y = 0.5
            row.label(text="  This feature adjusts Sphere opacity to convey spawn predictions based on friendly and enemy Spartan locations.")
            row = box.row()
            row.scale_y = 0.5
            row.label(text="  It can also accurately emulate a 2v2 game environment, by respawning Spartans using Halo's actual spawn code.")
            row = box.row()
            row.scale_y = 0.5
            row.label(text="  Enjoy!")
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
        
        return context.window_manager.invoke_props_dialog(self, width=640)


class HowShell(Operator):
    bl_idname = "object.how_shell"
    bl_label = "Shelling the map..."
    bl_description = "Need some handholding on shelling your map?"
    
    def draw(self, context):
        box = self.layout
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  Your level may consist of several geometry clusters, and lots of clutter, such as light-emitting")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  strips, floating panels, ladders, and glass. Clone the geometry that defines your sealed world,")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  combine any clusters, and leave out or remove all the other clutter, as it will disturb the shell")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  process. Make sure the BSP is STL Checked (100% sealed, all vertices welded), and select it")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  with the object picker provided. Click [Shell Map] to produce another clone of your BSP and")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  turn it into a pink skin covering all the surfaces. The Spawn Spheres will be carved out of this")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  geometry to produce the random zones in the next few steps.")
        row = box.row()
        row.scale_y = 0.5
    
    def execute(self, context):
        print("Go on with your bad shellf")
        return {"FINISHED"}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=510)


class HowPopulate(Operator):
    bl_idname = "object.how_populate"
    bl_label = "Populating the map..."
    bl_description = "Learn how to quickly add Spawn Spheres and Markers to the level..."
    
    def draw(self, context):
        box = self.layout
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  Whether you've imported an existing map or you're designing a new one, you can create and link")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  Spawn Spheres and Markers to each PSL ('Player Starting Location'). In either case, it is best to")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  use the [Populate All Spawns] button, as each object will be automatically renamed and linked to")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  its parent spawn point, adopting its transform. However, this can be done manually, too: Add and")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  select a Sphere or Marker, then select a 'Player Starting Location', press CTRL+P, and choose")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  'Object (Without Inverse)'.")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  ")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  NOTE: Spheres must be in a collection called 'Spawn Spheres' in order to be considered during")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  the generation of 'Randoms' geometry.")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  ")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  You can adjust the color and opacity of Spheres and Markers before or after you've added them.")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  Caution: Do not manually move a Sphere or Marker! Rather, move the parent PSL, and the objects")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  will move with it. If you need to start over, delete the Spheres and Markers collections, and click")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  the [Purge Orphans </3] button to clean up the leftover mesh and materials. (Change your")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  'Outliner' list view to 'Unused Data' to see orphans).")
        row = box.row()
        row.scale_y = 0.5

    def execute(self, context):
        print("Welcome to Halo. Population: 0. Please procreate.")
        return {"FINISHED"}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=530)


class HowRandoms(Operator):
    bl_idname = "object.how_randoms"
    bl_label = "Generating Randoms..."
    bl_description = "Best practices for populating randoms..."
    
    def draw(self, context):
        box = self.layout
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  By default, this operation will use the 'Exact' boolean solver, which may take a few minutes if")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  your spheres are high-poly (recommended 'Sphere Detail' setting is [4] for acceptably smooth")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  curves and reasonable run-time.) Unfortunately, the 'Fast' solver has been known to completely")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  ignore some spheres, so unless you're just testing the process, it's highly recommended to")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  leave 'Exact' mode selected. Don't be alarmed if Blender stops responding during this step. If")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  you're curious, you can uncheck 'Apply When Completed' and make manual adjustments to")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  the boolean modifier.")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  ")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  NOTE: This operation may completely hang Blender when calculating and applying. Let it work.")
        row = box.row()
        row.scale_y = 0.5

    def execute(self, context):
        print("You've been randomly selected.")
        return {"FINISHED"}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=520)



class HowSimulate(Operator):
    bl_idname = "object.how_simulate"
    bl_label = "Simulating spawns..."
    bl_description = "How to see Halo 1's spawn engine in action..."
    
    def draw(self, context):
        box = self.layout
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  By this step, you should have semi-transparent spheres and markers at every spawn point, and some pink")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  surfaces depicting the random zones. The last thing you'll need is a group of 4 Spartans to demonstrate")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  Halo's spawn engine. Next to 'Auto-respawn', click the [Generate Spartans] button to add 2 \"players\" to")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  each team. If you have at least 4 'Spawn Spheres' attached to your PSLs, they will spawn into the map")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  using the Halo 1 spawn engine.")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  ")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  Visualizing Spawn Prediction:")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  ")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  Manually hide P2 and P4 (or disable 'Auto-respawn' and 'kill' them with the provided ghost buttons), then")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  move P1 and P3 around the map to see how the spheres and markers fade in and out. A higher opacity")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  means a higher likelihood that spawn will be selected. If 'Perspective' is set to 'Blue', the blue Spartan will")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  increase a spawn point's as he moves within 60 feet. A red Spartan will do the opposite, decreasing that")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  point's opacity / odds from 50 feet down to 20, at which point it's totally blocked. This is a great way to")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  visualize why certain spawns happen in known maps, and what sort of randoms or forced spawns will")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  work in yours.")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  ")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  Realistic Spawn Engine:")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  ")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  To see actual spawn selection in action, you can respawn the dead (hidden) players (with the 'Kill' button,")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  which counts down 5 seconds before respawning, or use the provided 🗘 buttons for instant respawn)")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  and watch where they reappear. Use these features to get a full understanding of team and enemy spawn")
        row = box.row()
        row.scale_y = 0.5
        row.label(text="  influence while designing new, competitive 2v2 maps.")
        row = box.row()
        row.scale_y = 0.5


    def execute(self, context):
        print("Welcome to Halo. Population: 0. Please procreate.")
        return {"FINISHED"}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=580)


classes = (
    HowTo,
    WM_HowTo,
    HowShell,
    HowPopulate,
    HowRandoms,
    HowSimulate,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
        
def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)