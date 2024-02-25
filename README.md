# DO NOT USE, CONTAINS LEAK THAT BLOATS SIZE OF YOUR BLEND FILE - see [this issue](https://projects.blender.org/blender/blender/issues/118642) for details

I don't know when or if I will get around to fixing this, this addon is not part of my workflow any more - using linked libraries primarily instead.

---

# Blender "Edit Instanced Collection" Add-on
This is a fork/rewrite of [SuperFLEB/BlenderEditCollectionAddon](https://github.com/SuperFLEB/BlenderEditCollectionAddon)

The changes I've made facilitate a faster, cleaner workflow in my opinion.

The add-on allows you to select an instanced collection in your scene, hit a button (either from the Object menu - "Edit Instanced Collection", or the hot-key Ctrl+Alt+C), and instantly stage the source collection for editing. The differences from FLEB's add-on are described below.

## Collection Stages

Collection stages are isolated scenes that contain only the source collection for your editing. A simple but needed change to FLEB's add-on is that these stage scenes are designed to be **re-used**. You can leave and come back to the same scene with no duplication of scenes, and no 'clean-up' necessary.

## Collection Staging Workspace

This is the most important addition in terms of workflow. In the preferences of this add-on, you can set a dedicated workspace for staging and editing collections. In combination with pinning the staging scene to the workspace (which is activated automatically), you can preserve the viewport and original scene of your other workspaces, effectively separating it. This reduces disruption and facilitates a faster, cleaner workflow.

Make sure the workspace that you type into the add-on preferences actually exists in the blend file/is spelled correctly.

If you use the [Synchronize Workspaces](https://m-soluyanov.gumroad.com/l/afoty) add-on, turn off synchronization for your collection staging workspace.

### A Recommendation

After amassing a lot of collections, you may build up a fairly large list of stage scenes. Instead of using the normal scene drop-down box near the top right of the tool-bar, you may want a more easily accessible list of your scenes. Use a **second Outliner panel set to 'Scenes' mode** in your collection staging workspace. Collapse in all the scene fold-outs so you just have a list of scene names. Clicking on them jumps to that scene.

## Collection Stages World

In the preferences, you can also set the name of a world you'd like to use when creating stage scenes. If you leave it blank, the world will be copied over from the previous scene you were in before creating the stage scene.

## Installation

Download this repository as a ZIP, and install it like any other Blender add-on.
