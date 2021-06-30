import bpy


class DISSOLVE_PT_main_panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Dissolve Shader"
    bl_idname = "DISSOLVE_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "New tab"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("addonname.addbasic_operator")


class DISSOLVE_OT_add_bassic(bpy.types.Operator):
    bl_label= "Add Shadder"
    bl_idname = "addonname.addbasic_operator"


    def execute(self, context):

        material_basic = bpy.data.materials.new(name = "Dissolve")
        material_basic.use_nodes = True


        bpy.context.object.active_material = material_basic
        link = material_basic.node_tree.links.new

        #Principled BSDF Node
        principled_node = material_basic.node_tree.nodes.get("Principled BSDF")
        principled_node.location = (-500, -100)
        link(principled_node.outputs[0], mix_shader_node2.inputs[1])

        #Output Node
        material_out_node = material_basic.node_tree.nodes.get("Material Output")

        #Mix Shader Node 1
        mix_shader_node = material_basic.node_tree.nodes.new("ShaderNodeMixShader")
        mix_shader_node.location = (-200, 300)
        link(mix_shader_node.outputs[0], material_out_node.inputs[0])

        #Mix Shader Node 2
        mix_shader_node2 = material_basic.node_tree.nodes.new("ShaderNodeMixShader")
        mix_shader_node2.location = (-200, 100)
        link(mix_shader_node2.outputs[0], mix_shader_node.inputs[2])

        #Transparent BSFD
        transparent_node = material_basic.node_tree.nodes.new("ShaderNodeBsdfTransparent")
        transparent_node.location = (-400, 250)
        link(transparent_node.outputs[0], mix_shader_node.inputs[1])

        #ColorRamp Node
        color_ramp_node = material_basic.node_tree.nodes.new("ShaderNodeValToRGB")
        color_ramp_node.location = (-700, 300)
        link(color_ramp_node.outputs[0], mix_shader_node.inputs[0])
        link(color_ramp_node.outputs[1], mix_shader_node2.inputs[0])

        #Emission Node
        emission_node = material_basic.node_tree.nodes.new("SHaderNodeEmission")
        color_ramp_node.location = (-500, 100)
        link(color_ramp_node.outputs[0], mix_shader_node.inputs[0])














        return {"FINISHED"}


classes = [DISSOLVE_PT_main_panel, DISSOLVE_OT_add_bassic]



def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
