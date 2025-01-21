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


# That all being said... I'm not a coder by trade,
# I don't know Python, and I don't even do this kinda
# thing as a hobby anymore. So... don't judge my code!
# I do hope you enjoy and get some use out of this.
# Thanks for playing and creating :)
# - insidi0us

bl_info = {
    "name" : "Spawn Shop",
    "author" : "insidi0us",
    "version" : (1, 0),
    "blender" : (4, 3, 2),
    "location" : "View3d > Tool",
    "warning" : "",
    "wiki_url" : "",
    "category" : "Add Mesh",
}

import bpy, functools, random, math, bmesh
from math import *
from mathutils import Vector


slayerSpawnTypes = ['Slayer','All Games','All Except CTF','All Except Race And CTF']
ctfSpawnTypes = ['CTF','All Games']

slayerSpawnIndices = ['2','12','13','14']
ctfSpawnIndices = ['1','12']



######################################################################################################################
###
###   README
###

class HowTo(bpy.types.Operator):
    
    bl_idname = "object.how_to"
    bl_label = "How To...   "
    bl_description = "Click for Instructions"
    
    def execute(self, context):
    
        bpy.ops.wm.howto('INVOKE_DEFAULT')
        
        return {"FINISHED"}


class WM_HowTo(bpy.types.Operator):
    bl_label = "Spawn Shop v1.0 - Guide"
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


######################################################################################################################
###
###   SHELL THE MAP
###

class ShellMap(bpy.types.Operator):
    
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
###   GENERATE SPHERES
###

def MakeMat(matname,color):
    print("Making"+color+"material!")
    mat = bpy.data.materials.get(matname+color)
    if(mat):
        print("Material already exists!")
    else:
        mat = bpy.data.materials.new(name=matname+color)
        mat.use_nodes = True
        
        col = (0,0,0,1) # black
        
        if color == 'red':
            col = (1,0,0,1)
        elif color == 'blue':
            col = (0,0,1,1)
        elif color == 'green':
            col = (0,1,0,1)
        elif color == 'yellow':
            col = (1,1,0,1)
        elif color == 'gray':
            col = (0.5,0.5,0.5,1)
        elif color == 'black':
            col = (0,0,0,1)

        # Create a Principled BSDF shader node
        principled_bsdf = mat.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        principled_bsdf.inputs['Base Color'].default_value = col
        principled_bsdf.inputs['Alpha'].default_value = bpy.context.scene.sphere_opacity # Transparency

        # Connect the Principled BSDF to the Material Output
        output_node = mat.node_tree.nodes.get('Material Output')
        mat.node_tree.links.new(principled_bsdf.outputs['BSDF'], output_node.inputs['Surface'])
    return mat

def MakeSphere(mat):

    # look for 'Spawn Shop'
    SpawnShopCollection = bpy.context.scene.collection.children.get("Spawn Shop")
    if SpawnShopCollection:
        print("Spawn Shop collection already exists, which is good. Proceeding.")
    else:
        SpawnShopCollection = bpy.data.collections.new("Spawn Shop")
        bpy.context.scene.collection.children.link(SpawnShopCollection)
    
    # CREATE INNER ICOSPHERE
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=bpy.context.scene.subdivisions,
        radius=100,
        enter_editmode=False,
        align='WORLD',
        location=(0, 0, 0),
        scale=(1, 1, 1)
    )
    
    inball = bpy.context.active_object
    inner_name = "Sample Sphere inner_mesh"
    inball.data.name = inner_name

    # CREATE OUTER ICOSPHERE
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=bpy.context.scene.subdivisions,
        radius=600,
        enter_editmode=False,
        align='WORLD',
        location=(0, 0, 0),
        scale=(1, 1, 1)
    )

    sphere = bpy.context.active_object
    sphere.data.name = "Sample Sphere Mesh"
    sphere.name = "Sample Sphere [Detail "+str(bpy.context.scene.subdivisions)+"]"
    
    # ASSIGN MATERIAL
    if sphere.data.materials: # If the object already has a material, replace it
        sphere.data.materials[0] = mat
    else: # If the object doesn't have any materials, add the new one
        sphere.data.materials.append(mat)

    # ADD BOOLEAN MODIFIER TO OUTER ICOSPHERE, DELETE INNER ICOSPHERE
    bpy.ops.object.modifier_add(type='BOOLEAN')
    bpy.context.object.modifiers["Boolean"].object = bpy.data.objects[inball.name]
    bpy.ops.object.modifier_apply(modifier="Boolean")
    bpy.data.objects.remove(inball, do_unlink=True)
    
    bpy.context.object.active_material.surface_render_method = 'BLENDED'
    sphere.data.shade_smooth()
    
    # Deleting inball (above) produces an orphaned mesh. delete it:
    if bpy.data.meshes[inner_name]:
        bpy.data.meshes.remove(bpy.data.meshes[inner_name])
    
    if(sphere.users_collection):
        parent = sphere.users_collection[0]
        parent.objects.unlink(sphere)
    SpawnShopCollection.objects.link(sphere)
    
    return sphere

def MakeMarker(mat):

    # look for 'Spawn Shop'
    SpawnShopCollection = bpy.context.scene.collection.children.get("Spawn Shop")
    if SpawnShopCollection:
        print("Spawn Shop collection already exists, which is good. Proceeding.")
    else:
        SpawnShopCollection = bpy.data.collections.new("Spawn Shop")
        bpy.context.scene.collection.children.link(SpawnShopCollection)
        
    # CREATE MARKER FROM SCRATCH
    obj_name = "Sample Marker"

    mesh_data = bpy.data.meshes.new("Sample Marker Mesh")  # create mesh data
    marker = bpy.data.objects.new(obj_name, mesh_data) # create the mesh object using the mesh data
    bpy.context.scene.collection.objects.link(marker)  # add the mesh object into the scene
    bm = bmesh.new() # create a new bmesh
    
    # define the footprint
    verts = [
        (32,0,0),
        (0,-16,0),
        (-16,-16,0),
        (-24,-8,0),
        (-24,8,0),
        (-16,16,0),
        (0,16,0)
    ]

    for loc in verts:
        bm.verts.new(loc)

    bm.verts.ensure_lookup_table()
    face_vert_indices = [(0,1,2,3,4,5,6)]
    extrude_face_indices = [0]

    f = 0
    for vert_indices in face_vert_indices:
        vz = []
        for index in vert_indices:
            vz.append(bm.verts[index])
        face = bm.faces.new(vz)
        
        if f in extrude_face_indices:
            extrude_distance = 8
            top = bmesh.ops.extrude_face_region(bm, geom=[face])
            bmesh.ops.translate(bm, vec=Vector((0,0,extrude_distance)), verts=[v for v in top["geom"] if isinstance(v,bmesh.types.BMVert)])
        f += 1

    bm.to_mesh(mesh_data) # writes the bmesh data into the mesh data
    mesh_data.update()    # [Optional] update the mesh data (helps with redrawing the mesh in the viewport
    bm.free()             # clean  up / free memory that was allocated for the bmesh
    
    # ASSIGN MATERIAL
    if marker.data.materials: # If the object already has a material, replace it
        marker.data.materials[0] = mat
    else: # If the object doesn't have any materials, add the new one
        marker.data.materials.append(mat)
        
    marker.data.materials[0].surface_render_method = 'BLENDED'
    marker.data.shade_smooth()
    
    # LINK TO 'Spawn Shop'
    if(marker.users_collection):
        parent = marker.users_collection[0]
        parent.objects.unlink(marker)
    SpawnShopCollection.objects.link(marker)
    
    marker.select_set(True)
    
    return marker

class AddSphere(bpy.types.Operator):
    bl_idname = "object.add_sphere"
    bl_label = "+ Sample Sphere      "
    bl_description = "Add a single Spawn Sphere object to the scene."
    
    def execute(self, context):
        # Create a new material (if necessary) and new sphere
        color = bpy.context.scene.sphere_color_enum.sphere_color
        bout = MakeMat("SpawnMat_",color)
        MakeSphere(bout)
        
        return {"FINISHED"}    

class AddMarker(bpy.types.Operator):
    bl_idname = "object.add_marker"
    bl_label = "+ Sample Marker      "
    bl_description = "Add a single Spawn Marker object to the scene."
    
    def execute(self, context):
        print("do it!")
        
        if "Sample Marker" in bpy.data.objects:
            bpy.ops.object.select_all(action='DESELECT') 
            bpy.data.objects.get("Sample Marker").select_set(True)
            self.report({"ERROR"},"'Sample Marker' already exists in the scene!")
        else:
            print("'Sample Marker' not found. Creating...")
            
            # Create a new material and new marker
            color = bpy.context.scene.sphere_color_enum.sphere_color
            bout = MakeMat("SpawnMat_",color)
            MakeMarker(bout)
        
        return {"FINISHED"}
 
class GenerateSpheres(bpy.types.Operator):
    bl_idname = "object.generate_spheres"
#    bl_label = "Add Spheres & Markers    "
    bl_label = "Populate All Spawns    "
    bl_description = "Place spheres and markers on all Slayer spawns.\n\nRequires 'Player Starting Locations' in Scene root."
    
    def execute(self, context):
        
        print("Hello from the ico-sphere generator!")
        
        scene = bpy.context.scene
                
        # look for 'Spawn Shop'
        SpawnShopCollection = bpy.context.scene.collection.children.get("Spawn Shop")
        if SpawnShopCollection:
            print("Spawn Shop collection already exists, which is good. Proceeding.")
        else:
            SpawnShopCollection = bpy.data.collections.new("Spawn Shop")
            bpy.context.scene.collection.children.link(SpawnShopCollection)
        
        # look for 'Spawn Spheres'
        SpawnSpheresCollection = SpawnShopCollection.children.get("Spawn Spheres")
        if SpawnSpheresCollection:
            print("Spawn Spheres collection already exists!")
            # how many children
            if len(SpawnSpheresCollection.objects) > 0 : 
                print("'Spawn Spheres' collection has children!")
                error_line_one = "'Spawn Spheres' collection not empty!"
                error_line_two = "Please delete the collection first, or move on to Step 3."
                self.report({'ERROR'},error_line_one+"\n"+error_line_two)
                return {"CANCELLED"} # canceling because if these are here, markers likely are also. if not,
                                     # user only half deleted stuff, which means we don't know what to trust
            else:
                print("...but it's empty. Carry on.")
        else:
            SpawnSpheresCollection = bpy.data.collections.new("Spawn Spheres")
            SpawnShopCollection.children.link(SpawnSpheresCollection)
        
        # look for 'Spawn Markers'
        SpawnMarkersCollection = SpawnShopCollection.children.get("Spawn Markers")
        if SpawnMarkersCollection:
            print("Spawn Markers collection already exists!")
            # how many children
            if len(SpawnMarkersCollection.objects) > 0 :
                print("'Spawn Markers' collection has children!")
                error_line_one = "'Spawn Markers' collection not empty!"
                error_line_two = "Please delete the collection first, or move on to Step 3."
                self.report({'ERROR'},error_line_one+"\n"+error_line_two)
                return {"CANCELLED"} # canceling because if these are here, spheres likely are also. if not,
                                     # user only half deleted stuff, which means we don't know what to trust
            else:
                print("...but it's empty. Carry on.")
        else:
            SpawnMarkersCollection = bpy.data.collections.new("Spawn Markers")
            SpawnShopCollection.children.link(SpawnMarkersCollection)
        
        # look for 'Player Starting Locations' (imported)
        PSL = bpy.context.scene.collection.children.get("Player Starting Locations") 
        if PSL:
            print("Player Starting Locations found:",PSL.name)

            slayer_count = 0
            ctf_count = 0

            color = bpy.context.scene.sphere_color_enum.sphere_color
            bout = MakeMat("SpawnMat_",color)
            
            SampleSphere = MakeSphere(bout)
            SampleMarker = MakeMarker(bout)
#            SampleSphere.hide_set(True) # they get deleted, no need to hide, but...
#            SampleMarker.hide_set(True) # keeping this function for future reference
            
            SlayerSpawns = {} # used only for counting the total
            CTFSpawns = {}    # number of spawns at end of loop
            
            for Spawn in PSL.objects:
                #break # for debugging
                if Spawn.tag_player_starting_location.type_0 in slayerSpawnIndices:

                    slayer_count += 1
                    n = Spawn.name.split("_")[1]
                    SlayerSpawns[n] = Spawn
                                
                    # COPY SPHERE
#                    newname = "SpawnSphere_"+n
                    NewSphere = SampleSphere.copy()
                    NewSphere.data = SampleSphere.data.copy()
                    NewSphere.location = Spawn.location
                    NewSphere.name = "SpawnSphere_"+n
                    NewSphere.data.name = "SpawnSphere_Mesh_"+n
                    
                    dupmat = bout.copy()
                    existing = bpy.data.materials.get("SpawnMat_"+n)
                    if existing:
                        bpy.data.materials.remove(existing)
                    dupmat.name = "SpawnMat_"+n
                    NewSphere.data.materials[0] = dupmat

                    # ADD SPHERE TO 'Spawn Spheres' COLLECTION, UNLINK FROM 'Scene Collection'
                    if NewSphere.users_collection:
                        parent = NewSphere.users_collection[0]
                        parent.objects.unlink(NewSphere)
                    SpawnSpheresCollection.objects.link(NewSphere)
                    
                    NewSphere.parent = Spawn
                    NewSphere.matrix_parent_inverse = Spawn.matrix_world.inverted()
                    
                    # MAKE SPAWN MARKER
                    NewMarker = SampleMarker.copy()
                    NewMarker.data = SampleMarker.data.copy()
                    NewMarker.location = Spawn.location
                    NewMarker.rotation_euler = Spawn.rotation_euler
                    NewMarker.name = "SpawnMarker_"+n
                    NewMarker.data.name = "SpawnMarker_Mesh_"+n
                    
                    NewMarker.data.materials[0] = dupmat
                    
                    # MOVE SPAWN MARKER TO 'Spawn Markers' COLLECTION, UNLINK FROM 'Scene Collection'
                    if NewMarker.users_collection:
                        parent = NewMarker.users_collection[0]
                        parent.objects.unlink(NewMarker)
                    SpawnMarkersCollection.objects.link(NewMarker)
                    
                    # MAKE SPAWN MARKER A CHILD OF ITS RESPECTIVE Player Starting Location
                    NewMarker.parent = Spawn
                    NewMarker.matrix_parent_inverse = Spawn.matrix_world.inverted()

                elif Spawn.tag_player_starting_location.type_0 in ctfSpawnIndices:
                    ctf_count += 1
                    n = Spawn.name.split("_")[1]
                    CTFSpawns[n] = Spawn

            print("Slayer spawns:",len(SlayerSpawns))
            print("CTF spawns:",len(CTFSpawns))
            
            # delete samples
            sphere_mesh = SampleSphere.data.name
            marker_mesh = SampleMarker.data.name
            bpy.data.objects.remove(SampleMarker, do_unlink=True)
            bpy.data.objects.remove(SampleSphere, do_unlink=True)
            if bpy.data.meshes[sphere_mesh]:
                bpy.data.meshes.remove(bpy.data.meshes[sphere_mesh])
            if bpy.data.meshes[marker_mesh]:
                bpy.data.meshes.remove(bpy.data.meshes[marker_mesh])
             
        else:
            self.report({'ERROR'}, "Player Starting Locations not found in Scene root!")
                
        
        return {'FINISHED'}



######################################################################################################################
###
###   GENERATE RANDOMS GEOMETRY
###


class GenerateRandoms(bpy.types.Operator):
    bl_idname = "object.generate_randoms"
    bl_label = "Generate Randoms  "
    bl_description = "Cut the spheres out of the shelled\nmap to create the randoms geometry."
    
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
            
            if tris == 640:
                detail = 3
                kinda_break = "Press OK if you're willing to unfocus your eyes for 30 seconds."
            elif tris == 2560:
                detail = 4
                kinda_break = "Press OK if you're heading to the bathroom."
            elif tris == 10240:
                detail = 5
                kinda_break = "Press OK if you acknowledge this is a bad idea."
            elif tris == 40960:
                detail = 6
                kinda_break = "Press OK if you're absolutely insane."
        
        tris_formatted = "{:,}".format(tris)
        
        layout = self.layout
        layout.label(text="Warning!", icon="ERROR")
        
        row = layout.row()
        row.label(text="         You're about to boolean "+str(total_spheres)+" spheres, each with "+tris_formatted+" triangles.")
#        row.scale_y = 0.5
        
        row = layout.row()
        row.label(text="         Blender may stop responding during this operation!")
#        row.scale_y = 0.5
        
        row = layout.row()
        row.label(text="         "+kinda_break)
#        row.scale_y = 0.5
        
        row = layout.row()
     
    def execute(self, context):       
        print("Go get a coffee")
        bpy.ops.object.generate_randoms_confirm()       
        return {"FINISHED"}
    
    def invoke(self, context, event):
        
        return context.window_manager.invoke_props_dialog(self, width=400)


class GenerateRandomsConfirm(bpy.types.Operator):
     
    bl_idname = "object.generate_randoms_confirm"
    bl_label = "Generate Randoms  "
    bl_description = "Cut the spheres out of the shelled\nmap to create the randoms geometry."
    
    def execute(self, context):
        print("Hello from the randoms generator!")
        
        found = False
        
        SpawnShopCollection = bpy.context.scene.collection.children.get("Spawn Shop")
        SpawnSpheresCollection = SpawnShopCollection.children.get("Spawn Spheres")
        
        required_collections = 2
        found_collections = 0
        
        if SpawnShopCollection is not None:
            print("Spawn Shop collection already exists, which is good. Proceeding.")
            found_collections += 1
        else:
            self.report({'ERROR'}, "Could not find 'Spawn Shop' collection!\nPlease run 'Shell Map' and 'Populate All Spawns' first.")
        
        if(SpawnSpheresCollection):
            print("Spawn Spheres collection already exists. Proceeding.")
            found_collections += 1
        else:
            self.report({'ERROR'}, "Could not find 'Spawn Spheres' collection!\nPlease run 'Shell Map' and 'Populate All Spawns' first.")
            
        if(found_collections == required_collections):
            print("can proceed!")
        else:
            print("cannot proceed!")
        
        shelled_bsp = None
        for obx in SpawnShopCollection.objects:
            if obx.name == "BSP.shell":
                bpy.context.view_layer.objects.active = obx
                obx.select_set(True)
                shelled_bsp = obx
                
        quality = 'FAST'
        if(bpy.context.scene.use_exact):
            quality = 'EXACT'
        
        
        if(shelled_bsp is not None):
            print("Found shelled!")            
            found = True
            bpy.context.view_layer.objects.active = shelled_bsp
            shelled_bsp.select_set(True)
            boo = shelled_bsp.modifiers.new("Bootilt","BOOLEAN")
            boo.solver = quality
            boo.operand_type = 'COLLECTION'
            boo.collection = SpawnSpheresCollection
            shelled_bsp.name = "BSP.shell.rand"
            if(bpy.context.scene.apply_randoms_modifier):
                bpy.ops.object.modifier_apply(modifier="Bootilt")
        else:
            SpawnShopCollection = bpy.context.scene.collection.children.get("Spawn Shop")
            
            if SpawnShopCollection is not None:
                for obj in SpawnShopCollection.objects:
                    if obj.name == "BSP.shell":
                        found = True
                        break
                if(found):
                    print("Found shelled in collection!")
                    bpy.context.view_layer.objects.active = shelled_bsp
                    shelled_bsp.select_set(True)
                    boo = shelled_bsp.modifiers.new("Bootilt","BOOLEAN")
                    boo.solver = quality
                    boo.operand_type = 'COLLECTION'
                    boo.collection = SpawnSpheresCollection
                    shelled_bsp.name = "BSP.shell.rand"
#                    if(bpy.context.scene.apply_randoms_modifier):            # why is this
#                        bpy.ops.object.modifier_apply(modifier="Bootilt")    # commented out?
                else:
                    self.report({'ERROR'}, "Could not find 'BSP.shell'! Did you forget to run 'Shell Map'?")
            else:
                self.report({'ERROR'}, "Could not find 'Spawn Shop' collection!\nPlease run 'Shell Map' and 'Populate All Spawns' first.")

            
        
        return {'FINISHED'}





######################################################################################################################
###
###   SET AND TRACK SPARTANS / DYNAMIC SPAWNS
###

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

def update_sphere_opacity(self, context):

    SpawnSpheres = bpy.data.collections.get("Spawn Spheres")
    for SS in SpawnSpheres.objects:
        spawnmat = SS.data.materials[0]
        if spawnmat:
            spawnmat.node_tree.nodes["Principled BSDF.001"].inputs[4].default_value = bpy.context.scene.sphere_opacity

def update_sphere_color(self, context):
#    print("updating colors")
    color = bpy.context.scene.sphere_color_enum.sphere_color
    col = (0,0,0,1) # black
        
    if color == 'red':
        col = (1,0,0,1)
    elif color == 'blue':
        col = (0,0,1,1)
    elif color == 'green':
        col = (0,1,0,1)
    elif color == 'yellow':
        col = (1,1,0,1)
    elif color == 'gray':
        col = (0.5,0.5,0.5,1)
    elif color == 'black':
        col = (0,0,0,1)
    
    spawn_mat = MakeMat("SpawnMat_",color)
    
    # do the samples also
    for o in bpy.data.objects:
        if "Sample Marker" in o.name or "Sample Sphere" in o.name:
            o.data.materials[0] = spawn_mat
            o.data.materials[0].surface_render_method = 'BLENDED'

    SpawnSpheres = bpy.data.collections.get("Spawn Spheres")
    if(SpawnSpheres):
        for SS in SpawnSpheres.objects:
            spawnmat = SS.data.materials[0]
            if spawnmat:
                spawnmat.node_tree.nodes["Principled BSDF.001"].inputs[0].default_value = col


class PaintSpartans(bpy.types.Operator):
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
        

def reenable_tracking():
    print("Restart tracking...")
    bpy.context.scene.real_time_tracking = True

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
                    rand = random.uniform(0.0,1.0)
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



######################################################################################################################
###
###   EXTRA BUTTONS
###   
  
class PurgeOrphans(bpy.types.Operator):
    bl_idname = "object.purge_orphans"
    bl_label = ""
    bl_description = "Removes orphaned meshes and materials\nafter their parents were manually deleted."

    def execute(self, context):
        
        delete_strings = [
            'Sample Sphere',
            'Sample Marker',
            'SpawnSphere',
            'SpawnMarker',
            'BSP_Mesh'
        ]
        
        objects_removed = 0
        for object in bpy.data.objects:
            if object.users == 0:
                delete_object = False
                
                for string in delete_strings:
                    if string in object.name:
                        delete_object = True
                        break
                if delete_object:
                    objects_removed += 1
                    bpy.data.objects.remove(object)                        

        meshes_removed = 0
        for block in bpy.data.meshes:
            if block.users == 0:
                print(block.name)
                
                delete_block = False
                for string in delete_strings:
                    if string in block.name:
                        delete_block = True
                        break
                
                if delete_block:
                    meshes_removed += 1
                    bpy.data.meshes.remove(block)
        
        materials_removed = 0
        for material in bpy.data.materials:
            if material.users == 0:
                if "SpawnMat" in material.name or "PinkShell" in material.name:
                    materials_removed += 1
                    bpy.data.materials.remove(material)
        
        self.report({"ERROR"},f"{objects_removed} orphaned objects removed!")
        self.report({"ERROR"},f"{meshes_removed} orphaned meshes removed!")
        self.report({"ERROR"},f"{materials_removed} orphaned materials removed!")
        
        return {"FINISHED"}
    




class CustomProperties(bpy.types.PropertyGroup):
    # dropdown menu for color selection
    # this class must come after 'def update_sphere_color'
    sphere_color : bpy.props.EnumProperty(
        name="",
        description="Select a color for the spawn spheres",
        items=[
            ('red',"Red","Spheres will be a nice, transparent red."),
            ('blue',"Blue","Spheres will be the superior blue color."),
            ('green',"Green","Spheres will be good for the environment."),
            ('yellow',"Yellow","Spheres will be yellow. Like the sun."),
            ('gray',"Gray","Spheres will be a neutral, dull, boring gray."),
            ('black',"Black","Spheres will be transparent black (best for seeing through).")
        ],
        update = update_sphere_color
    )

    
class SpawnShop(bpy.types.Panel):
        
    bl_label = "Spawn Shop    v1.0"
    bl_idname = "OBJECT_PT_SpawnShop"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI" # Called with N key
    bl_category = "Spawn Shop"
#    bl_options = {'HIDE_HEADER'} # hides the add-on title header, but makes the whole add-on transparent

    def draw(self, context):
        layout = self.layout
        scene = context.scene

# HOW TO        
#        row = layout.row()                   # put this header back in
#        row.label(text="Spawn Shop [0.9.9]") # if HIDE_HEADER is in use
        row = layout.row()
        row.operator("object.how_to",icon="QUESTION")
        row = layout.row()

# STEP 1
        header, panel = layout.panel("shpa", default_closed=False)
        header.label(text="Shell The Map", icon="EVENT_NDOF_BUTTON_1") # EVENT_NDOF_BUTTON_1 IPO_SINE EVENT_ONEKEY
        header.scale_y = 1.25
        if panel:
            panel.label(text="Select a sealed BSP:")
            panel.prop(context.scene, "bsp_select", text="")
            panel.prop(context.scene, "apply_solidify_modifier", text="Apply When Completed")
            panel.operator("object.shell_map", icon = "MOD_EDGESPLIT")

# STEP 2
        header, panel = layout.panel("sppa", default_closed=False)
        header.label(text="Spheres & Markers", icon="EVENT_NDOF_BUTTON_2") # EVENT_NDOF_BUTTON_2 IPO_QUAD EVENT_TWOKEY
        header.scale_y = 1.25
        if panel:
            split = panel.split(factor=0.55)
            left = split.column()
            right = split.column()
            
            left.label(text="Color:")
            right.prop(context.scene.sphere_color_enum, "sphere_color")
            left.label(text="Opacity:")
            right.prop(context.scene, "sphere_opacity", text="")
            
            left.label(text="Sphere Detail:")
            right.prop(context.scene, "subdivisions", text="") # need to add this option for inner sphere
                                    
            panel.operator("object.add_marker", icon = "PMARKER_ACT")
            panel.operator("object.add_sphere", icon = "MESH_CIRCLE")
            # other icons: SHADING_RENDERED NODE_MATERIAL SHADING_RENDERED MESH_CIRCLE
            panel.operator("object.generate_spheres", icon = "POINTCLOUD_DATA")
            split = panel.split(factor=0.75)
            left = split.column()
            right = split.column()
            left.label(text="Purge Orphans:")
            right.operator("object.purge_orphans", text="", icon="ORPHAN_DATA") # ORPHAN_DATA INFO_LARGE
            # other icons: SHADING_RENDERED NODE_MATERIAL POINTCLOUD_DATA GEOMETRY_NODES ONIONSKIN_ON

# STEP 3    
        header, panel = layout.panel("rapa", default_closed=False)
        header.label(text="Randoms Geometry", icon="EVENT_NDOF_BUTTON_3") # EVENT_NDOF_BUTTON_3 IPO_CUBIC EVENT_THREEKEY
        header.scale_y = 1.25
        if panel:
            panel.prop(context.scene, "use_exact", text="Use 'Exact' Boolean")
            panel.prop(context.scene, "apply_randoms_modifier", text="Apply When Completed")
            panel.operator("object.generate_randoms", icon = "HOLDOUT_ON")
        
# STEP 4
        header, panel = layout.panel("inpa", default_closed=False)
        header.label(text="Gameplay Simulation", icon="EVENT_NDOF_BUTTON_4") # EVENT_NDOF_BUTTON_4 IPO_QUART EVENT_FOURKEY
        header.scale_y = 1.25
        if panel:
            panel.label(text="Select Spartan(s):")
            split = panel.split(factor=0.3)
            left = split.column()
            right = split.column()
            left.label(text="Team:")
            right.prop(context.scene, "team_spartan_select", text="")
            left.label(text="Enemy:")
            right.prop(context.scene, "enemy_spartan_select", text="")
            row = right.row()
            right.operator("object.paint_spartans", icon="BRUSH_DATA")
            
            panel.prop(context.scene, "real_time_tracking", text="Real Time Tracking")
            split = panel.split(factor=0.5)
            left = split.column()
            left.label(text="Refresh Rate:")
            right = split.column()
            right.prop(context.scene, "spawn_refresh_rate", text="")
        
#        # neat little thing - show (and edit from panel) context.object's location and rotation
#        row = layout.row() 
#        if context.object is not None:
#            layout.label(text=""+context.object.name+"")
#            split = layout.split(factor=1)  # Split the layout 54% left, 46% right
#            col_left = split.column()
#            col_left.prop(context.object, "location", text="Location")
#            col_left.prop(context.object, "rotation_euler", text="Rotation")
                
# EXTRAS
#        layout.operator("object.delete_spheres", icon = "X")
#        row = layout.row() # space
        row = layout.row()
        row.alignment = 'CENTER'
        row.label(text="   Long live Halo 1")


def object_exists(name):
    return name in bpy.data.objects
              
        
def register():
    bpy.utils.register_class(SpawnShop)
    bpy.utils.register_class(HowTo)
    bpy.utils.register_class(ShellMap)
    bpy.utils.register_class(CustomProperties)
    bpy.utils.register_class(AddSphere)
    bpy.utils.register_class(AddMarker)
    bpy.utils.register_class(GenerateSpheres)
    bpy.utils.register_class(GenerateRandoms)
    bpy.utils.register_class(GenerateRandomsConfirm)
    bpy.utils.register_class(PaintSpartans)
    bpy.utils.register_class(PurgeOrphans)
    bpy.utils.register_class(WM_HowTo)
    
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
    
    bpy.types.Scene.bsp_select = bpy.props.PointerProperty(
        name = "",
        description = "Please select a perfect manifold (STL Checked)\nsealed world. No holes (or it won't shell nicely)!",
        type = bpy.types.Object
    )
    bpy.types.Scene.outer_segments = bpy.props.IntProperty(
        name = "",
        description = "Number of segments for the 6-meter-radius\nouter sphere (spawn influence zone)",
        default = 32,
        min = 8,
        max = 64
    )
    bpy.types.Scene.inner_segments = bpy.props.IntProperty(
        name = "",
        description = "Number of segments for the 1-meter-radius\ninner sphere (spawn blocking zone)",
        default = 24,
        min = 8,
        max = 64
    )
    bpy.types.Scene.apply_randoms_modifier = bpy.props.BoolProperty(
        name = "Apply",
        description = "Apply the modifier when the boolean operation\ncompletes, or leave unchecked to tweak settings.",
        default = True
    )
    bpy.types.Scene.apply_solidify_modifier = bpy.props.BoolProperty(
        name = "Apply",
        description = "Apply the modifier when the 'Solidify' operation\ncompletes, or leave unchecked to tweak settings.",
        default = True
    )
    bpy.types.Scene.use_exact = bpy.props.BoolProperty(
        name = "Exact",
        description = "Uncheck for testing in 'Fast' mode, which\nis much quicker, but notably unreliable.",
        default = True
    )
    bpy.types.Scene.subdivisions = bpy.props.IntProperty( # need another option for inner sphere levels
        name = "",
        description = "Range: 3-6\nDefault: 4\n\nSet the number of subdivisions to\nperform when creating the spheres.\n4 really is enough.",
        default = 4,
        min = 3,
        max = 6
    )
    bpy.types.Scene.spawn_refresh_rate = bpy.props.FloatProperty(
        name = "",
        description = "Range: 0.01-1.0\nDefault: 0.05\n\nSet the spawn analysis refresh rate.\nLower value = faster updates, higher CPU tax.",
        default = 0.05,
        min = 0.01,
        max = 1
    )
    bpy.types.Scene.sphere_opacity = bpy.props.FloatProperty(
        name = "",
        description = "Range: 0.2-0.8\nDefault: 0.4\n\nSet the opacity for spawn\nspheres and markers.",
        default = 0.4,
        min = 0.2,
        max = 0.8,
        update = update_sphere_opacity
    )
    
    bpy.types.Scene.sphere_color_enum = bpy.props.PointerProperty(
        type = CustomProperties
    )
    
    # collapsibles
    bpy.types.Scene.shell_expanded = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.spheres_expanded = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.randoms_expanded = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.simulation_expanded = bpy.props.BoolProperty(default=False)


def unregister():
#    bpy.app.handlers.depsgraph_update_post.remove(deps_callback) # this caused problems    
    bpy.utils.unregister_class(SpawnShop)
    bpy.utils.unregister_class(HowTo)
    bpy.utils.unregister_class(ShellMap)
    bpy.utils.unregister_class(CustomProperties)
    bpy.utils.unregister_class(AddSphere)
    bpy.utils.unregister_class(AddMarker)
    bpy.utils.unregister_class(GenerateSpheres)
    bpy.utils.unregister_class(GenerateRandoms)
    bpy.utils.unregister_class(GenerateRandomsConfirm)
    bpy.utils.unregister_class(PaintSpartans)
    bpy.utils.unregister_class(PurgeOrphans)
    bpy.utils.unregister_class(WM_HowTo)
    del bpy.types.Scene.team_spartan_select
    del bpy.types.Scene.enemy_spartan_select
    del bpy.types.Scene.real_time_tracking
    del bpy.types.Scene.bsp_select
    del bpy.types.Scene.influence_segments
    del bpy.types.Scene.inner_segments
    del bpy.types.Scene.apply_randoms_modifier
    del bpy.types.Scene.apply_solidify_modifier
    del bpy.types.Scene.use_exact
    del bpy.types.Scene.subdivisions
    del bpy.types.Scene.spawn_refresh_rate
    del bpy.types.Scene.sphere_color_enum
    
    # collapsibles
    del bpy.types.Scene.shell_expanded
    del bpy.types.Scene.spheres_expanded
    del bpy.types.Scene.randoms_expanded
    del bpy.types.Scene.simulation_expanded
    
if __name__ == "__main__":
    register()