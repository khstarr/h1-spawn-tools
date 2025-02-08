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

# needed for making low-poly marker
import math, bmesh
from math import *
from mathutils import Vector

# needed for importing io_scene_halo, for injecting custom .jms
from os import path
addon_directory = bpy.utils.user_resource('SCRIPTS') + "\\addons\\io_scene_halo"
if addon_directory not in sys.path:
    sys.path.append(addon_directory)

from io_scene_halo import global_functions
from io_scene_halo.global_functions import mesh_processing
from io_scene_halo.misc import scale_models


class CountSpawns(Operator):
    
    bl_label = "Count Spawns"
    bl_idname = "object.count_spawns"
    bl_description = "Get an initial count of Slayer PSLs"
    
    slayer: bpy.props.IntProperty(default=0)
    
    def invoke(self, context, event):
        
        PSL = bpy.data.collections.get("Player Starting Locations") 
        if PSL:
            print("Player Starting Locations found:",PSL.name)

            slayer_count = 0
            ctf_count = 0
            
            SlayerSpawns = {} # used only for counting the total number of 
            CTFSpawns = {}    # spawns at the end of the loop

            slayerSpawnIndices = ['2','12','13','14']
            ctfSpawnIndices = ['1','12']
            
            for Spawn in PSL.objects:
                #break # for debugging
                if Spawn.tag_player_starting_location.type_0 in slayerSpawnIndices:

                    slayer_count += 1
                    n = Spawn.name.split("_")[1]
                    SlayerSpawns[n] = Spawn
                    
                elif Spawn.tag_player_starting_location.type_0 in ctfSpawnIndices:
                    ctf_count += 1
                    n = Spawn.name.split("_")[1]
                    CTFSpawns[n] = Spawn

            print("Slayer spawns:",len(SlayerSpawns))
            print("CTF spawns:",len(CTFSpawns))
            
            self.slayer = len(SlayerSpawns)
            bpy.types.Scene.slayer_count = self.slayer
#            bpy.objects.OBJECT_PT_SpawnShop.slayer_spawn_count = self.slayer_spawn_count
#            bpy.context.scene.OBJECT_PT_SpawnShop.slayer_spawn_count = self.slayer_spawn_count
        
        return {"FINISHED"}
            
    def execute(self, context):
        return {"FINISHED"}


class WM_ShowError(Operator):
    # needed for the respawn functions...
    # maybe because they run after a timer?
    bl_label = "Error:"
    bl_idname = "wm.show_error"
    
    message: bpy.props.StringProperty()
    wide: bpy.props.IntProperty(default=320)
        
    def draw(self, context):
        layout = self.layout
        layout.label(text=self.message)
    
    def execute(self, context):
        return {"FINISHED"}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=self.wide)
    

def update_sphere_opacity(self, context):
            
    materials = bpy.data.materials
    for material in materials:
        if "SphereMat" in material.name:
            material.node_tree.nodes["Principled BSDF"].inputs[4].default_value = bpy.context.scene.sphere_opacity


def update_marker_opacity(self, context):

    MarkersCollection = bpy.data.collections.get("Markers")
    for SM in MarkersCollection.objects:
        markermat = SM.data.materials[0]
        if markermat:
#            markermat.node_tree.nodes["Principled BSDF"].inputs[4].default_value = bpy.context.scene.marker_opacity
            markermat.node_tree.nodes["Mix Shader"].inputs[0].default_value = 1 - bpy.context.scene.marker_opacity


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
        col = (0.5,0.5,0.5,1.0)
    elif color == 'black':
        col = (0,0,0,1)
    
#    spheremat = MakeMat("SphereMat_",color)
    
    # do the samples also
#    for o in bpy.data.objects:
#        if "Sample Sphere" in o.name:
##            o.data.materials[0] = spheremat
#            o.data.materials[0].surface_render_method = 'BLENDED'
#            o.data.materials[0].node_tree.nodes["Principled BSDF"].inputs[0].default_value = col
                
    materials = bpy.data.materials
    for material in materials:
        if "SphereMat" in material.name:
            material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = col


def update_marker_color(self, context):
    color = bpy.context.scene.marker_color_enum.marker_color
    col = (0,0,0,1) # black
        
    if color == 'green':
        col = (0,1,0,1)
    elif color == 'yellow':
        col = (1,1,0,1)
    elif color == 'white':
        col = (1,1,1,1)
    elif color == 'purple':
        col = (0.5,0.0,0.8,1.0)
    elif color == 'black':
        col = (0,0,0,1)
    
#    markermat = MakeMat("MarkerMat_",color)
    
    # do the samples also
    for o in bpy.data.objects:
        if "Sample Marker" in o.name:
#            o.data.materials[0] = markermat
            o.data.materials[0].surface_render_method = 'BLENDED'
            o.data.materials[0].node_tree.nodes["Principled BSDF"].inputs[0].default_value = col

    SpawnMarkers = bpy.data.collections.get("Markers") # this should be dynamically acquired
    if(SpawnMarkers):
        for SM in SpawnMarkers.objects:
            markermat = SM.data.materials[0]
            if markermat:
                markermat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = col
                

def MakeMat(matname,color):
    print("Making",color,"material!")
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
        if mat.use_nodes:
#            ntree = mat.node_tree
            bsdf = mat.node_tree.nodes.get("Principled BSDF", None)
            if bsdf is None:
                bsdf = mat.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
            
            bsdf.name = 'Principled BSDF'
            bsdf.inputs['Base Color'].default_value = col
            bsdf.inputs['Alpha'].default_value = bpy.context.scene.sphere_opacity # Transparency
            # future: need another function for marker?

            # Connect the Principled BSDF to the Material Output
            output = mat.node_tree.nodes.get('Material Output')
            mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    return mat


def MakeSphere(mat,sdout,sdin):

    # look for 'Spawn Shop'
    SpawnShopCollection = bpy.data.collections.get("Spawn Shop")
    if SpawnShopCollection:
        print("Spawn Shop collection already exists, which is good. Proceeding.")
    else:
        SpawnShopCollection = bpy.data.collections.new("Spawn Shop")
        bpy.context.scene.collection.children.link(SpawnShopCollection)
    
    # CREATE INNER ICOSPHERE
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=sdin,
        radius=100,
        enter_editmode=False,
        align='WORLD',
        location=(0, 0, 0),
        scale=(1, 1, 1)
    )
    
    inball = bpy.context.active_object
    inner_mesh_name = "Sample Sphere inner_mesh"
    inball.data.name = inner_mesh_name

    # CREATE OUTER ICOSPHERE
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=sdout,
        radius=600,
        enter_editmode=False,
        align='WORLD',
        location=(0, 0, 0),
        scale=(1, 1, 1)
    )
    sphere = bpy.context.active_object
    sphere.data.name = "Sample Sphere Mesh ["+str(sdout)+"."+str(sdin)+"]"
    sphere.name = "Sample Sphere ["+str(sdout)+"."+str(sdin)+"]"
    
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
    if bpy.data.meshes[inner_mesh_name]:
        bpy.data.meshes.remove(bpy.data.meshes[inner_mesh_name])
    
    if(sphere.users_collection):
        parent = sphere.users_collection[0]
        parent.objects.unlink(sphere)
    SpawnShopCollection.objects.link(sphere)
    
    return sphere


def MakeMarker(mat):

    # look for 'Spawn Shop'
    SpawnShopCollection = bpy.data.collections.get("Spawn Shop")
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

def MakeNHEMarker(color):
    
    # look for 'Spawn Shop'
    SpawnShopCollection = bpy.data.collections.get("Spawn Shop")
    if SpawnShopCollection:
        print("Spawn Shop collection already exists, which is good. Proceeding.")
    else:
        SpawnShopCollection = bpy.data.collections.new("Spawn Shop")
        bpy.context.scene.collection.children.link(SpawnShopCollection)
        
    if color == 'green':
        col = (0,1,0,1)
    elif color == 'yellow':
        col = (1,1,0,1)
    elif color == 'white':
        col = (1,1,1,1)
    elif color == 'purple':
        col = (0.5,0.0,0.8,1.0)
    elif color == 'black':
        col = (0,0,0,1)

    print("Import from spawn_marker.blend and make it",color)
    
    # build file path:
    script_folder_path = path.dirname(path.dirname(__file__))
    p = bpy.utils.user_resource('SCRIPTS') + "\\addons\\halo_spawn_shop\\blend\\"
    f = "spawn_marker.blend"
    filepath = p+f
    
    with bpy.data.libraries.load(filepath) as (data_from, data_to):
        data_to.objects = ["spawn_marker_nhe"]
    
    marker = data_to.objects[0]
#    bpy.context.collection.objects.link(obj)
    
    # LINK TO 'Spawn Shop'
    if(marker.users_collection):
        parent = marker.users_collection[0]
        parent.objects.unlink(marker)
    SpawnShopCollection.objects.link(marker)
    
    bpy.ops.object.select_all(action='DESELECT')
    marker.select_set(True)
    
    marker.data.materials[0].node_tree.nodes["Principled BSDF"].inputs[0].default_value = col
    
    for mat in marker.data.materials:
        if mat.name not in bpy.data.materials:
            bpy.data.materials.append(mat)
    
    return marker


#class Make_NHE_Marker(Operator): # not in use
#    bl_idname = "object.spawn_marker_nhe"
#    bl_label = "NHE Spawn Marker"
#    bl_description = "Place a spawn scenery item at every Slayer spawn."
#    
#    def execute(self, context):

#        print("Import from spawn_marker.blend...")
#        
#        # build file path:
#        script_folder_path = path.dirname(path.dirname(__file__))
#        p = bpy.utils.user_resource('SCRIPTS') + "\\addons\\halo_spawn_shop\\blend\\"
#        f = "spawn_marker.blend"
#        filepath = p+f
#        
#        with bpy.data.libraries.load(filepath) as (data_from, data_to):
#            data_to.objects = ["spawn_marker_nhe"]
#        
##        marker = data_to.objects[0]
##        bpy.context.collection.objects.link(marker)
#        
#        # LINK TO 'Spawn Shop'
#        if(marker.users_collection):
#            parent = marker.users_collection[0]
#            parent.objects.unlink(marker)
#        SpawnShopCollection.objects.link(marker)
#        
#        marker.select_set(True)
#        
#        for mat in marker.data.materials:
#            if mat.name not in bpy.data.materials:
#                bpy.data.materials.append(mat)
#        
#        return {"FINISHED"}


    
classes = (
    WM_ShowError,
#    Make_NHE_Marker,
    CountSpawns,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
        
#    from bpy.utils import register_class
#    register_class(WM_ShowError)
#    register_class(Make_NHE_Marker)
        
    bpy.types.Scene.sphere_detail_outer = bpy.props.IntProperty( # need another option for inner sphere levels
        name = "",
        description = "Set the number of subdivisions to perform\nwhen creating the outer spheres.\n\nRange: 3-6\nDefault: 4\n\n4 really is enough.",
        default = 4,
        min = 3,
        max = 6
    )
        
    bpy.types.Scene.sphere_detail_inner = bpy.props.IntProperty( # need another option for inner sphere levels
        name = "",
        description = "Set the number of subdivisions to\nperform when creating the spheres.\n\nRange: 3-6\nDefault: 4\n\n4 really is enough.",
        default = 4,
        min = 3,
        max = 6
    )
    
    bpy.types.Scene.sphere_opacity = bpy.props.FloatProperty(
        name = "",
        description = "Range: 0.2-0.8\nDefault: 0.4\n\nSet the opacity for spawn spheres.",
        default = 0.4,
        min = 0.2,
        max = 0.8,
        update = update_sphere_opacity
    )
    bpy.types.Scene.marker_opacity = bpy.props.FloatProperty(
        name = "",
        description = "Range: 0.4-1.0\nDefault: 1.0\n\nSet the opacity for spawn markers.",
        default = 1.0,
        min = 0.4,
        max = 1.0,
        update = update_marker_opacity
    )


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
#    from bpy.utils import unregister_class
#    unregister_class(WM_ShowError)
#    unregister_class(Make_NHE_Marker)
    
    del bpy.types.Scene.sphere_detail_outer
    del bpy.types.Scene.sphere_detail_inner
    del bpy.types.Scene.sphere_opacity
    del bpy.types.Scene.marker_opacity