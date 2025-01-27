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

bl_info = {
    "name": "Halo Spawn Shop",
    "author": "insidi0us",
    "version": (0,8,1),
    "blender": (4,3,2),
    "location": "View3D > Tool",
    "description": "Halo 1 spawn engine analysis tool.",
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
# trick blender into reloading scripts:   .----------------------------.
# uncomment "importlib.reload(error)" below, save this file            /
# disable addon, enable addon, observe 'cause_error' not defined      /
# then comment again, save this file, enable addon. profit.          /
#                                                                   /
#importlib.reload(cause_error) #  <---...__________________________/
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
