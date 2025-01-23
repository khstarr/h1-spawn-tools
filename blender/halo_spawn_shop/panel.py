# License

import bpy
from bpy.types import Panel

from .func import update_sphere_color, update_sphere_opacity

#from .operators import get_rig_and_cam, CameraRigMixin

class VIEW_3D_PT_halo_spawn_shop(Panel):
        
    bl_label = "Spawn Shop    v0.7.0"
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
        row.operator("object.spawn_scenery", text="Spawn Scenery")
        row = layout.row()
        row.operator("object.how_to",icon="QUESTION")
        row = layout.row()

# STEP 1
        header, panel = layout.panel("shpa", default_closed=False)
        header.label(text="Shell The Map", icon="EVENT_NDOF_BUTTON_1") # EVENT_NDOF_BUTTON_1 IPO_SINE EVENT_ONEKEY
        header.scale_y = 1.25
        if panel:
            panel.label(text="Select a good sealed BSP:")
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
            right.prop(context.scene, "sphere_detail", text="") # need to add this option for inner sphere
                                    
            panel.operator("object.add_marker", icon = "PMARKER_ACT")
            panel.operator("object.add_sphere", icon = "MESH_CIRCLE")
            # other icons: SHADING_RENDERED NODE_MATERIAL SHADING_RENDERED MESH_CIRCLE
            panel.operator("object.populate_spawns", icon = "POINTCLOUD_DATA")
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


classes = (
    VIEW_3D_PT_halo_spawn_shop,
    CustomProperties
)

       
def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    
    bpy.types.Scene.sphere_color_enum = bpy.props.PointerProperty(
        type = CustomProperties
    )


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)