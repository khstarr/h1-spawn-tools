# License

bl_info = {
    "name": "Halo Spawn Shop",
    "author": "Kendall Starr",
    "version": (0,7,0),
    "blender": (4,3,2),
    "location": "View3D > Tool",
    "description": "Halo 1 spawnalysis and 'random-zone' generator.",
    "doc_url": "https://github.com/khstarr/h1-spawn-tools",
    "tracker_url": "",
    "category": "Add Mesh",
}

import bpy
import os

from . import func
from . import op_how
from . import op_map
from . import op_pop
from . import op_rand
from . import op_spar
from . import panel

import importlib 
# trick blender into reloading scripts:   .-----------------------------.
# uncomment "importlib.reload(error)" below, save this file             /
# disable addon, "Refresh Local", enable addon, observe error          /
# then comment again, save this file, "Refresh Local" enable addon.   /
#importlib.reload(cause_error) #  <---...____________________________/
importlib.reload(func)
importlib.reload(op_how)
importlib.reload(op_map)
importlib.reload(op_pop)
importlib.reload(op_rand)
importlib.reload(op_spar)
importlib.reload(panel)

# =========================================================================
# Registration:
# =========================================================================

def register():
    func.register()
    op_how.register()
    op_map.register()
    op_pop.register()
    op_rand.register()
    op_spar.register()
    panel.register()


def unregister():
    func.unregister()
    op_how.unregister()
    op_map.unregister()
    op_pop.unregister()
    op_rand.unregister()
    op_spar.unregister()
    panel.unregister()


if __name__ == "__main__":
    register()
