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
import mathutils
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
        
        # update the countdown in case mouse wasn't moving over panel
        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                area.tag_redraw
                
        s = -1
        print("Respawn now!")
        # bpy.app.timers.unregister(RespawnPlayer)
        # failed because "function is not registered".
        # weird. thought a timer would keep going.


    

def select_spawn_point(Player, move_viewport = True):
    
    PSLs = {}
    PSL = bpy.data.collections.get("Player Starting Locations") 
    if PSL:
        slayer_count = 0
        slayerSpawnIndices = ['2','12','13','14']
        for Spawn in PSL.objects:
            if Spawn.tag_player_starting_location.type_0 in slayerSpawnIndices:
                slayer_count += 1
                n = Spawn.name.split("_")[1]
                PSLs[n] = Spawn

    Spartans = get_selected_spartans()
        
    spawner_team = 'unknown'
    p = -1
    
    if Player == bpy.context.scene.player_1_select:
        spawner_team = 'blue'
        p = 1
    elif Player == bpy.context.scene.player_2_select:
        spawner_team = 'blue'
        p = 2
    elif Player == bpy.context.scene.player_3_select:
        spawner_team = 'red'
        p = 3
    elif Player == bpy.context.scene.player_4_select:
        spawner_team = 'red'
        p = 4

    if len(PSLs.items()) == 0:
        bpy.ops.wm.show_error('INVOKE_DEFAULT',message="No Player Starting Locations found!")
        return {"CANCELLED"}

    if len(Spartans) > 0:
        # LOOP THROUGH ALL SPAWNS
        SpawnWeights = {}
        for n, PSL in PSLs.items():
            distance_rating = 1.0
            friendly_bonus = 0.0
            # Future: if this is "Both", need to loop through two sets of spheres:
            perspective = bpy.context.scene.perspective_enum.perspective
            # LOOP THROUGH ALL SPARTANS
            for teamplayer, Spartan in Spartans.items():
                
                if Spartan.hide_get(): # spartan is manually hidden by user, or hidden by code (dead)
#                    print("Not considering",Spartan.name)
                    continue # don't consider this spartan
                
                tp = teamplayer.split(".")
                team = tp[0]
                
                dist = (Spartan.location - PSL.location).length
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
            SpawnWeights[PSL] = spawn_weight
        
        for ss, weight in SpawnWeights.items():
            print(ss.name,"---> Weight:",weight)

        chosen = get_highest_weight(SpawnWeights)
        loc = chosen[0].location
        rot = chosen[0].rotation_euler
        print("Chosen Spawn:",chosen[0].name,"at:",loc,"spin:",rot)
        Player.location = loc
        Player.rotation_euler = rot
        Player.hide_set(False)
#        bpy.ops.object.select_all(action='DESELECT')
        Player.select_set(True)
        
        if bpy.context.scene.auto_view and move_viewport: # make this a user toggle from panel
            spartan_shoulders(p)
            
            
    else:
        print("No spartans selected. Cannot calculate spawns. (This actually shouldn't even happen.)")

def get_highest_weight(weights):
    if not weights:
        return None  # Return None if the dictionary is empty

    max_key = max(weights, key = weights.get)
    return max_key, weights[max_key]


def spartan_shoulders(p):
    
    # define players
    players = [
        None,
        bpy.context.scene.player_1_select,
        bpy.context.scene.player_2_select,
        bpy.context.scene.player_3_select,
        bpy.context.scene.player_4_select
    ]
    
    player = players[p]

    area_type = 'VIEW_3D'
    areas  = [area for area in bpy.context.window.screen.areas if area.type == area_type]

    with bpy.context.temp_override( # this was a fuck
        window=bpy.context.window,
        area=areas[0],
        region=[region for region in areas[0].regions if region.type == 'WINDOW'][0],
        screen=bpy.context.window.screen):
            

# enums - fly to spartan - this needs to be done first
        # jump camera to SELECTED (requires selecting the player)
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = player
        player.select_set(True)
        bpy.ops.view3d.view_selected(use_all_regions=False)


# enums - move viewport to spartan's chest height (must happen after view_selected)
        player_chest = player.location.copy() + mathutils.Vector((0,0,50))
        bpy.context.space_data.region_3d.view_location = player_chest
        
        # get spawn orientation (we care about Z axis)
        facing = player.rotation_euler.copy()
        spawn_z = math.degrees(facing[2])
        
        # get viewport orientation
        view_euler = bpy.context.space_data.region_3d.view_rotation.to_euler()
        
        # get and fix viewport X angle
        view_x_rad = view_euler.x
        view_x_deg = math.degrees(view_x_rad)
#        print("View X Degrees:",view_x_deg)
        if view_x_deg >= 0:
            pitch = view_x_deg - 72 
            direction = 'ORBITUP'
        elif view_x_deg < 0:
            pitch = 72 - view_x_deg
            direction = 'ORBITDOWN'
#        print(direction,pitch)
        bpy.ops.view3d.view_orbit(angle=math.radians(pitch), type=direction)
        
        # get and fix viewport Z angle
        view_z_rad = view_euler.z
        view_z_deg = math.degrees(view_z_rad)
        spin = (view_z_deg - spawn_z) + 90 # not sure why the 90 is needed
#        print('Spin...\nView Z: ',view_z_deg,'\nSpawnZ: ',spawn_z,'\nFinal:  ',spin)
        # orbit the viewport ('ORBITLEFT' subtracts the supplied angle)
        bpy.ops.view3d.view_orbit(angle=math.radians(spin), type='ORBITLEFT')



class ZoomSpartan(Operator):
    bl_idname = "object.view_spartan"
    bl_label = "Find Spartan"
    bl_description = "Move viewport to this Spartan"
    
    player: bpy.props.IntProperty(name="Player", default=-1)
    
    def execute(self,context):
        
        p = self.player
        
        spartan_shoulders(p)
        
#        # old attempts to get quaternion
#        facing = players[p].rotation_euler.copy()
#        x = facing[0]
#        y = facing[1]
#        z = facing[2]
#        
#        base_vector = mathutils.Vector(facing)
#        
#        rotation_matrix = facing.to_matrix()
#        
#        rotated_vector = rotation_matrix @ base_vector
#        
#        print('Rotated Vector:',rotated_vector)
#        
#        quat = facing.to_quaternion()
#        
#        xrad = math.radians(90)
#        yrad = math.radians(45)
#        zrad = math.radians(-12)
#        euler = mathutils.Euler((xrad,yrad,zrad),'XYZ')
#        
#        quat_to_euler = bpy.context.space_data.region_3d.view_rotation.to_euler()
#        
#        print("View Quaternion  :",bpy.context.space_data.region_3d.view_rotation)
#        print("Spawn Facing     :",facing)
#        print("Built Euler      :",euler)
#        print("Quat to Euler    :",quat_to_euler)
#        
#        qrot = euler.to_quaternion()
#        bpy.context.space_data.region_3d.view_rotation = qrot # points straight down at spawn


        
        return {"FINISHED"}
    

class KillSpartan(Operator):
    bl_idname = "object.kill_spartan"
    bl_label = "Kill"
    bl_description = "If 'Auto-respawn' is selected, he will respawn in 5 seconds."
    
    player: bpy.props.IntProperty(name="Player", default=-1)
    
    def execute(self, context):
        
        print("KillSpartan(Operator) >>>",str(context),str(context.area),str(context.area.type))
        
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
        
        
        print("SpawnSpartan(Operator) >>>",str(context),str(context.area),str(context.area.type))
        
        spawner = self.spawner
        print("Respawning player", str(self.spawner))

        SpawnSpheres = bpy.context.scene.spheres_select # add a dedicated picker for simulation?
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
the Spheres populated and linked to said spawns)."""
    
    def execute(self, context):
        
        # look for 'Spawn Shop' collection
        SpawnShopCollection = bpy.data.collections.get("Spawn Shop")
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
            return {"CANCELLED"}
        
        print("Generating, painting, and spawning Spartans...")
        
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

        bpy.ops.object.select_all(action='DESELECT')
        
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
                select_spawn_point(spartan, False)#,SpawnSpheres,Spartans):
        
        
        bpy.ops.view3d.view_selected(use_all_regions=False)
        
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


#def MakeSpartanMat(team):
#    print("Making spartan material...")
#    mat = bpy.data.materials.get(team+" Team")
#    if(mat):
#        print("Material already exists!")
#    else:
#        mat = bpy.data.materials.new(name=team+" Team")
#        mat.use_nodes = True
#        
#        col = (0,0,0,1) # black
#        
#        if team == 'Blue':
#            col = (0,0.239,1,1)
#        elif team == 'Red':
#            col = (0.8,0.04,0.04,1)

#        # Create a Principled BSDF shader node
#        principled_bsdf = mat.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
#        principled_bsdf.inputs['Base Color'].default_value = col

#        # Connect the Principled BSDF to the Material Output
#        output_node = mat.node_tree.nodes.get('Material Output')
#        mat.node_tree.links.new(principled_bsdf.outputs['BSDF'], output_node.inputs['Surface'])
#    return mat

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


def update_prediction_bool(self, context):
    

    SpawnSpheres = bpy.context.scene.spheres_select # add a dedicated picker for simulation?
    SpawnMarkers = bpy.data.collections.get("Markers")
    
    if bpy.context.scene.prediction:
        if not SpawnSpheres and not SpawnMarkers:
            bpy.ops.wm.show_error('INVOKE_DEFAULT',message="Need spheres or markers to display predictions!")
            return {"CANCELLED"}
        
    PSLs = {}
    PSL = bpy.data.collections.get("Player Starting Locations")
    if PSL:
        slayer_count = 0
        slayerSpawnIndices = ['2','12','13','14']
        for Spawn in PSL.objects:
            if Spawn.tag_player_starting_location.type_0 in slayerSpawnIndices:
                slayer_count += 1
                n = Spawn.name.split("_")[1]
                PSLs[n] = Spawn

    # Check if user wants to track spartans, begin timer if so
    if bpy.context.scene.prediction:

        Spartans = get_selected_spartans()
            
        try:
            bpy.app.timers.register(functools.partial(TrackingLoop, PSLs, Spartans))
        except ValueError:
            print("Couldn't start the tracker.")
        
    else:
        print("Stopped tracking spartans.")
        
        # turn all spheres and markers back on, if exist
        if SpawnSpheres:
            for SS in SpawnSpheres.objects:
                spheremat = SS.data.materials[0]
                if spheremat:
                    spheremat.node_tree.nodes["Principled BSDF"].inputs[4].default_value = bpy.context.scene.sphere_opacity
        if SpawnMarkers:
            for SM in SpawnMarkers.objects:
                markermat = SM.data.materials[0]
                if markermat:
#                    markermat.node_tree.nodes["BSDF"].inputs[4].default_value = bpy.context.scene.marker_opacity
                    markermat.node_tree.nodes["Mix Shader"].inputs[0].default_value = 1 - bpy.context.scene.marker_opacity

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

def TrackingLoop(PSLs, Spartans):
    
    if(bpy.context.scene.prediction):
        
        if len(Spartans) > 0:
            
            perspective = bpy.context.scene.perspective_enum.perspective

            # LOOP THROUGH ALL PROVIDED (slayer-enabled) Player Starting Locations:
            for n, PSL in PSLs.items():
                
                # if this PSL has spheres or markers attached:
                if len(PSL.children) > 0:
                    
                    # set the initial material and alpha for the discovered objects
                    for child in PSL.children:
                        if 'SpawnSphere' in child.name:
                            sphere_alpha = 0
                            spheremat = child.data.materials[0]
                        if 'SpawnMarker' in child.name:
                            marker_alpha = 0
                            markermat = child.data.materials[0]
                    
                    # calculate this spawn location, regardless of sphere or marker presence
                    distance_rating = 1.0
                    friendly_bonus = 0.0
                    # Future: if this is "Both", we'll need another set of spheres attached to each PSL,
                    # much like the markers, but team color will need to be provided in the name (I think?)
                    
                    # LOOP THROUGH ALL SPARTANS
                    for teamplayer, Spartan in Spartans.items():
                        
                        if Spartan.hide_get():
#                            print("Not considering",Spartan.name)
                            continue # don't consider this spartan
                        
                        tp = teamplayer.split(".")
                        team = tp[0]
                        player = tp[1]
                        
                        dist = (Spartan.location - PSL.location).length
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
                        sphere_alpha = 0.01
                    elif spawn_weight > 1:
                        sphere_alpha = (spawn_weight / 3) * bpy.context.scene.sphere_opacity
                        marker_alpha = (spawn_weight / 3) * bpy.context.scene.marker_opacity
                        # spawn_weight / 3 is not exactly correct, but close
                        # enough for visualization because spawn weight won't
                        # go much over 3 with a single teammate.
                        if sphere_alpha > bpy.context.scene.sphere_opacity:
                            sphere_alpha = bpy.context.scene.sphere_opacity
                            
                        if marker_alpha > bpy.context.scene.marker_opacity:
                            marker_alpha = bpy.context.scene.marker_opacity
                    
                    if spheremat:
                        spheremat.node_tree.nodes["Principled BSDF"].inputs[4].default_value = sphere_alpha
    
                    if markermat:
#                        markermat.node_tree.nodes["Principled BSDF"].inputs[4].default_value = marker_alpha
                        # we're mixing transparency into shader, so it has to be inverse (1 - marker_alpha)
                        markermat.node_tree.nodes["Mix Shader"].inputs[0].default_value = 1 - marker_alpha
                                
            return bpy.context.scene.spawn_refresh_rate # tells the timer how quickly to run again
        else:
            print("No spartans selected.")
    
    else:
        print("Stopping");



classes = (            # careful, if this is one item, 
    ZoomSpartan,
    KillSpartan,       # it needs a trailing comma, 
    SpawnSpartan,      # otherwise python shits
    GenerateSpartans,  # itself trying to iterate
)

def register():
    
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    # keeping this here in case we add a class to this script
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)