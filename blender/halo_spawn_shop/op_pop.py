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
        sphere_mat = MakeMat("SampleSphere_",color)
        
        sdout = bpy.context.scene.sphere_detail_outer
        sdin = bpy.context.scene.sphere_detail_inner
        MakeSphere(sphere_mat,sdout,sdin)
        
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
            
            color = bpy.context.scene.marker_color_enum.marker_color
            MakeNHEMarker(color)
            
            # old vert-by-vert mesh marker:
            # Create a new material and new marker
#            marker_mat = MakeMat("MarkerMat_",color)
#            MakeMarker(marker_mat)
        
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
        SpawnShopCollection = bpy.data.collections.get("Spawn Shop")
        if SpawnShopCollection:
            print("Spawn Shop collection already exists, which is good. Proceeding...")
        else:
            SpawnShopCollection = bpy.data.collections.new("Spawn Shop")
            bpy.context.scene.collection.children.link(SpawnShopCollection)
        
        # look for 'Spheres'
        make_spheres = True
        sdout = bpy.context.scene.sphere_detail_outer
        sdin = bpy.context.scene.sphere_detail_inner
        details = str(sdout)+"."+str(sdin)
        spheres_collection_name = "Spheres ["+details+"]"
        
        SpheresCollection = SpawnShopCollection.children.get(spheres_collection_name)
        if SpheresCollection:
            print("'"+spheres_collection_name+"' collection already exists!")
            # how many children
            if len(SpheresCollection.objects) > 0 : 
                print("'"+spheres_collection_name+"' collection has children!")
                make_spheres = False
                error_line_one = "'"+spheres_collection_name+"' already exists and is not empty. "
                error_line_two = "No new spheres were created!"
                self.report({"ERROR"},error_line_one+"\n"+error_line_two)
            else:
                print("...but it's empty. Carry on.")
        else:
            SpheresCollection = bpy.data.collections.new(spheres_collection_name)
            SpawnShopCollection.children.link(SpheresCollection)
        
        # look for 'Markers'
        make_markers = True
        MarkersCollection = SpawnShopCollection.children.get("Markers")
        if MarkersCollection:
            print("'Markers' collection already exists!")
            # how many children
            if len(MarkersCollection.objects) > 0 :
                print("'Markers' collection has children!")
                make_markers = False
                error_line_one = "'Markers' collection already exists and is not empty."
                error_line_two = "No new markers were created!"
                self.report({"ERROR"},error_line_one+"\n"+error_line_two)
            else:
                print("...but it's empty. Carry on.")
        else:
            MarkersCollection = bpy.data.collections.new("Markers")
            SpawnShopCollection.children.link(MarkersCollection)
        
        # look for 'Player Starting Locations' (imported)
        PSL = bpy.data.collections.get("Player Starting Locations") 
        if PSL:
            print("Player Starting Locations found:",PSL.name)

            slayer_count = 0
            ctf_count = 0

            sphere_color = bpy.context.scene.sphere_color_enum.sphere_color
            marker_color = bpy.context.scene.marker_color_enum.marker_color
            
            sphere_mat = MakeMat("SampleSphere_",sphere_color)
#            markmat = MakeMat("MarkerMat_",marker_color)
            
            if make_spheres:
                SampleSphere = MakeSphere(sphere_mat,sdout,sdin)
                
            if make_markers:
#                SampleMarker = MakeMarker(markmat)
                NHEMarker = MakeNHEMarker(marker_color)
                # how to edit nhe marker opacity:
#                bpy.data.materials["spawn_marker_nhe"].node_tree.nodes["Mix Shader"].inputs[0].default_value = 0

                # turn on backface culling
#                bpy.context.object.active_material.use_backface_culling = True

            
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
                        NewSphere.name = "SpawnSphere["+details+"]_"+n
                        NewSphere.data.name = "sphere_mesh["+details+"]_"+n
                        
                        # assign material to this spawn number
                        mat = bpy.data.materials.get("SphereMat_"+n)
                        if not mat:
                            mat = sphere_mat.copy()
                            mat.name = "SphereMat_"+n
                        NewSphere.data.materials[0] = mat
        # ALERT: Potential Bug
        # if user adds new spawns, or changes the spawn numbers,
        # wrong spheres will illuminate during simulation. advise user to
        # wipe spheres collection and purge orphans if they see this

                        # ADD SPHERE TO 'Spheres [X.X]' COLLECTION, UNLINK FROM 'Scene Collection'
                        if NewSphere.users_collection:
                            parent = NewSphere.users_collection[0]
                            parent.objects.unlink(NewSphere)
                        SpheresCollection.objects.link(NewSphere)
                        
                        NewSphere.parent = Spawn
                        NewSphere.matrix_parent_inverse = Spawn.matrix_world.inverted()
                    
                    if make_markers:
                        # MAKE SPAWN MARKER
#                        NewMarker = SampleMarker.copy()
#                        NewMarker.data = SampleMarker.data.copy()
                        NewMarker = NHEMarker.copy()
                        NewMarker.data = NHEMarker.data.copy()
                        NewMarker.location = Spawn.location
                        NewMarker.rotation_euler = Spawn.rotation_euler
                        NewMarker.name = "SpawnMarker_"+n
                        NewMarker.data.name = "marker_mesh_"+n
                        
                        # if using SampleMarker:
#                        dupmat = markmat.copy()
#                        existing = bpy.data.materials.get("MarkerMat_"+n)
#                        if existing:
#                            bpy.data.materials.remove(existing)
#                        dupmat.name = "MarkerMat_"+n
#                        NewMarker.data.materials[0] = dupmat

                        dupmat = NewMarker.data.materials[0].copy()
                        existing = bpy.data.materials.get("NHEMarkerMat_"+n)
                        if existing:
                            bpy.data.materials.remove(existing)
                        dupmat.name = "NHEMarkerMat_"+n
                        NewMarker.data.materials[0] = dupmat
#                        dupmat.use_backface_culling = True

                        
                        # MOVE SPAWN MARKER TO 'Markers' COLLECTION, UNLINK FROM 'Scene Collection'
                        if NewMarker.users_collection:
                            parent = NewMarker.users_collection[0]
                            parent.objects.unlink(NewMarker)
                        MarkersCollection.objects.link(NewMarker)
                        
                        # MAKE SPAWN MARKER A CHILD OF ITS RESPECTIVE Player Starting Location
                        NewMarker.parent = Spawn
                        NewMarker.matrix_parent_inverse = Spawn.matrix_world.inverted()
                        
                        # tag marker as a scenery item for inclusion in the .scenario upon export
                        # user should supply this path? ---\
                        tag_path = context.scene.tag_input.scenery_path
                        NewMarker.tag_object.tag_path = tag_path
                        
#                        SceneryCollection = bpy.data.collections.get("Scenery")
#                        if SceneryCollection:
#                            SceneryCollection.objects.link(NewMarker)
                        
                        # link to frame:
                        # don't know how to link to frame

                elif Spawn.tag_player_starting_location.type_0 in ctfSpawnIndices:
                    ctf_count += 1
                    n = Spawn.name.split("_")[1]
                    CTFSpawns[n] = Spawn

            print("Slayer spawns:",len(SlayerSpawns))
            print("CTF spawns:",len(CTFSpawns))
            
            
            
            # delete samples
            if make_spheres:
                # link SpheresCollection to Randoms Boolean select    
                bpy.context.scene.spheres_select = SpheresCollection
                
                sphere_mesh = SampleSphere.data.name
                bpy.data.objects.remove(SampleSphere, do_unlink=True)
                if bpy.data.meshes[sphere_mesh]:
                    bpy.data.meshes.remove(bpy.data.meshes[sphere_mesh])
            
            if make_markers:
#                marker_mesh = SampleMarker.data.name
#                bpy.data.objects.remove(SampleMarker, do_unlink=True)
#                if bpy.data.meshes[marker_mesh]:
#                    bpy.data.meshes.remove(bpy.data.meshes[marker_mesh])
                    
                nhe_marker_mesh = NHEMarker.data.name
                bpy.data.objects.remove(NHEMarker, do_unlink=True)
                if bpy.data.meshes[nhe_marker_mesh]:
                    bpy.data.meshes.remove(bpy.data.meshes[nhe_marker_mesh])
             
        else:
            self.report({'ERROR'}, "Player Starting Locations not found in Scene root!")
                
        
        return {'FINISHED'}

class CommuteMarkers(bpy.types.Operator):
    bl_idname = "object.commute_markers"
    bl_label = "Add Markers to Scenery Palette"
    bl_description = """
Move markers to the 'Scenery' collection and tag them with the below path.
This is necessary in order to include them in the exported .scenario"""
    
    def execute(self, context):
#        print("gonna",bpy.context.scene.tag_input.scenery_path)
                   
        SceneryCollection = bpy.data.collections.get("Scenery")
        MarkersCollection = bpy.data.collections.get("Markers")
        
        
        if SceneryCollection and MarkersCollection:
            for Marker in MarkersCollection.objects:
                SceneryCollection.objects.link(Marker)
#                MarkersCollection.objects.unlink(Marker)
        
        return {"FINISHED"}


class PurgeOrphans(bpy.types.Operator):
    bl_idname = "object.purge_orphans"
    bl_label = "Purge Orphans"
    bl_description = """
Remove orphaned meshes and materials
after their parents were manually deleted."""

    def execute(self, context):
        
        delete_strings = [
            'Sample Sphere',
            'Sample Marker',
            'SpawnSphere',
            'SpawnMarker',
            'sphere_mesh',
            'marker_mesh',
            'BSP_Mesh',
            'BSP.shell',
            'shell_mesh',
            'Randoms',
            'P1',
            'P2',
            'P3',
            'P4',
            'spartan',
            'spawn_marker_nhe',
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
        
        delete_mats = [
            'SampleSphere_',
            'SpawnMat',
            'SphereMat',
            'MarkerMat',
            'PinkShell',
            'spawn_marker_nhe',
        ]
        
        materials_removed = 0
        for material in bpy.data.materials:
            if material.users == 0:
                
                delete_mat = False
                for string in delete_mats:
                    if string in material.name:
                        delete_mat = True
                        break
                    
                if delete_mat:
                    materials_removed += 1
                    bpy.data.materials.remove(material)
        
        
        images_removed = 0            
        for image in bpy.data.images:
            if image.users == 0:
                if "spawn_marker_blender" in image.name:
                    images_removed += 1
                    bpy.data.images.remove(image)
        
        obs = "" if objects_removed == 1 else "s"
        mes = "" if meshes_removed == 1 else "es"
        mas = "" if materials_removed == 1 else "s"
        ims = "" if images_removed == 1 else "s"
        
        self.report({"ERROR"},f"{objects_removed} orphaned object{obs} removed!")
        self.report({"ERROR"},f"{meshes_removed} orphaned mesh{mes} removed!")
        self.report({"ERROR"},f"{materials_removed} orphaned material{mas} removed!")
        self.report({"ERROR"},f"{images_removed} orphaned image{ims} removed!")
        
        return {"FINISHED"}





classes = (
    AddSphere,
    AddMarker,
    PopulateSpawns,
    PurgeOrphans,
    CommuteMarkers
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)