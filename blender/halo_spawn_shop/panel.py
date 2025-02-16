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
from .op_sim import update_tracking, update_prediction_bool

class VIEW_3D_PT_halo_spawn_shop(Panel):
        
    bl_label = "Spawn Shop    v0.9.1"
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
#            split = panel.split(factor=0.75)
#            left = split.column()
#            right = split.column()
#            left.label(icon="KEY_RING", text="Outer Detail:") # KEY_RING
#            left.label(text="Inner Detail:", icon="LAYER_USED") # LAYER_USED
#            right.prop(context.scene, "sphere_detail_outer", text="") # need to add this option for inner sphere
#            right.prop(context.scene, "sphere_detail_inner", text="") # need to add this option for inner sphere
            
            # sphere detail condensed
#            split = panel.split(factor=0.5)
#            left = split.column()
#            middle = split.column()
#            right = split.column()
#            left.label(icon="NODE_MATERIAL", text="Detail:")
#            middle.prop(context.scene, "sphere_detail_outer", text="")
#            right.prop(context.scene, "sphere_detail_inner", text="")
            
            # sphere detail row
            sphere_row_split = panel.split(factor=0.5)
            sphere_detail = sphere_row_split.column() # 50% of total width
            sphere_detail.label(text="Sphere Detail:")
            controls = sphere_row_split.column() # 50% of total width
            row = controls.row(align=True)
            row.prop(context.scene, "sphere_detail_outer", text="")
            row.prop(context.scene, "sphere_detail_inner", text="")
#            add_column.operator("object.add_sphere", text="+")
            
            # sphere color/opacity row
            sphere_row_split = panel.split(factor=0.1)
            sphere_icon = sphere_row_split.column() # 10% of total width
            sphere_icon.label(icon="NODE_MATERIAL", text="")
            controls_and_add = sphere_row_split.column() # 90% of total width
            controls_and_add_split = controls_and_add.split(factor=0.8)
            middle_columns = controls_and_add_split.column()  # 80% of 90% = 72% of total width
            add_column = controls_and_add_split.column() # 20% of 90% = 18% of total width
            row = middle_columns.row(align=True)
            row.prop(context.scene.sphere_color_enum, "sphere_color")
            row.prop(context.scene, "sphere_opacity", text="")
            add_column.operator("object.add_sphere", text="", icon="ADD")
            
            # marker color/opacity row
            marker_row_split = panel.split(factor=0.1)
            marker_icon = marker_row_split.column() # 10% of total width
            marker_icon.label(icon="PMARKER_SEL", text="")
            controls_and_add = marker_row_split.column() # 90% of total width
            controls_and_add_split = controls_and_add.split(factor=0.8)
            middle_columns = controls_and_add_split.column()  # 80% of 90% = 72% of total width
            add_column = controls_and_add_split.column() # 20% of 90% = 18% of total width
            row = middle_columns.row(align=True)
            row.prop(context.scene.marker_color_enum, "marker_color")
            row.prop(context.scene, "marker_opacity", text="")
            add_column.operator("object.add_marker", text="", icon="ADD")
            
            # tri column with icons
#            asp = panel.split(factor=0.12) # opacity XRAY OBJECT_HIDDEN color RESTRICT_COLOR_OFF COLOR RESTRICT_COLOR_ON
#            lab = asp.column()
#            lab.label(text="")
#            lab.label(text="", icon="RESTRICT_COLOR_ON")
#            lab.label(text="", icon="XRAY")
#            lab.label(text="", icon="ADD")
##            lab.operator("object.count_spawns", text="", icon="LINENUMBERS_ON") # GEOMETRY_NODES LINENUMBERS_ON
#            #lab.prop(context.scene, "sphere_detail", text="")
#            rtt = asp.column()
#            rsp = rtt.split(factor=0.5)
#            lab = rsp.column()
#            lab.label(text="Spheres")
#            lab.prop(context.scene.sphere_color_enum, "sphere_color")
#            lab.prop(context.scene, "sphere_opacity", text="")
#            lab.operator("object.add_sphere", text="Add 1", icon="MESH_CIRCLE")
#            #mid.label(text="", icon="MESH_ICOSPHERE")
#            lab = rsp.column()
#            lab.label(text="  Markers")
#            lab.prop(context.scene.marker_color_enum, "marker_color")
#            lab.prop(context.scene, "marker_opacity", text="")
#            lab.operator("object.add_marker", text="Add 1", icon="PMARKER_SEL") # OUTLINER_DATA_META SNAP_NORMAL

            asp = panel.split(factor=0.12)
            lab = asp.column()
            lab.operator("object.count_spawns", text="", icon="LINENUMBERS_ON") # GEOMETRY_NODES LINENUMBERS_ON
            rtt = asp.column()
            if context.scene.slayer_count == 0 :
#                panel.operator("object.populate_spawns", icon = "POINTCLOUD_DATA", text="Populate All Spawns")
                rtt.operator("object.populate_spawns", icon = "POINTCLOUD_DATA", text="Populate All Spawns")
            else:
#                panel.operator("object.populate_spawns", icon = "POINTCLOUD_DATA", text="Populate "+str(context.scene.slayer_count)+" Spawns")
                rtt.operator("object.populate_spawns", icon = "POINTCLOUD_DATA", text="Populate "+str(context.scene.slayer_count)+" Spawns")
            
            split = panel.split(factor=0.75)
            left = split.column()
            right = split.column()
            #left.label(text="Purge Orphans:")
            right.operator("object.purge_orphans", text="", icon="ORPHAN_DATA") # ORPHAN_DATA INFO_LARGE
#            left.operator("object.commute_markers", text=str(context.scene.slayer_count), icon="COPYDOWN")
            left.operator("object.commute_markers", text="Scenery", icon="COPYDOWN")
            
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
            
            split = panel.split(factor=0.25)
            left = split.column()
            right = split.column()
            three = right.split(factor=0.67)
#            l = three.column()
            m = three.column()
            r = three.column()
#            l.label(text="Auto:")
            left.prop(context.scene, "auto_view", text="", icon="VIEW_CAMERA_UNSELECTED")
            m.operator("object.generate_spartans", text="+2v2  ", icon="COMMUNITY")
            r.prop(context.scene, "auto_respawn", text="", icon="RECOVER_LAST") # RECOVER_LAST FILE_REFRESH

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
            panel.prop(context.scene, "prediction", text="Real Time Prediction", icon="ORIENTATION_GIMBAL", toggle=1)
            # PIVOT_ACTIVE MEMORY NORMALIZE_FCURVES
                            
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
            ('EXACT','Exact',"Use 'Exact' when running the boolean modifier to cut spheres from shell."),
            ('FAST','Fast',"Use 'Fast' when running the boolean modifier to cut spheres from shell.")
        ],
        default='EXACT'
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
        
    # Shell The Map
    bpy.types.Scene.bsp_select = bpy.props.PointerProperty(
        name = "",
        description = "Please select a perfect manifold (STL Checked)\nsealed world. No holes (or it won't shell nicely)!",
        type = bpy.types.Object)
        
    bpy.types.Scene.apply_solidify_modifier = bpy.props.BoolProperty(
        name = "Apply",
        description = "Apply the modifier when the 'Solidify' operation\ncompletes, or leave unchecked to tweak settings.",
        default = True)
        
    
    # Populate The Map
    bpy.types.Scene.sphere_detail_outer = bpy.props.IntProperty(default = 4, min = 3, max = 6,
        name = "",
        description = "Outer Sphere Detail\n\nRange: 3-6\nDefault: 4\n\n(Number of subdivisions when creating the outer spheres)")
        
    bpy.types.Scene.sphere_detail_inner = bpy.props.IntProperty(default = 4, min = 3, max = 6,
        name = "",
        description = "Inner Sphere Detail\n\nRange: 3-6\nDefault: 4\n\n(Number of subdivisions when creating the inner spheres)")
        
    bpy.types.Scene.sphere_color_enum = bpy.props.PointerProperty(
        name = "SphereColorizer",
        description = "Color selector for spheres",
        type = CustomProperties)
        
    bpy.types.Scene.marker_color_enum = bpy.props.PointerProperty(
        name = "MarkerColorizer",
        description = "Color selector for markers",
        type = CustomProperties)
        
    bpy.types.Scene.sphere_opacity = bpy.props.FloatProperty(default = 0.4, min = 0.2, max = 0.8,
        name = "",
        description = "Sphere Opacity\n\nRange: 0.2-0.8\nDefault: 0.4\n\nSet the opacity for spawn spheres.",
        update = update_sphere_opacity)

    bpy.types.Scene.marker_opacity = bpy.props.FloatProperty(default = 1.0, min = 0.4, max = 1.0,
        name = "",
        description = "Marker Opacity\n\nRange: 0.4-1.0\nDefault: 1.0\n\nSet the opacity for spawn markers.",
        update = update_marker_opacity)
    
    bpy.types.Scene.slayer_count = bpy.props.IntProperty()
    
    
    # Randoms Geometry
    bpy.types.Scene.shell_select = bpy.props.PointerProperty(
        name = "",
        description = "Select the shelled BSP created in Step 1",
        type = bpy.types.Object)
        
    bpy.types.Scene.spheres_select = bpy.props.PointerProperty(
        name = "Spheres Collection",
        description = "Select the collection of Spheres to cut from the shell.",
        type = bpy.types.Collection)
    
    bpy.types.Scene.boolean_solver_enum = bpy.props.PointerProperty(
        name = "Boolean Solver",
        description = "Randoms generation boolean solver method",
        type = CustomProperties)
    
    bpy.types.Scene.apply_randoms_modifier = bpy.props.BoolProperty(
        name = "Apply",
        description = "Apply the modifier when the boolean operation\ncompletes, or leave unchecked to tweak settings.",
        default = True)
        
    bpy.types.Scene.tag_input = bpy.props.PointerProperty(
        name = "Marker Scenery Path",
        description = "",
        type = CustomProperties)
    
    
    # Gameplay Simulation
    bpy.types.Scene.auto_respawn = bpy.props.BoolProperty(
        name = "Auto-respawn",
        description = "Countdown from 5 and then automatically respawn the dead player.",
        default = True)
        
    bpy.types.Scene.auto_view = bpy.props.BoolProperty(
        name = "Auto-view",
        description = "Upon respawn, move the main viewport to the Spartan's location.",
        default = True)
        
    bpy.types.Scene.player_1_select = bpy.props.PointerProperty(
        name = "",
        description = "Select Player 1 (Blue Team)",
        type = bpy.types.Object,
        update = update_tracking)
    
    bpy.types.Scene.player_2_select = bpy.props.PointerProperty(
        name = "",
        description = "Select Player 2 (Blue Team)",
        type = bpy.types.Object,
        update = update_tracking)
    
    bpy.types.Scene.player_3_select = bpy.props.PointerProperty(
        name = "",
        description = "Select Player 3 (Red Team)",
        type = bpy.types.Object,
        update = update_tracking)
    
    bpy.types.Scene.player_4_select = bpy.props.PointerProperty(
        name = "",
        description = "Select Player 4 (Red Team)",
        type = bpy.types.Object,
        update = update_tracking)

    bpy.types.Scene.sec_p1 = bpy.props.IntProperty(default = 0, min = 0, max = 10,
        name = "",
        description = "Respawn time remaining")
        
    bpy.types.Scene.sec_p2 = bpy.props.IntProperty(default = 0, min = 0, max = 10,
        name = "",
        description = "Respawn time remaining",)
        
    bpy.types.Scene.sec_p3 = bpy.props.IntProperty(default = 0, min = 0, max = 10,
        name = "",
        description = "Respawn time remaining")
        
    bpy.types.Scene.sec_p4 = bpy.props.IntProperty(default = 0, min = 0, max = 10,
        name = "",
        description = "Respawn time remaining")
        
    bpy.types.Scene.perspective_enum = bpy.props.PointerProperty(
        name = "Team Perspective",
        description = "Spawn influence team perspective",
        type = CustomProperties)
    
    bpy.types.Scene.spawn_refresh_rate = bpy.props.FloatProperty(default = 0.05, min = 0.01, max = 1,
        name = "",
        description = "Range: 0.01-1.0\nDefault: 0.05\n\nSet the spawn analysis refresh rate.\nLower value = faster updates, higher CPU tax.")
        
    bpy.types.Scene.prediction = bpy.props.BoolProperty(
        name = "Real Time Tracking",
        description = "Show and hide spawn markers and influence spheres\nbased on the locations of the selected Spartan objects.",
        update = update_prediction_bool,
        default = False)
        


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
        
    # Shell The Map
    del bpy.types.Scene.bsp_select
    del bpy.types.Scene.apply_solidify_modifier
    
    # Populate The Map
    del bpy.types.Scene.sphere_detail_outer
    del bpy.types.Scene.sphere_detail_inner
    del bpy.types.Scene.sphere_color_enum
    del bpy.types.Scene.marker_color_enum
    del bpy.types.Scene.sphere_opacity
    del bpy.types.Scene.marker_opacity
    del bpy.types.Scene.slayer_count
    
    # Randoms Geometry
    del bpy.types.Scene.shell_select
    del bpy.types.Scene.spheres_select
    del bpy.types.Scene.boolean_solver_enum
    del bpy.types.Scene.apply_randoms_modifier
    del bpy.types.Scene.tag_input
    
    # Gameplay Simulation
    del bpy.types.Scene.auto_respawn
    del bpy.types.Scene.auto_view
    del bpy.types.Scene.player_1_select
    del bpy.types.Scene.player_2_select
    del bpy.types.Scene.player_3_select
    del bpy.types.Scene.player_4_select
    del bpy.types.Scene.perspective_enum
    del bpy.types.Scene.spawn_refresh_rate
    del bpy.types.Scene.prediction
    del bpy.types.Scene.sec_p1
    del bpy.types.Scene.sec_p2
    del bpy.types.Scene.sec_p3
    del bpy.types.Scene.sec_p4