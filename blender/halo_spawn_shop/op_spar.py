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

import sys, bpy
from bpy.types import Operator
import functools, random # real time tracking
import math
from math import *

def RespawnPlayer(player):
    
    s = 0
    
    if player == 1:
        s = bpy.context.scene.sec_p1
    elif player == 2:
        s = bpy.context.scene.sec_p2
    elif player == 3:
        s = bpy.context.scene.sec_p3
    elif player == 4:
        s = bpy.context.scene.sec_p4
    
    s -= 1
    
    if s > 0:
        if player == 1:
            bpy.context.scene.sec_p1 -= 1
        elif player == 2:
            bpy.context.scene.sec_p2 -= 1
        elif player == 3:
            bpy.context.scene.sec_p3 -= 1
        elif player == 4:
            bpy.context.scene.sec_p4 -= 1
        
        print("Player",player,"respawns in:",s)
    
        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                area.tag_redraw()
            
        return 1 # time to wait before next iteration
    else:
        # choose a spawn!            
        if player == 1:
            bpy.context.scene.sec_p1 = 0
            select_spawn_point(bpy.context.scene.player_1_select)
        elif player == 2:
            bpy.context.scene.sec_p2 = 0
            select_spawn_point(bpy.context.scene.player_2_select)
        elif player == 3:
            bpy.context.scene.sec_p3 = 0
            select_spawn_point(bpy.context.scene.player_3_select)
        elif player == 4:
            bpy.context.scene.sec_p4 = 0
            select_spawn_point(bpy.context.scene.player_4_select)
        
        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                area.tag_redraw()
                
        s = -1
        print("Respawn now!")
        # bpy.app.timers.unregister(RespawnPlayer)
        # failed because "function is not registered".
        # weird. thought a timer would keep going.

def select_spawn_point(player):#,SpawnSpheres,Spartans):
#    print("choose a spawn point for:",player.name,len(SpawnSpheres.objects),"spheres",len(Spartans.items()),"spartans")

    SpawnSpheres = bpy.data.collections.get("Spawn Spheres")

    Spartans = get_selected_spartans()
        
    spawner_team = 'unknown'
    if player == bpy.context.scene.player_1_select or player == bpy.context.scene.player_2_select:
        spawner_team = 'blue'
    elif player == bpy.context.scene.player_3_select or player == bpy.context.scene.player_4_select:
        spawner_team = 'red'

    if len(Spartans) > 0:
        # LOOP THROUGH ALL SPAWNS
        SpawnWeights = {}
        for SS in SpawnSpheres.objects:
            distance_rating = 1.0
            friendly_bonus = 0.0
            perspective = bpy.context.scene.perspective_enum.perspective # Future: if this is "Both", we need to loop through twice
            # LOOP THROUGH ALL SPARTANS
            for teamplayer, Spartan in Spartans.items():
                
                if Spartan.hide_get(): # spartan is manually hidden by user, or hidden by code (dead)
#                    print("Not considering",Spartan.name)
                    continue # don't consider this spartan
                
                tp = teamplayer.split(".")
                team = tp[0]
#                player = tp[1]
                
                dist = (Spartan.location - SS.location).length
                halo_distance = dist * 0.01 # world units
                
                # TEAM OR ENEMY BLOCKING
                if 0.25 <= halo_distance < 1.0:
                    distance_rating = distance_rating * 0.1
                elif halo_distance < 0.25:
                    distance_rating = 0.0
                
                # TEAM INFLUENCE
                if team == spawner_team:
                    if 1.0 <= halo_distance <= 6.0: # 18.288 meters
                        friendly_bonus = friendly_bonus + (1.0 - (halo_distance - 1.0) * 0.2) ** 0.6
                    elif halo_distance < 1.0:
                        friendly_bonus = 0.0
                
                # ENEMY INFLUENCE
                if team != spawner_team:
                    if 2.0 <= halo_distance <= 5.0: # 15.24 meters
                        distance_rating = distance_rating * (halo_distance - 2.0) * (1/3)
                    elif halo_distance < 2.0:
                        distance_rating = 0.0

            if friendly_bonus > 3.0:
                friendly_bonus = 3.0                        # max is 3
                
            friendly_bonus = (friendly_bonus * 3.0) + 1.0   # thus, max is 10
            rand = random.uniform(0.0,1.0)
            spawn_weight = distance_rating * friendly_bonus * math.sqrt(rand)
            
            SpawnWeights[SS] = spawn_weight
        
        for ss, weight in SpawnWeights.items():
            print(ss.name,"Weight:",weight)

        chosen = get_highest_weight(SpawnWeights)
        loc = chosen[0].location
        rot = chosen[0].rotation_euler
        print("Chosen Spawn:",chosen[0].name,"at:",loc,"spin:",rot)
        player.location = loc
        player.rotation_euler = rot
        player.hide_set(False)
            
    else:
        print("No spartans selected. Cannot calculate spawns. (This actually shouldn't even happen.)")

def get_highest_weight(weights):
    if not weights:
        return None  # Return None if the dictionary is empty

    max_key = max(weights, key = weights.get)
    return max_key, weights[max_key]
             

class KillSpartan(Operator):
    bl_idname = "object.kill_spartan"
    bl_label = "Kill"
    bl_description = "If 'Auto-respawn' is selected, he will respawn in 5 seconds."
    
    player: bpy.props.IntProperty(name="Player", default=-1)
    
    def execute(self, context):
        
        p = self.player
        
        if bpy.context.scene.auto_respawn:
    #        sec = -1
            if p == 1:
                bpy.context.scene.sec_p1 = 5
                sec = bpy.context.scene.sec_p1
                bpy.context.scene.player_1_select.hide_set(True)
            elif p == 2:
                bpy.context.scene.sec_p2 = 5
                sec = bpy.context.scene.sec_p2
                bpy.context.scene.player_2_select.hide_set(True)
            elif p == 3:
                bpy.context.scene.sec_p3 = 5
                sec = bpy.context.scene.sec_p3
                bpy.context.scene.player_3_select.hide_set(True)
            elif p == 4:
                bpy.context.scene.sec_p4 = 5
                sec = bpy.context.scene.sec_p4
                bpy.context.scene.player_4_select.hide_set(True)
            else:
                print("Got confused")
                
            for area in bpy.context.screen.areas:
                if area.type == "VIEW_3D":
                    area.tag_redraw()
            
            print("Player",str(self.player),"respawns in: 5")
            
            try:
                bpy.app.timers.register(functools.partial(RespawnPlayer, self.player), first_interval=1)
            except ValueError:
                print("Couldn't start the countdown.")
            
        else:
            if p == 1:
                bpy.context.scene.player_1_select.hide_set(True)
            elif p == 2:
                bpy.context.scene.player_2_select.hide_set(True)
            elif p == 3:
                bpy.context.scene.player_3_select.hide_set(True)
            elif p == 4:
                bpy.context.scene.player_4_select.hide_set(True)
        
        return {"FINISHED"}
    
    
class SpawnSpartan(Operator):
    bl_idname = "object.spawn_spartan"
    bl_label = "Respawn"
    bl_description = "Manually respawn this Spartan immediately."
    
    spawner: bpy.props.IntProperty(name="Spawner", default=-1)
    
    def execute(self, context):
        
        spawner = self.spawner
        print("Spawn who?", str(self.spawner))

        SpawnSpheres = bpy.data.collections.get("Spawn Spheres")
        Spartans = get_selected_spartans()

        if spawner == 1:
            bpy.context.scene.player_1_select.hide_set(True)
        elif spawner == 2:
            bpy.context.scene.player_2_select.hide_set(True)
        elif spawner == 3:
            bpy.context.scene.player_3_select.hide_set(True)
        elif spawner == 4:
            bpy.context.scene.player_4_select.hide_set(True)
        
        bpy.app.timers.register(functools.partial(RespawnPlayer, self.spawner), first_interval=0.25)
        
        return {"FINISHED"}
        
class GenerateSpartans(Operator):
    bl_idname = "object.generate_spartans"
    bl_label = "Generate Spartans"
    bl_description = """Generate Spartans

Adds 2 blue and 2 red Spartans to the map, spawning them the same way Halo would.
(Requires at least 4 spawn points in the 'Player Starting Locations' collection, and all
the Spawn Spheres populated and linked to said spawns)."""
    
    def execute(self, context):
        print("Go ahead and generate the spartans now. Paint them. Select them.")
        
        # look for 'Spawn Shop' collection
        SpawnShopCollection = bpy.context.scene.collection.children.get("Spawn Shop")
        if SpawnShopCollection:
            print("Spawn Shop collection already exists, which is good. Proceeding.")
        else:
            SpawnShopCollection = bpy.data.collections.new("Spawn Shop")
            bpy.context.scene.collection.children.link(SpawnShopCollection)
        
        
        # look for 'Spartans' collection
        SpartansCollection = SpawnShopCollection.children.get("Spartans")
        if SpartansCollection:
            print("Spartans collection already exists!")
            # how many children
            if len(SpartansCollection.objects) > 0 : 
                print("'Spartans' collection has children!")
                error_line_one = "'Spartans' collection not empty! Please delete"
                error_line_two = "the existing Spartans before generating more."
                self.report({'ERROR'},error_line_one+"\n"+error_line_two)
                return {"CANCELLED"}
            else:
                print("...but it's empty. Carry on.")
        else:
            SpartansCollection = bpy.data.collections.new("Spartans")
            SpawnShopCollection.children.link(SpartansCollection)
            
        # needed for importing io_scene_halo, for injecting custom .jms
        from os import path
        addon_directory = bpy.utils.user_resource('SCRIPTS') + "\\addons\\io_scene_halo"
        if addon_directory not in sys.path:
            sys.path.append(addon_directory)
        
        try:
            from io_scene_halo import global_functions
            from io_scene_halo.global_functions import mesh_processing
            from io_scene_halo.misc import scale_models
        except ValueError:
            self.report({"ERROR"},"Couldn't load 'io_scene_halo'! Check that it's in your (AppData) Blender addons folder.")
        
        game_version = "halo1"
        
        # get_object_mesh stuff here:
        script_folder_path = path.dirname(path.dirname(__file__))
        p = path.join(script_folder_path, "resources")
        p = bpy.utils.user_resource('SCRIPTS') + "\\addons\\halo_spawn_shop\\jms\\"
        f = "spartan.jms"
        filepath = p+f
        
        # dimensions aren't used unless item not found,
        # then makes a box with these dimensions:
        array_item = ("spartan", (18.4183, 29.8282, 70.362))

        # start from bottom:
        mesh_processing.deselect_objects(context)
        
        # clear any oldies
        bpy.context.scene.player_1_select = None
        bpy.context.scene.player_2_select = None
        bpy.context.scene.player_3_select = None
        bpy.context.scene.player_4_select = None
        player_names = ['P1','P2','P3','P4']
        for object in bpy.data.objects:
            if object.users == 0:
                delete_object = False
                for string in player_names:
                    if string in object.name:                        
                        delete_object = True
                        break
                if delete_object:
#                    objects_removed += 1
                    bpy.data.objects.remove(object)
        
        for block in bpy.data.meshes:
            if block.users == 0:                
                delete_block = False
                for string in player_names:
                    if string in block.name:
                        delete_block = True
                        break
                if delete_block:
#                    meshes_removed += 1
                    bpy.data.meshes.remove(block)
        
        # then create empty and select it
        spartan_name = player_names[0]
        mesh = scale_models.generate_mesh(filepath, array_item, game_version)
#        print(mesh)
        P1 = bpy.data.objects.new(spartan_name, mesh)
        SpartansCollection.objects.link(P1)
#        P1.select_set(True)
        P1.data.name = player_names[0]+"_mesh"
        
        bpy.context.scene.player_1_select = P1

        select_spawn_point(P1)
        
        team_size = 2
        
        for i in [1,2,3,4]:
            
            team = 'Blue'
            if i > team_size:
                team = 'Red'
                
            if i == 1:            
                P1.data.materials.append(GetSpartanMaterial(team+" Team"))
            else:
                name = player_names[i-1]#"P"+str(i)
                spartan = P1.copy()
                spartan.data = P1.data.copy()
                spartan.location = ((i-1)*50,(i-1)*50,0) # run spawn code
                spartan.name = name
                spartan.data.name = name+"_mesh"
                
                SpartansCollection.objects.link(spartan)
                    
                if i == 2:
                    bpy.context.scene.player_2_select = spartan
                elif i == 3:
                    bpy.context.scene.player_3_select = spartan
                elif i == 4:
                    bpy.context.scene.player_4_select = spartan
                
                spartan.data.materials[0] = GetSpartanMaterial(team+" Team")
                select_spawn_point(spartan)#,SpawnSpheres,Spartans):
        
        return {"FINISHED"}

def GetSpartanMaterial(matname):
    mat = bpy.data.materials.get(matname)
    if(mat):
        print("Material already exists!")
    else:
        mat = bpy.data.materials.new(name=matname)
        mat.use_nodes = True
        
        col = (0.0, 0.0, 0.0, 1.0) # black
        if matname == 'Red Team':
            col = (0.8, 0.04, 0.04, 1.0)
        elif matname == 'Blue Team':
            col = (0.0, 0.24, 1.0, 1.0)

        # Create a Principled BSDF shader node
        principled_bsdf = mat.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        principled_bsdf.inputs['Base Color'].default_value = col

        # Connect the Principled BSDF to the Material Output
        output_node = mat.node_tree.nodes.get('Material Output')
        mat.node_tree.links.new(principled_bsdf.outputs['BSDF'], output_node.inputs['Surface'])
    return mat

#class PaintSpartans(Operator): # not in use
#    bl_idname = "object.paint_spartans"
#    bl_label = "Paint Spartans  "
#    bl_description = "Paint the 'Team' Spartan blue, and the 'Enemy' Spartan red."
#    
#    def execute(self, context):
#        print("Get out the spray can!")
#        
##        team_spartan = bpy.context.scene.team_spartan_select
##        enemy_spartan = bpy.context.scene.enemy_spartan_select
#        
##        if team_spartan:
##            blue = MakeSpartanMat('Blue')
##            if team_spartan.data.materials: # If the object already has a material, replace it
##                print('team had a mat')
##                team_spartan.data.materials[0] = blue
##            else: # If the object doesn't have any materials, add the new one
##                team_spartan.data.materials.append(blue)
##        if enemy_spartan:
##            red = MakeSpartanMat('Red')
##            if enemy_spartan.data.materials: # If the object already has a material, replace it
##                print('enemy had a mat')
##                enemy_spartan.data.materials[0] = red
##            else: # If the object doesn't have any materials, add the new one
##                enemy_spartan.data.materials.append(red)

#        return {"FINISHED"}


def MakeSpartanMat(team):
    print("making spartan mat!")
    mat = bpy.data.materials.get(team+" Team")
    if(mat):
        print("Material already exists!")
    else:
        mat = bpy.data.materials.new(name=team+" Team")
        mat.use_nodes = True
        
        col = (0,0,0,1) # black
        
        if team == 'Blue':
            col = (0,0.239,1,1)
        elif team == 'Red':
            col = (0.8,0.04,0.04,1)

        # Create a Principled BSDF shader node
        principled_bsdf = mat.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        principled_bsdf.inputs['Base Color'].default_value = col

        # Connect the Principled BSDF to the Material Output
        output_node = mat.node_tree.nodes.get('Material Output')
        mat.node_tree.links.new(principled_bsdf.outputs['BSDF'], output_node.inputs['Surface'])
    return mat

def get_selected_spartans():

    Spartans = {}

    p1 = bpy.context.scene.player_1_select
    p2 = bpy.context.scene.player_2_select
    p3 = bpy.context.scene.player_3_select
    p4 = bpy.context.scene.player_4_select
    if p1:
        Spartans['blue.p1'] = p1
    if p2:
        Spartans['blue.p2'] = p2
    if p3:
        Spartans['red.p3'] = p3
    if p4:
        Spartans['red.p4'] = p4

    return Spartans


def update_tracking_bool(self, context):

    SpawnSpheres = bpy.data.collections.get("Spawn Spheres")

    # Check if user wants to track spartans, begin timer if so
    if bpy.context.scene.prediction:

        Spartans = get_selected_spartans()
            
        try:
            bpy.app.timers.register(functools.partial(TrackingLoop, SpawnSpheres, Spartans))
        except ValueError:
            print("Couldn't start the tracker.")
        
    else:
        print("Stopped tracking spartans.")
        
        # turn all bubbles back on
        for SS in SpawnSpheres.objects:
            spawnmat = SS.data.materials[0]
            if spawnmat:
                spawnmat.node_tree.nodes["Principled BSDF.001"].inputs[4].default_value = bpy.context.scene.sphere_opacity
        try:
            bpy.app.timers.unregister(TrackingLoop)
        except ValueError:
            pass
        

def reenable_tracking():
    print("Restart tracking...")
#    bpy.context.scene.prediction = True

def update_tracking(self, context):
    if bpy.context.scene.prediction:
        bpy.context.scene.prediction = False
        bpy.app.timers.register(reenable_tracking, first_interval=0.01) # needs to be a delay, 
        # otherwise this one doesn't cancel and two timers run at once

def TrackingLoop(SpawnSpheres, Spartans):
    
    if(bpy.context.scene.prediction):
        
        if len(Spartans) > 0:
            # LOOP THROUGH ALL SPAWNS
            for SS in SpawnSpheres.objects:
                spawnmat = SS.data.materials[0]
                if(spawnmat):    
                    alpha = 0
                    distance_rating = 1.0
                    friendly_bonus = 0.0
                    # Future: if this is "Both", we need to loop through twice:
                    # (or two sets of spheres. eek.)
                    perspective = bpy.context.scene.perspective_enum.perspective
                    # LOOP THROUGH ALL SPARTANS
                    for teamplayer, Spartan in Spartans.items():
                        
                        if Spartan.hide_get():
#                            print("Not considering",Spartan.name)
                            continue # don't consider this spartan
                        
                        tp = teamplayer.split(".")
                        team = tp[0]
                        player = tp[1]
                        
                        dist = (Spartan.location - SS.location).length
                        halo_distance = dist * 0.01
                        
                        # TEAM OR ENEMY BLOCKING
                        if 0.25 <= halo_distance < 1.0:
                            distance_rating = distance_rating * 0.1
                        elif halo_distance < 0.25:
                            distance_rating = 0.0
                        
                        # TEAM INFLUENCE
                        if team == perspective:
                            if 1.0 <= halo_distance <= 6.0:       
                                friendly_bonus = friendly_bonus + (1.0 - (halo_distance - 1.0) * 0.2) ** 0.6
                            elif halo_distance < 1.0:
                                friendly_bonus = 0.0
                        
                        # ENEMY INFLUENCE
                        if team != perspective:
                            if 2.0 <= halo_distance <= 5.0:     
                                distance_rating = distance_rating * (halo_distance - 2.0) * (1/3)
                            elif halo_distance < 2.0:
                                distance_rating = 0.0

                    if friendly_bonus > 3.0:
                        friendly_bonus = 3.0                        # max is 3
                        
                    friendly_bonus = (friendly_bonus * 3.0) + 1.0   # thus, max is 10
#                    rand = random.uniform(0.0,1.0)
                    spawn_weight = distance_rating * friendly_bonus # * math.sqrt(rand) # removed because we aren't choosing a spawn,
                                                                                        # just showing available spawns
                    if spawn_weight == 1:
                        alpha = 0.01
                    elif spawn_weight > 1:
                        alpha = (spawn_weight / 3) * bpy.context.scene.sphere_opacity
                        # spawn_weight / 3 is not exactly correct, but close
                        # enough for visualization because spawn weight won't
                        # go much over 3 with a single teammate.
                        if alpha > bpy.context.scene.sphere_opacity:
                            alpha = bpy.context.scene.sphere_opacity
                    
#                    if SS.name == "SpawnSphere_11": # debug - was making sure the teammate block distance was correct. it was.
#                        print("distance:",halo_distance,"distance rating:",distance_rating,"alpha:",alpha)
                        
                    spawnmat.node_tree.nodes["Principled BSDF.001"].inputs[4].default_value = alpha
                                
            return bpy.context.scene.spawn_refresh_rate # tells the timer how quickly to run again
        else:
            print("No spartans selected.")

    
    else:
        print("Stopping");



classes = (            # careful, if this is one item, 
    KillSpartan,       # it needs a trailing comma, 
    SpawnSpartan,      # otherwise python shits
    GenerateSpartans,  # itself trying to iterate
)

def register():
    
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    # player selection
    bpy.types.Scene.player_1_select = bpy.props.PointerProperty(
        name = "",
        description = "Select Player 1 (Blue Team)",
        type = bpy.types.Object,
        update = update_tracking
    )
    
    bpy.types.Scene.player_2_select = bpy.props.PointerProperty(
        name = "",
        description = "Select Player 2 (Blue Team)",
        type = bpy.types.Object,
        update = update_tracking
    )
    
    bpy.types.Scene.player_3_select = bpy.props.PointerProperty(
        name = "",
        description = "Select Player 3 (Red Team)",
        type = bpy.types.Object,
        update = update_tracking
    )
    
    bpy.types.Scene.player_4_select = bpy.props.PointerProperty(
        name = "",
        description = "Select Player 4 (Red Team)",
        type = bpy.types.Object,
        update = update_tracking
    )
    
    # player respawn time remaining integers
    bpy.types.Scene.sec_p1 = bpy.props.IntProperty(
        name = "",
        description = "Respawn time remaining",
        default = 0,
        min = 0,
        max = 10
    )
    bpy.types.Scene.sec_p2 = bpy.props.IntProperty(
        name = "",
        description = "Respawn time remaining",
        default = 0,
        min = 0,
        max = 10
    )
    bpy.types.Scene.sec_p3 = bpy.props.IntProperty(
        name = "",
        description = "Respawn time remaining",
        default = 0,
        min = 0,
        max = 10
    )
    bpy.types.Scene.sec_p4 = bpy.props.IntProperty(
        name = "",
        description = "Respawn time remaining",
        default = 0,
        min = 0,
        max = 10
    )
    
    # simulation options
    bpy.types.Scene.auto_respawn = bpy.props.BoolProperty(
        name = "Auto-respawn",
        description = "Countdown from 5 and then automatically respawn the dead player.",
        default = True
    )
    bpy.types.Scene.spawn_refresh_rate = bpy.props.FloatProperty(
        name = "",
        description = "Range: 0.01-1.0\nDefault: 0.05\n\nSet the spawn analysis refresh rate.\nLower value = faster updates, higher CPU tax.",
        default = 0.05,
        min = 0.01,
        max = 1
    )
    bpy.types.Scene.prediction = bpy.props.BoolProperty(
        name = "Real Time Tracking",
        description = "Show and hide spawn markers and influence spheres\nbased on the locations of the selected Spartan objects.",
        default = False,
        update = update_tracking_bool
    )


def unregister():
    # keeping this here in case we add a class to this script
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
        
    del bpy.types.Scene.player_1_select
    del bpy.types.Scene.player_2_select
    del bpy.types.Scene.player_3_select
    del bpy.types.Scene.player_4_select
    del bpy.types.Scene.auto_respawn
    del bpy.types.Scene.spawn_refresh_rate
    del bpy.types.Scene.prediction
    del bpy.types.Scene.sec_p1
    del bpy.types.Scene.sec_p2
    del bpy.types.Scene.sec_p3
    del bpy.types.Scene.sec_p4