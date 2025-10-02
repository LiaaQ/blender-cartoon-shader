bl_info = {
    "name": "Cartoon Shader Creator",
    "description": "Creates a cartoon shader material.",
    "author": "Natalie Teplicka",
    "version": (1, 0, 0),
    "blender": (4, 3, 2),
    "location": "View3D > UI Panel > Cartoon Shader",
    "category": "Material"
}

import bpy

class MATERIAL_OT_cartoon_shader(bpy.types.Operator):
    """Create a Cartoon Shader with Options"""
    bl_idname = "material.create_cartoon_shader"
    bl_label = "Create Cartoon Shader"
    bl_options = {'REGISTER', 'UNDO'}
    obj = None

    shades_positions = [[0.000],
                        [0.405, 0.000],
                        [0.514, 0.375, 0.000],
                        [0.534, 0.400, 0.337, 0.000],
                        [0.567, 0.517, 0.400, 0.321, 0.000],
                        [0.585, 0.517, 0.455, 0.400, 0.325, 0.000],
                        [0.541, 0.498, 0.450, 0.422, 0.404, 0.345, 0.000],
                        [0.592, 0.545, 0.510, 0.488, 0.464, 0.421, 0.370, 0.000],
                        [0.659, 0.633, 0.578, 0.539, 0.496, 0.476, 0.462, 0.416, 0.000],
                        [0.701, 0.659, 0.633, 0.578, 0.539, 0.496, 0.476, 0.462, 0.416, 0.000]]

    def execute(self, context):
        obj = context.active_object
        if not obj:
            self.report({'INFO'}, "No Active Object.")
            return {'CANCELLED'}
        obj.active_material = self.create_cartoon_shader(context.scene)
        self.create_outline(context.scene)
        self.report({'INFO'}, "Cartoon Shader created.")
        return {'FINISHED'}

    def create_cartoon_shader(self, scene):
        mat_name = "Cartoon_Shader"

        main_color = scene.main_color
        num_shades = scene.num_shades

        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        # Clear default nodes
        for node in nodes:
            nodes.remove(node)

        # Create nodes
        diffuse_node = nodes.new(type='ShaderNodeBsdfPrincipled')
        diffuse_node.location = (-550, 0)
        diffuse_node.inputs['Base Color'].default_value = main_color

        shader_to_rgb_node = nodes.new(type='ShaderNodeShaderToRGB')
        shader_to_rgb_node.location = (-200, 0)

        color_ramp_node = nodes.new(type='ShaderNodeValToRGB')
        color_ramp_node.location = (0, 0)

        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (300, 0)

        # Link nodes
        links.new(diffuse_node.outputs['BSDF'], shader_to_rgb_node.inputs['Shader'])
        links.new(shader_to_rgb_node.outputs['Color'], color_ramp_node.inputs['Fac'])
        links.new(color_ramp_node.outputs['Color'], output_node.inputs['Surface'])

        # Customize the Color Ramp with the number of shades
        color_ramp_node.color_ramp.interpolation = 'CONSTANT'
        while len(color_ramp_node.color_ramp.elements) > 1:
            color_ramp_node.color_ramp.elements.remove(color_ramp_node.color_ramp.elements[0])

        # Get the initial color
        base_color = main_color[:3]  # Ignore the alpha component
        alpha = main_color[3]

        # Add elements based on the number of shades
        for i in range(num_shades):
            pos = self.shades_positions[num_shades-1][i]
            print(pos)
            element = color_ramp_node.color_ramp.elements.new(pos)
        
        # Calculate the new color by scaling the base color
            scale_factor = 1.0 - (i * (1 / num_shades))
            scaled_color = [channel * scale_factor for channel in base_color] + [alpha]
        
            element.color = scaled_color
            print(scaled_color)
        
        color_ramp_node.color_ramp.elements.remove(color_ramp_node.color_ramp.elements[num_shades])

        return mat

    def create_outline(self, scene):
        thickness = scene.thickness
        bpy.ops.object.grease_pencil_add(type='LINEART_SCENE')
        lineart = bpy.context.active_object
        lineart.modifiers["Lineart"].use_intersection = False
        lineart.modifiers["Lineart"].thickness = thickness

        return lineart
        
def menu_func(self, context):
    self.layout.operator(MATERIAL_OT_cartoon_shader.bl_idname)

class MATERIAL_PT_cartoon_shader_panel(bpy.types.Panel):
    """Panel for Creating a Cartoon Shader"""
    bl_label = "Cartoon Shader Creator"
    bl_idname = "MATERIAL_PT_cartoon_shader_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Cartoon Shader'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Create UI controls for parameters
        layout.prop(scene, "main_color")
        layout.prop(scene, "num_shades")
        layout.prop(scene, "thickness")

        layout.operator("material.create_cartoon_shader", text="Generate Cartoon Shader")


# Function to initialize properties in the scene
def init_properties():
    bpy.types.Scene.main_color = bpy.props.FloatVectorProperty(
        name="Main Color",
        subtype='COLOR',
        default=(1.0, 0.5, 0.0, 1.0),
        size=4,
        min=0.0,
        max=1.0
    )
    bpy.types.Scene.num_shades = bpy.props.IntProperty(
        name="Number of Shades",
        default=2,
        min=1,
        max=10
    )
    bpy.types.Scene.thickness = bpy.props.IntProperty(
        name="Outline Thickness",
        default=25,
        min=1,
        max=100
    )

# Cleanup function for removing properties
def clear_properties():
    del bpy.types.Scene.main_color
    del bpy.types.Scene.num_shades
    del bpy.types.Scene.thickness


def register():
    bpy.utils.register_class(MATERIAL_PT_cartoon_shader_panel)
    bpy.utils.register_class(MATERIAL_OT_cartoon_shader)
    init_properties()

def unregister():
    clear_properties()
    bpy.utils.unregister_class(MATERIAL_PT_cartoon_shader_panel)
    bpy.utils.unregister_class(MATERIAL_OT_cartoon_shader)

if __name__ == "__main__":
    register()
