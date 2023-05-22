import bpy
from mathutils import Vector
import numpy as np


class GroupInputException(Exception):
    """Exception to allow to get the socket index when recursion runs inside a group input node.
    Enables higher-up code to get the group input socket of the higher node tree.
    """
    def __init__(self, input_socket_index):
        super().__init__('Ran into group input node')
        self.input_socket_index = input_socket_index


def get_color_from_image(curr_node: bpy.types.Node) -> Vector:
    if not hasattr(curr_node, 'image') or curr_node.image is None:
        return Vector((1.0, 0.0, 1.0, 1.0))  # typical "cannot find the texture" color

    pixels = np.array(curr_node.image.pixels).reshape(-1, 4)

    # slice the pixels into the RGB channels, filter out transparent pixels, get mean
    ch_a = pixels[:, 3]
    pixels = pixels[(ch_a >= 0.7)]
    pixels = np.delete(pixels, 3, axis=1)

    return Vector(tuple(list(pixels.mean(axis=0)) + [1.0]))


def get_float_from_image(curr_node: bpy.types.Node) -> float:
    if not hasattr(curr_node, 'image') or curr_node.image is None:
        return 0.0

    pixels = np.array(curr_node.image.pixels).reshape(-1, 4)

    # slice the pixels into the RGB channels, filter out transparent pixels, get mean
    ch_a = pixels[:, 3]
    pixels = pixels[(ch_a >= 0.7)]
    pixels = np.delete(pixels, 3, axis=1)

    return np.max(pixels)


FIRST_INPUT = ('inputs', 0)

UNIVERSAL_MAP = {
    'ShaderNodeRGB': ('outputs', 0),
    'ShaderNodeValue': ('outputs', 0),
    'ShaderNodeMapRange': FIRST_INPUT,
    'ShaderNodeSeparateColor': FIRST_INPUT,
    'NodeGroupOutput': FIRST_INPUT,
    'ShaderNodeOutputMaterial': FIRST_INPUT,
    'ShaderNodeBrightContrast': FIRST_INPUT,
    'ShaderNodeGamma': FIRST_INPUT,
    'ShaderNodeHueSaturation': ('inputs', 4),
    'ShaderNodeInvert': ('inputs', 1),
    'ShaderNodeRGBCurve': ('inputs', 1),
}

ALBEDO_MAP = {
    'ShaderNodeBsdfPrincipled': FIRST_INPUT,
    'ShaderNodeEmission': FIRST_INPUT,
    'ShaderNodeBsdfToon': FIRST_INPUT,
    'ShaderNodeBsdfAnisotropic': FIRST_INPUT,
    'ShaderNodeBsdfDiffuse': FIRST_INPUT,
    'ShaderNodeBsdfGlass': FIRST_INPUT,
    'ShaderNodeBsdfGlossy': FIRST_INPUT,
    'ShaderNodeBsdfHair': FIRST_INPUT,
    # 'ShaderNodeHoldout', # this would need to get the world node's color
    'ShaderNodeBsdfHairPrincipled': FIRST_INPUT,
    'ShaderNodeBsdfRefraction': FIRST_INPUT,
    'ShaderNodeSubsurfaceScattering': FIRST_INPUT,
    'ShaderNodeBsdfTranslucent': FIRST_INPUT,
    'ShaderNodeBsdfVelvet': FIRST_INPUT,
    # 'ShaderNodeVertexColor', # need to analyze mesh attributes, get average color
    'ShaderNodeTexImage': get_color_from_image,
    'ShaderNodeTexEnvironment': get_color_from_image,
    # 'ShaderNodeBlackbody' # convert blackbody values to color
}

METALLIC_MAP = {
    'ShaderNodeBsdfPrincipled': ('inputs', 6),
    # 'ShaderNodeVertexColor', # need to analyze mesh attributes, get average color
    'ShaderNodeTexImage': get_float_from_image,
    'ShaderNodeTexEnvironment': get_float_from_image,
    # 'ShaderNodeBlackbody' # convert blackbody values to color
}

ROUGHNESS_MAP = {
    'ShaderNodeBsdfPrincipled': ('inputs', 9),
    'ShaderNodeBsdfToon': ('inputs', 1),
    'ShaderNodeBsdfAnisotropic': ('inputs', 1),
    'ShaderNodeBsdfDiffuse': ('inputs', 1),
    'ShaderNodeBsdfGlass': ('inputs', 1),
    'ShaderNodeBsdfGlossy': ('inputs', 1),
    'ShaderNodeBsdfHairPrincipled': ('inputs', 5),
    'ShaderNodeBsdfRefraction': ('inputs', 1),
    'ShaderNodeBsdfVelvet': ('inputs', 1),
    # 'ShaderNodeVertexColor', # need to analyze mesh attributes, get average color
    'ShaderNodeTexImage': get_float_from_image,
    'ShaderNodeTexEnvironment': get_float_from_image,
}

ALBEDO_MAP.update(UNIVERSAL_MAP)
METALLIC_MAP.update(UNIVERSAL_MAP)
ROUGHNESS_MAP.update(UNIVERSAL_MAP)
