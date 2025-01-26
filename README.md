# H1 Spawn Tools

This repository is for Halo 1 multiplayer level designers. Included are tools and resources for optimizing spawn points for competitive play when designing a map.

## Requirements

The instructions and processes described in this writeup have been tested in a Windows environment, using the H1EK (included in the Master Chief Collection Steam release). The process for generating "randoms" geometry is only available to Blender users (Halo Spawn Shop add-on has been tested on Blender 4.3). The Blender add-on was designed to work with Player Starting Location data imported from a Scenario Tag using the [Halo Asset Blender Development Tools](https://github.com/General-101/Halo-Asset-Blender-Development-Toolset). The automated process for placing spawn marker scenery in the Scenario tag currently requires the use of a Windows batch script, as well as a specific outdated version of [Invader](https://github.com/SnowyMouse/invader) (compatible versions are included in the */_redist/* folder). There are NO PLANS to support Mac/Linux users, 3ds Max users, or users still creating content with the original HEK (released for Custom Edition). The repository and associated tools are offered as-is, as development tools for advanced users, and may never improve or be updated for compatibility with newer versions of Blender, Invader, or the H1EK.

# Halo 1 Spawn System

For detailed information about Halo 1's spawn system, refer to the excellent [Halo Spawns website](https://www.halospawns.com/) (created by Mintograde). There is also a writeup tailored for level designers available on the [c20 Reclaimers Library](https://c20.reclaimers.net/h1/guides/multiplayer/player-spawns/).

# How to Use this Repository

There is no build/compile process for this repository. Simply download the source files from your browser or clone the repository to your local machine.

# Workflows

This section covers the high-level workflows that are possible with the tools & resources available in this repository.

## Generating "Randoms" Geometry, Checking Spawn Point Influence Range, and Real-Time Simulation of Spawn Selection Logic (in Blender)

Before starting, you will need all the Player Starting Location scenario data in your scene, which can be obtained by importing a Scenario Tag with the [Halo Asset Blender Development Tools](https://github.com/General-101/Halo-Asset-Blender-Development-Toolset). Refer to that tool's instructions/documentation for details about this process. 

Install the Halo Spawn Shop add-on by copying the */blender/halo_spawn_shop/* folder from this repository to your local Blender */scripts/* folder (by default, this is *%appdata%/Blender Foundation/Blender/4.3/scripts/addons*). In Blender, navigate to Edit menu > Preferences > Add-ons and enable the **Halo Spawn Shop** add-on from the list.

Expand the newly-added Spawn Shop widget in the Viewport and click on the *How To* button at the top of the interface for detailed instructions on the tool's capabilities:

[*] **Place spawn "influence spheres" at each spawn point location:** this is useful for distancing spawn points correctly and for fine-tuning spawn placements for forced/random spawns.
[*] **Generate the "random spawn" geometry:** this feature covers the map in a "shell" using the Solidify modifier, then uses a boolean operation based on the spawn "influence spheres" placed in the previous step in order to remove all areas of the shell geometry that are within the influence range of Slayer spawn points.
[*] **Gameplay Simulation:** this feature allows level designers to simulate the game's spawn selection logic in real-time, with up to 2 players on each team. You can place "friendly" and "enemy" player reference models and move them around the scene, which changes the opacity of the spawn "influence spheres" (higher opacity = higher chance of the spawn point being selected).

## Inserting Spawn Marker Scenery in a Scenario Tag

First, you will need to install the included custom spawn marker scenery tags. Copy */tags/scenery/spawn_marker_nhe/* to your current tags folder.

Next, install one of the legacy versions of Invader included in the /_redist/ folder for compatibility (technically, only *invader-edit.exe* is required). Be sure to back up any previous Invader installations (if applicable). During testing, Invader was installed in the same location as */data/* and */tags/* directories (typically the *Chelan_1* folder). Finally, place **injector.bat** in the same folder as Invader (which should be in the same location as your */data/* & */tags/* folders).

When running **injector.bat**, you will be prompted to specify your */tags/* folder and the path equivalent of a */levels/test/* directory. You will then be prompted to select a scenario tag from the specified directory (the script will automatically make a copy and rename it based on UNIX timestamp).

Once a scenario tag has been selected, several options are available. In this case, select **[4] Inject spawn markers**. The script will then use *invader-edit* to iterate through all spawn points enabled for Slayer gametypes, and place the spawn marker scenery object at each location.

When finished, simply exit the command line interface and verify the scenery object placements in Sapien.

# Acknowledgements

[*] Halo Spawn Shop Blender add-on created by insidi0us
[*] Batch script for injecting spawn marker scenery created by insidi0us
[*] Custom spawn marker scenery created by stunt_man
[*] Special thanks to General-101 for the [Halo Asset Blender Development Tools](https://github.com/General-101/Halo-Asset-Blender-Development-Toolset)
[*] Special thanks to Snowy for [Invader](https://github.com/SnowyMouse/invader)
[*] Special thanks to insidi0us, Mintograde and ChaosTheory for reverse-engineering the game's spawn selection logic