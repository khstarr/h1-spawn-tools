
import bpy
from bpy.types import Operator
#from .operators import *
import functools#, random # real time tracking


### GOALS:
# Create a button that generates 4 Spartans (harnessing HABleT), two painted red, and two painted blue
# Support these 4 players in the panel by adding 4 slots: Blue Player 1, Blue 2, Red 1, Red 2
# Link them to a newly created Spawn Shop > Players collection
# "Spawn" them into the map using the real spawn engine, start with blue player 1 on random, then blue 2 spawns based on that. Repeat for red.
# Add a button next to each player slot to kill them, and 5 seconds later (or instantly), respawn them based on all other players in the map
# Revive the sqrt rand line in the spawn engine. Hopefully we can witness a random random happening.

# NOTE: Can two players be dead at the same time, with two countdown timers running for them? Will have to experiment

class PaintSpartans(Operator):
    bl_idname = "object.paint_spartans"
    bl_label = "Paint Spartans  "
    bl_description = "Paint the 'Team' Spartan blue, and the 'Enemy' Spartan red."
    
    def execute(self, context):
        print("Get out the spray can!")
        
        team_spartan = bpy.context.scene.team_spartan_select
        enemy_spartan = bpy.context.scene.enemy_spartan_select
        
        if team_spartan:
            blue = MakeSpartanMat('Blue')
            if team_spartan.data.materials: # If the object already has a material, replace it
                print('team had a mat')
                team_spartan.data.materials[0] = blue
            else: # If the object doesn't have any materials, add the new one
                team_spartan.data.materials.append(blue)
        if enemy_spartan:
            red = MakeSpartanMat('Red')
            if enemy_spartan.data.materials: # If the object already has a material, replace it
                print('enemy had a mat')
                enemy_spartan.data.materials[0] = red
            else: # If the object doesn't have any materials, add the new one
                enemy_spartan.data.materials.append(red)

        return {"FINISHED"}


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



def update_tracking_bool(self, context):

    team_spartan = bpy.context.scene.team_spartan_select
    enemy_spartan = bpy.context.scene.enemy_spartan_select  
    SpawnSpheres = bpy.data.collections.get("Spawn Spheres")
    
    # Check if user wants to track spartans, begin timer if so
    if bpy.context.scene.real_time_tracking:
        Spartans = {}
        # if we ever expand to 4 spartans, we will need to loop through them, key them
        # with a number and probably have a nested dictionary. this is good for now.
        if team_spartan:
            print("Start tracking...")
            print("Selected team spartan:",team_spartan.name)
            Spartans['team'] = team_spartan
        if enemy_spartan:
            print("Selected enemy Spartan:",enemy_spartan.name)
            Spartans['enemy'] = enemy_spartan
#            print(Spartans)
        try:
            bpy.app.timers.register(functools.partial(TrackingLoop, team_spartan, enemy_spartan, SpawnSpheres, Spartans))
        except ValueError:
            print("Couldn't start the tracker.")
#            else:
#                print("No spartans selected!")
        
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
#    bpy.context.scene.real_time_tracking = True

def update_tracking(self, context):
    if bpy.context.scene.real_time_tracking:
        bpy.context.scene.real_time_tracking = False
        bpy.app.timers.register(reenable_tracking, first_interval=0.01)

def TrackingLoop(team_spartan, enemy_spartan, SpawnSpheres, Spartans):
    
    if(bpy.context.scene.real_time_tracking):
        
        if len(Spartans) > 0:
            # LOOP THROUGH ALL SPAWNS
            for SS in SpawnSpheres.objects:
                spawnmat = SS.data.materials[0]
                if(spawnmat):    
                    alpha = 0
                    distance_rating = 1.0
                    friendly_bonus = 0.0
                    # LOOP THROUGH ALL SPARTANS
                    for team, Spartan in Spartans.items():
                        
                        dist = (Spartan.location - SS.location).length
                        halo_distance = dist * 0.01
                        
                        # TEAM OR ENEMY BLOCKING
                        if 0.25 <= halo_distance < 1.0:
                            distance_rating = distance_rating * 0.1
                        elif halo_distance < 0.25:
                            distance_rating = 0.0
                        
                        # TEAM INFLUENCE
                        if team == 'team':
                            if 1.0 <= halo_distance <= 6.0:       
                                friendly_bonus = friendly_bonus + (1.0 - (halo_distance - 1.0) * 0.2) ** 0.6
                            elif halo_distance < 1.0:
                                friendly_bonus = 0.0
                        
                        # ENEMY INFLUENCE
                        if team == 'enemy':
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
                    
                    spawnmat.node_tree.nodes["Principled BSDF.001"].inputs[4].default_value = alpha
                                
            return bpy.context.scene.spawn_refresh_rate # tells the timer how quickly to run again
        else:
            print("No spartans selected.")

    
    else:
        print("Stopping");



#classes = (
#    PaintSpartans # can't iterate over a single-item object. the fuck python?
#)


def register():
    bpy.utils.register_class(PaintSpartans)
    
     # keeping this here in case we add a class to this script
#    from bpy.utils import register_class
#    for cls in classes:
#        register_class(cls)
    
    bpy.types.Scene.team_spartan_select = bpy.props.PointerProperty(
        name = "",
        description = "Select your team Spartan object",
        type = bpy.types.Object,
        update = update_tracking
    )
    
    bpy.types.Scene.enemy_spartan_select = bpy.props.PointerProperty(
        name = "",
        description = "Select your enemy Spartan object",
        type = bpy.types.Object,
        update = update_tracking
    )
    
    bpy.types.Scene.real_time_tracking = bpy.props.BoolProperty(
        name = "Real Time Tracking",
        description = "Show and hide spawn markers and influence spheres\nbased on the locations of the selected Spartan objects.",
        default = False,
        update = update_tracking_bool
    )
    bpy.types.Scene.spawn_refresh_rate = bpy.props.FloatProperty(
        name = "",
        description = "Range: 0.01-1.0\nDefault: 0.05\n\nSet the spawn analysis refresh rate.\nLower value = faster updates, higher CPU tax.",
        default = 0.05,
        min = 0.01,
        max = 1
    )


def unregister():
    # keeping this here in case we add a class to this script
#    from bpy.utils import unregister_class
#    for cls in classes:
#        unregister_class(cls)

    bpy.utils.unregister_class(PaintSpartans)
        
    del bpy.types.Scene.team_spartan_select
    del bpy.types.Scene.enemy_spartan_select
    del bpy.types.Scene.real_time_tracking
    del bpy.types.Scene.spawn_refresh_rate