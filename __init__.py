import bpy

bl_info = {
    "name": "Edit Instanced Collection",
    "description": "Edit a Collection Instance's source Collection (even if it is not in the Scene).",
    "author": "FLEB, Albert O'Shea",
    "version": (1, 0, 0),
    "blender": (3, 1, 0),
    "location": "Object > Edit Instanced Collection",
    "doc_url": "https://github.com/AMC-Albert/BlenderEditInstancedCollection",
    "tracker_url": "https://github.com/AMC-Albert/BlenderEditInstancedCollection/issues",
    "support": "COMMUNITY",
    "category": "Object",
}

addon_keymaps = []
package_name = __package__

class EditCollection(bpy.types.Operator):
    """Edit the Collection referenced by this Collection Instance in a new Scene"""
    bl_idname = "object.edit_collection"
    bl_label = "Edit Instanced Collection"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        def change_scene_on_next_workspace(scene):
            owner = object()
            subscribe_to = bpy.types.Window, "workspace"

            def msgbus_callback(*args):
                for area in bpy.context.screen.areas:
                    with bpy.context.temp_override(area=area):
                        bpy.context.window.scene = bpy.data.scenes.get(scene)
                # Clear subscription
                bpy.msgbus.clear_by_owner(owner)

            # Subscribe to workspace changes
            bpy.msgbus.subscribe_rna(
                key=subscribe_to,
                owner=owner,
                args=(1, 2, 3),
                notify=msgbus_callback,
        )

        prefs = context.preferences.addons[package_name].preferences
        coll = bpy.context.active_object.instance_collection

        if not coll:
            print("Active item is not a collection instance")
            self.report({"WARNING"}, "Active item is not a collection instance")
            return {"CANCELLED"}

        scene_name = f"stage:{coll.name}"
        previous_scene_name = bpy.context.scene.name

        if bpy.data.scenes.get(scene_name) is None:
            bpy.ops.scene.new(type="EMPTY")
            bpy.context.window.scene.name = scene_name

            if prefs.world_name != "":
                if bpy.data.worlds.get(prefs.world_name) is not None:
                    bpy.context.window.scene.world = bpy.data.worlds.get(prefs.world_name)
                else:
                    self.report({"WARNING"}, f"World '{prefs.world_name}' doesn't exist.")
                    print(f"World '{prefs.world_name}' doesn't exist.")
                    bpy.context.window.scene.world = bpy.data.scenes.get(previous_scene_name).world
            else:
                bpy.context.window.scene.world = bpy.data.scenes.get(previous_scene_name).world

            bpy.context.window.scene = bpy.data.scenes.get(previous_scene_name)

        if prefs.workspace_name != "":
            if prefs.workspace_name in bpy.data.workspaces:
                change_scene_on_next_workspace(scene_name)
                bpy.context.window.workspace = bpy.data.workspaces[prefs.workspace_name]
                if prefs.pin_scene:
                    bpy.data.workspaces.get(prefs.workspace_name).use_pin_scene = True
            else:
                bpy.context.window.scene = bpy.data.scenes.get(scene_name)
                self.report({"WARNING"}, f"Workspace '{prefs.workspace_name}' doesn't exist.")
                print(f"Workspace '{prefs.workspace_name}' doesn't exist.")
        else:
            bpy.context.window.scene = bpy.data.scenes.get(scene_name)

        if coll.name not in bpy.data.scenes.get(scene_name).collection.children:
            bpy.data.scenes.get(scene_name).collection.children.link(coll)

        return {"FINISHED"}


class EditInstancedCollectionPreferences(bpy.types.AddonPreferences):
    bl_idname = package_name
    workspace_name: bpy.props.StringProperty(
        name="Collection staging workspace",
        description="The name of a workspace that exists in this blend file to switch to when staging a collection source. Set blank to disable switching workspaces automatically",
        default=""
        )
    pin_scene: bpy.props.BoolProperty(
        name="Pin stage scene to workspace",
        description="Automatically pin the collection stage scene to the workspace defined above. Recommended for keeping your collection stages isolated to this workspace, while the rest of your workspaces remain viewing to your main scene",
        default=True
        )
    world_name: bpy.props.StringProperty(
        name="Collection staging world",
        description="The name of a world that exists in this blend file to use when creating colleciton stage scenes. Set blank to copy over the world of the previous scene",
        default=""
        )
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "workspace_name")
        layout.prop(self, "pin_scene")
        layout.prop(self, "world_name")

def menu_function(self, context):
    if bpy.context.active_object.instance_collection:
        self.layout.operator(EditCollection.bl_idname)

def register():
    # Register classes
    bpy.utils.register_class(EditCollection)
    bpy.utils.register_class(EditInstancedCollectionPreferences)

    # Add menu items
    bpy.types.VIEW3D_MT_object.append(menu_function)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_function)

    # Add keymaps
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.new(name="Object Mode", space_type="EMPTY")
        kmi = km.keymap_items.new(EditCollection.bl_idname, "C", "PRESS", ctrl=True, alt=True)
        # kmi.properties.total = 4
        addon_keymaps.append((km, kmi))


def unregister():
    # Unregister classes
    bpy.utils.unregister_class(EditCollection)
    bpy.utils.unregister_class(EditInstancedCollectionPreferences)

    # Remove menu items
    bpy.types.VIEW3D_MT_object.remove(menu_function)
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_function)

    # Clear keymaps
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()
