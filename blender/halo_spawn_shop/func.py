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
    SpawnShopCollection = bpy.data.collections.get("Spawn Shop")
    if SpawnShopCollection:
        print("Spawn Shop collection already exists, which is good. Proceeding.")
    else:
        SpawnShopCollection = bpy.data.collections.new("Spawn Shop")
        bpy.context.scene.collection.children.link(SpawnShopCollection)
    
    # CREATE INNER ICOSPHERE
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=bpy.context.scene.sphere_detail,
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
        subdivisions=bpy.context.scene.sphere_detail,
        radius=600,
        enter_editmode=False,
        align='WORLD',
        location=(0, 0, 0),
        scale=(1, 1, 1)
    )

    sphere = bpy.context.active_object
    sphere.data.name = "Sample Sphere Mesh"
    sphere.name = "Sample Sphere [Detail "+str(bpy.context.scene.sphere_detail)+"]"
    
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



#class SpawnScenery(Operator): # not in use
#    bl_idname = "object.spawn_scenery"
#    bl_label = "Spawn Scenery"
#    bl_description = "Place a spawn scenery item at every Slayer spawn."
#    
#    def execute(self, context):

#        print("hoping and trying and possibly placing scenery...")
#        
#        game_version = "halo1"
#        
#        # get_object_mesh stuff here:
#        script_folder_path = path.dirname(path.dirname(__file__))
#        p = path.join(script_folder_path, "resources")
#        p = bpy.utils.user_resource('SCRIPTS') + "\\addons\\halo_spawn_shop\\jms\\"
#        f = "jackal.jms"
#        filepath = p+f
#        
#        # dimensions aren't used unless item not found,
#        # then makes a box with these dimensions:
#        array_item = ("jackal", (2.66301, 8.74704, 17.708))

#        # start from bottom:
#        mesh_processing.deselect_objects(context)
#        
#        # then create empty and select it
#        n = "" # needs to come from looping through spawn points (or spheres, during that operation).
#        # also, copy this mesh once created, don't generate every iteration in the loop.
#        object_name = "spawn_marker"+n
#        mesh = scale_models.generate_mesh(filepath, array_item, game_version)
#        print(mesh)
#        object_mesh = bpy.data.objects.new(object_name, mesh)
#        context.collection.objects.link(object_mesh)
#        object_mesh.select_set(True)
#        
#        return {"FINISHED"}

def register():
    from bpy.utils import register_class
    register_class(WM_ShowError)
        
    bpy.types.Scene.sphere_detail = bpy.props.IntProperty( # need another option for inner sphere levels
        name = "",
        description = "Range: 3-6\nDefault: 4\n\nSet the number of subdivisions to\nperform when creating the spheres.\n4 really is enough.",
        default = 4,
        min = 3,
        max = 6
    )
    bpy.types.Scene.sphere_opacity = bpy.props.FloatProperty(
        name = "",
        description = "Range: 0.2-0.8\nDefault: 0.4\n\nSet the opacity for spawn\nspheres and markers.",
        default = 0.4,
        min = 0.2,
        max = 0.8,
        update = update_sphere_opacity
    )


def unregister():
    from bpy.utils import unregister_class
    unregister_class(WM_ShowError)
    
    del bpy.types.Scene.sphere_detail
    del bpy.types.Scene.sphere_color_enum