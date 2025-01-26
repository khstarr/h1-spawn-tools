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

from .func import *

class AddSphere(bpy.types.Operator):
    bl_idname = "object.add_sphere"
    bl_label = "+ Sphere"
    bl_description = "Add a single Spawn Sphere object to the scene."
    
    def execute(self, context):
        # Create a new material (if necessary) and new sphere
        color = bpy.context.scene.sphere_color_enum.sphere_color
        bout = MakeMat("SpawnMat_",color)
        MakeSphere(bout)
        
        return {"FINISHED"}    

class AddMarker(bpy.types.Operator):
    bl_idname = "object.add_marker"
    bl_label = "+ Marker"
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
 
class PopulateSpawns(bpy.types.Operator):
    bl_idname = "object.populate_spawns"
#    bl_label = "Add Spheres & Markers    "
    bl_label = "Populate All Spawns    "
    bl_description = "Place spheres and markers on all Slayer spawns.\n\nRequires 'Player Starting Locations' in Scene root."
    
    def execute(self, context):
        
        print("Generating spheres and markers...")
        
        scene = bpy.context.scene
                
        # look for 'Spawn Shop'
        SpawnShopCollection = bpy.context.scene.collection.children.get("Spawn Shop")
        if SpawnShopCollection:
            print("Spawn Shop collection already exists, which is good. Proceeding...")
        else:
            SpawnShopCollection = bpy.data.collections.new("Spawn Shop")
            bpy.context.scene.collection.children.link(SpawnShopCollection)
        
        # look for 'Spawn Spheres'
        make_spheres = True
        SpawnSpheresCollection = SpawnShopCollection.children.get("Spawn Spheres")
        if SpawnSpheresCollection:
            print("Spawn Spheres collection already exists!")
            # how many children
            if len(SpawnSpheresCollection.objects) > 0 : 
                print("'Spawn Spheres' collection has children!")
#                error_line_one = "'Spawn Spheres' collection not empty!"
#                error_line_two = "Please delete the collection first, or move on to Step 3."
#                self.report({'ERROR'},error_line_one+"\n"+error_line_two)
#                return {"CANCELLED"} # canceling because if these are here, markers likely are also. if not,
                                     # user only half deleted stuff, which means we don't know what to trust
                make_spheres = False
                error_line_one = "'Spawn Spheres' collection already exists and is not empty. As such, no "
                error_line_two = "new spheres were created. Please double check you have what you need."
                self.report({"ERROR"},error_line_one+"\n"+error_line_two)
            else:
                print("...but it's empty. Carry on.")
        else:
            SpawnSpheresCollection = bpy.data.collections.new("Spawn Spheres")
            SpawnShopCollection.children.link(SpawnSpheresCollection)
        
        # look for 'Spawn Markers'
        make_markers = True
        SpawnMarkersCollection = SpawnShopCollection.children.get("Spawn Markers")
        if SpawnMarkersCollection:
            print("Spawn Markers collection already exists!")
            # how many children
            if len(SpawnMarkersCollection.objects) > 0 :
                print("'Spawn Markers' collection has children!")
#                error_line_one = "'Spawn Markers' collection not empty!"
#                error_line_two = "Please delete the collection first, or move on to Step 3."
#                self.report({'ERROR'},error_line_one+"\n"+error_line_two)
#                return {"CANCELLED"} # canceling because if these are here, spheres likely are also. if not,
                                     # user only half deleted stuff, which means we don't know what to trust
                make_markers = False
                error_line_one = "'Spawn Markers' collection already exists and is not empty. As such, no "
                error_line_two = "new markers were created. Please double check you have what you need."
                self.report({"ERROR"},error_line_one+"\n"+error_line_two)
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
            
            if make_spheres:
                SampleSphere = MakeSphere(bout)
            if make_markers:
                SampleMarker = MakeMarker(bout)
            
            SlayerSpawns = {} # used only for counting the
            CTFSpawns = {}    # total number of spawns at end of loop
            
            slayerSpawnTypes = ['Slayer','All Games','All Except CTF','All Except Race And CTF']
            ctfSpawnTypes = ['CTF','All Games']

            slayerSpawnIndices = ['2','12','13','14']
            ctfSpawnIndices = ['1','12']
            
            for Spawn in PSL.objects:
                #break # for debugging
                if Spawn.tag_player_starting_location.type_0 in slayerSpawnIndices:

                    slayer_count += 1
                    n = Spawn.name.split("_")[1]
                    SlayerSpawns[n] = Spawn
                    
                    if make_spheres:
                        # COPY SPHERE
                        NewSphere = SampleSphere.copy()
                        NewSphere.data = SampleSphere.data.copy()
                        NewSphere.location = Spawn.location
                        NewSphere.rotation_euler = Spawn.rotation_euler
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
                    
                    if make_markers:
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
            if make_spheres:
                sphere_mesh = SampleSphere.data.name
                bpy.data.objects.remove(SampleSphere, do_unlink=True)
                if bpy.data.meshes[sphere_mesh]:
                    bpy.data.meshes.remove(bpy.data.meshes[sphere_mesh])
            
            if make_markers:
                marker_mesh = SampleMarker.data.name
                bpy.data.objects.remove(SampleMarker, do_unlink=True)
                if bpy.data.meshes[marker_mesh]:
                    bpy.data.meshes.remove(bpy.data.meshes[marker_mesh])
             
        else:
            self.report({'ERROR'}, "Player Starting Locations not found in Scene root!")
                
        
        return {'FINISHED'}



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
            'BSP_Mesh',
            'P1',
            'P2',
            'P3',
            'P4',
            'spartan'
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





classes = (
    AddSphere,
    AddMarker,
    PopulateSpawns,
    PurgeOrphans
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
        
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


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
        
    del bpy.types.Scene.outer_segments
    del bpy.types.Scene.inner_segments