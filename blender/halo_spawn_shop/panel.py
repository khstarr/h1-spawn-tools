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
from bpy.types import Panel
from .func import update_sphere_color, update_sphere_opacity, update_marker_color, update_marker_opacity

class VIEW_3D_PT_halo_spawn_shop(Panel):
        
    bl_label = "Spawn Shop    v0.8.8"
    bl_idname = "OBJECT_PT_SpawnShop"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI" # Called with N key
    bl_category = "Spawn Shop"
#    bl_options = {'HIDE_HEADER'} # hides the add-on title header, but makes the whole add-on transparent

    countdowns = {
        -1:"WARNING_LARGE",
        0:"FILE_REFRESH",
        1:"EVENT_ONEKEY",
        2:"EVENT_TWOKEY",
        3:"EVENT_THREEKEY",
        4:"EVENT_FOURKEY",
        5:"EVENT_FIVEKEY",
        10:"EVENT_NDOF_BUTTON_10"
        }
        
    slayer_spawn_count = 0

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        sec_p1 = scene.sec_p1
        sec_p2 = scene.sec_p2
        sec_p3 = scene.sec_p3
        sec_p4 = scene.sec_p4

# HOW TO        
#        row = layout.row()                   # put this header back in
#        row.label(text="Spawn Shop [0.9.9]") # if HIDE_HEADER is in use
#        row = layout.row()
#        row.operator("object.spawn_scenery", text="Spawn Scenery") # not in use
        row = layout.row()
        row.operator("object.how_to",icon="QUESTION")
        row = layout.row()
#        row.operator("object.spawn_marker_nhe",icon="SNAP_NORMAL") # SNAP_NORMAL FRAME_NEXT
#        row = layout.row()

# STEP 1
        header, panel = layout.panel("shpa", default_closed=False)
        header.label(text="Shell The Map")#, icon="EVENT_NDOF_BUTTON_1") # EVENT_NDOF_BUTTON_1 IPO_SINE EVENT_ONEKEY
        header.operator("object.how_shell", text="", icon="INFO") # INFO_LARGE
#        header.scale_y = 1.25
        if panel:
            panel.label(text="Select a sealed BSP:")
            panel.prop(context.scene, "bsp_select", text="")
            panel.prop(context.scene, "apply_solidify_modifier", text="Apply When Completed")
            panel.operator("object.shell_map", icon = "MOD_EDGESPLIT")

# STEP 2
        header, panel = layout.panel("sppa", default_closed=False)
        header.label(text="Populate The Map")#, icon="EVENT_NDOF_BUTTON_2") # EVENT_NDOF_BUTTON_2 IPO_QUAD EVENT_TWOKEY
        header.operator("object.how_populate", text="", icon="INFO") # INFO_LARGE
#        header.scale_y = 1.25
        if panel:
            
            # sphere detail written
            split = panel.split(factor=0.75)
            left = split.column()
            right = split.column()
            left.label(icon="KEY_RING", text="Outer Detail:") # KEY_RING
            left.label(text="Inner Detail:", icon="LAYER_USED") # LAYER_USED
            right.prop(context.scene, "sphere_detail_outer", text="") # need to add this option for inner sphere
            right.prop(context.scene, "sphere_detail_inner", text="") # need to add this option for inner sphere
            
            # tri column with icons
            asp = panel.split(factor=0.12) # opacity XRAY OBJECT_HIDDEN color RESTRICT_COLOR_OFF COLOR RESTRICT_COLOR_ON
            lab = asp.column()
            lab.label(text="")
            lab.label(text="", icon="RESTRICT_COLOR_ON")
            lab.label(text="", icon="XRAY")
            lab.operator("object.count_spawns", text="", icon="LINENUMBERS_ON") # GEOMETRY_NODES LINENUMBERS_ON
            #lab.prop(context.scene, "sphere_detail", text="")
            rtt = asp.column()
            rsp = rtt.split(factor=0.5)
            lab = rsp.column()
            lab.label(text="Spheres")
            lab.prop(context.scene.sphere_color_enum, "sphere_color")
            lab.prop(context.scene, "sphere_opacity", text="")
            lab.operator("object.add_sphere", text="Add 1", icon="MESH_CIRCLE")
            #mid.label(text="", icon="MESH_ICOSPHERE")
            lab = rsp.column()
            lab.label(text="  Markers")
            lab.prop(context.scene.marker_color_enum, "marker_color")
            lab.prop(context.scene, "marker_opacity", text="")
            lab.operator("object.add_marker", text="Add 1", icon="PMARKER_SEL") # OUTLINER_DATA_META SNAP_NORMAL

            if context.scene.slayer_count == 0 :
                panel.operator("object.populate_spawns", icon = "POINTCLOUD_DATA", text="Populate All Spawns")
            else:
                panel.operator("object.populate_spawns", icon = "POINTCLOUD_DATA", text="Populate "+str(context.scene.slayer_count)+" Spawns")
            
            split = panel.split(factor=0.75)
            left = split.column()
            right = split.column()
            #left.label(text="Purge Orphans:")
            right.operator("object.purge_orphans", text="", icon="ORPHAN_DATA") # ORPHAN_DATA INFO_LARGE
#            left.operator("object.commute_markers", text=str(context.scene.slayer_count), icon="COPYDOWN")
            left.operator("object.commute_markers", text="", icon="COPYDOWN")
            
            panel.prop(context.scene.tag_input, "scenery_path", text="", icon="TAG")
            # other icons: SHADING_RENDERED NODE_MATERIAL POINTCLOUD_DATA GEOMETRY_NODES ONIONSKIN_ON

# STEP 3    
        header, panel = layout.panel("rapa", default_closed=False)
        header.label(text="Randoms Geometry")#, icon="EVENT_NDOF_BUTTON_3") # EVENT_NDOF_BUTTON_3 IPO_CUBIC EVENT_THREEKEY
        header.operator("object.how_randoms", text="", icon="INFO")
        #header.scale_y = 1.25
        if panel:
            panel.prop(context.scene, "shell_select", text="", icon="MOD_EDGESPLIT")
            panel.prop(context.scene, "spheres_select", text="", icon="POINTCLOUD_DATA")
            
            row = panel.row()
            split = panel.split(factor=0.55)
            left = split.column()
            right = split.column()
            left.label(text="Boolean solver:")
            row = right.row()
            row.prop(context.scene.boolean_solver_enum, "boolean_solver", expand=True)
            
            panel.prop(context.scene, "apply_randoms_modifier", text="Apply When Completed")
            panel.operator("object.generate_randoms", icon = "HOLDOUT_ON")

# STEP 4
        header, panel = layout.panel("inpa", default_closed=False)
        header.label(text="Gameplay Simulation")#, icon="EVENT_NDOF_BUTTON_4") # EVENT_NDOF_BUTTON_4 IPO_QUART EVENT_FOURKEY
        header.operator("object.how_simulate", text="", icon="INFO")
        #header.scale_y = 1.25
        if panel:
            
            row = panel.row()
            
            split = panel.split(factor=0.75)
            left = split.column()
            right = split.column()
            left.prop(context.scene, "auto_respawn", text="Auto-respawn")
            right.operator("object.generate_spartans", text="+", icon="COMMUNITY")
            
            # add an enum here for Viewport behavior:
            # Options:
            # Don't Move Viewport
            # Look at Spartan
            # Fly to Spartan

            row = panel.row(align=True)
            row.label(text="", icon="SEQUENCE_COLOR_05")
#            row.label(text="", icon="EVENT_ONEKEY")
            row.operator("object.view_spartan", text="", icon="EVENT_ONEKEY").player = 1
            row.prop(context.scene, "player_1_select", text="", icon="USER")
            if bpy.context.scene.player_1_select:
                if bpy.context.scene.player_1_select.hide_get():
                    row.label(text="", icon="RIGHTARROW_THIN")
                else:
                    row.operator("object.kill_spartan", text="", icon="GHOST_DISABLED").player = 1
                row.operator("object.spawn_spartan", text="", icon=self.countdowns[context.scene.sec_p1]).spawner = 1 # FILE_REFRESH
                
            row = panel.row(align=True)
            row.label(text="", icon="SEQUENCE_COLOR_05")
#            row.label(text="", icon="EVENT_TWOKEY")
            row.operator("object.view_spartan", text="", icon="EVENT_TWOKEY").player = 2
            row.prop(context.scene, "player_2_select", text="", icon="USER")
            if bpy.context.scene.player_2_select:
                if bpy.context.scene.player_2_select.hide_get():
                    row.label(text="", icon="RIGHTARROW_THIN")
                else:
                    row.operator("object.kill_spartan", text="", icon="GHOST_DISABLED").player = 2
                row.operator("object.spawn_spartan", text="", icon=self.countdowns[context.scene.sec_p2]).spawner = 2 # FILE_REFRESH

            row = panel.row(align=True)
            row.label(text="", icon="SEQUENCE_COLOR_01")
#            row.label(text="", icon="EVENT_THREEKEY")
            row.operator("object.view_spartan", text="", icon="EVENT_THREEKEY").player = 3
            row.prop(context.scene, "player_3_select", text="", icon="USER")
            if bpy.context.scene.player_3_select:
                if bpy.context.scene.player_3_select.hide_get():
                    row.label(text="", icon="RIGHTARROW_THIN")
                else:
                    row.operator("object.kill_spartan", text="", icon="GHOST_DISABLED").player = 3 
                row.operator("object.spawn_spartan", text="", icon=self.countdowns[context.scene.sec_p3]).spawner = 3 # FILE_REFRESH
                
            row = panel.row(align=True)
            row.label(text="", icon="SEQUENCE_COLOR_01")
#            row.label(text="", icon="EVENT_FOURKEY")
            row.operator("object.view_spartan", text="", icon="EVENT_FOURKEY").player = 4
            row.prop(context.scene, "player_4_select", text="", icon="USER")
            if bpy.context.scene.player_4_select:
                if bpy.context.scene.player_4_select.hide_get():
                    row.label(text="", icon="RIGHTARROW_THIN")
                else:
                    row.operator("object.kill_spartan", text="", icon="GHOST_DISABLED").player = 4 
                row.operator("object.spawn_spartan", text="", icon=self.countdowns[context.scene.sec_p4]).spawner = 4 # FILE_REFRESH

# EXTRAS            
            row = panel.row()
            split = panel.split(factor=0.5)
            left = split.column()
            right = split.column()
            left.label(text="Perspective:")
            row = right.row()
            row.prop(context.scene.perspective_enum, "perspective", expand=True)
            left.label(text="Refresh Rate:")
            row = right.row()
            right.prop(context.scene, "spawn_refresh_rate", text="")
            panel.prop(context.scene, "prediction", text="Real Time Prediction")
        
#        # neat little thing - show (and edit from panel) context.object's location and rotation
#        row = layout.row() 
#        if context.object is not None:
#            layout.label(text=""+context.object.name+"")
#            split = layout.split(factor=1)  # Split the layout 54% left, 46% right
#            col_left = split.column()
#            col_left.prop(context.object, "location", text="Location")
#            col_left.prop(context.object, "rotation_euler", text="Rotation")
                
#       <3 <3 <3
        row = layout.row()
        row.alignment = 'CENTER'
        row.label(text="   Long live Halo 1")



class CustomProperties(bpy.types.PropertyGroup):
    # dropdown menu for color selection
    # this class must come after 'def update_sphere_color'
    sphere_color : bpy.props.EnumProperty(
        name="",
        description="Sphere color",
        items=[
            ('red',"Red","Spheres will be red, like the blood of your enemies."),
            ('blue',"Blue","Spheres will probably get top spawn."),
            ('green',"Green","Spheres will be good for the environment."),
            ('yellow',"Yellow","Spheres will be yellow. Like the sun."),
            ('gray',"Gray","Spheres will look like fog balls."),
            ('black',"Black","Spheres will be great for seeing through.")
        ],
        update = update_sphere_color
    )
    
    marker_color : bpy.props.EnumProperty(
        name="",
        description="Marker color",
        items=[ 
            ('green',"Green","Markers will be good for the environment."),
            ('white',"White","Markers will look smokey."),
            ('yellow',"Yellow","Markers will look like bananas."),
            ('purple',"Purple","Markers will be loved by the Covenant."),
            ('black',"Black","Markers will be hard to see.")
        ],
        update = update_marker_color
    )
    
    perspective : bpy.props.EnumProperty(
        name="Team",
        description="Choose team perspective for spawn influence computation.",
        items=[
            ('blue','Blue',"Show spawn spheres from blue's perspective."),
            ('red',"Red","Show spawn spheres from red's perspective.")
        ]
    )
    
    boolean_solver : bpy.props.EnumProperty(
        name="Solver",
        description="Select a solver for the boolean operation. 'Exact' is slow, 'Fast' is inaccurate.",
        items=[
            ('FAST','Fast',"Use 'Fast' when running the boolean modifier to cut spheres from shell."),
            ('EXACT','Exact',"Use 'Exact' when running the boolean modifier to cut spheres from shell.")
        ]
    )
    
    scenery_path: bpy.props.StringProperty(
        name="",
        description="Set the path for the [marker].scenery",
        default="scenery\spawn_marker_nhe\spawn_marker_nhe.scenery",
        maxlen=1024,
    )
        
    

classes = (
    VIEW_3D_PT_halo_spawn_shop,
    CustomProperties
)

       
def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
        
    bpy.types.Scene.slayer_count = bpy.props.IntProperty()

    bpy.types.Scene.tag_input = bpy.props.PointerProperty(
        type = CustomProperties,
        name = "Marker Scenery Path",
        description = ""
    )
    
    bpy.types.Scene.sphere_color_enum = bpy.props.PointerProperty(
        type = CustomProperties,
        name = "SphereColorizer",
        description = "Color selector for spheres"
    )
    
    bpy.types.Scene.marker_color_enum = bpy.props.PointerProperty(
        type = CustomProperties,
        name = "MarkerColorizer",
        description = "Color selector for markers"
    )
    
    bpy.types.Scene.perspective_enum = bpy.props.PointerProperty(
        type = CustomProperties,
        name = "Team Perspective",
        description = "Spawn influence team perspective"
    )
    
    bpy.types.Scene.boolean_solver_enum = bpy.props.PointerProperty(
        type = CustomProperties,
        name = "Boolean Solver",
        description = "Randoms generation boolean solver method"
    )


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)

    del bpy.types.Scene.slayer_count
    del bpy.types.Scene.tag_input
    
    del bpy.types.Scene.sphere_color_enum
    del bpy.types.Scene.marker_color_enum
    del bpy.types.Scene.perspective_enum
    del bpy.types.Scene.boolean_solver_enum