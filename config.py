import bpy
from mathutils import Vector
import numpy as np


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


UNIVERSAL_MAP = {
    'ShaderNodeRGB': ('outputs', 0),
    'ShaderNodeValue': ('outputs', 0),
    'ShaderNodeMapRange': ('inputs', 0),
    'ShaderNodeSeparateColor': ('inputs', 0),
}

ALBEDO_MAP = {
    'ShaderNodeBsdfPrincipled': ('inputs', 0),
    'ShaderNodeEmission': ('inputs', 0),
    'ShaderNodeBsdfToon': ('inputs', 0),
    'ShaderNodeBsdfAnisotropic': ('inputs', 0),
    'ShaderNodeBsdfDiffuse': ('inputs', 0),
    'ShaderNodeBsdfGlass': ('inputs', 0),
    'ShaderNodeBsdfGlossy': ('inputs', 0),
    'ShaderNodeBsdfHair': ('inputs', 0),
    # 'ShaderNodeHoldout', # this would need to get the world node's color
    'ShaderNodeBsdfHairPrincipled': ('inputs', 0),
    'ShaderNodeBsdfRefraction': ('inputs', 0),
    'ShaderNodeSubsurfaceScattering': ('inputs', 0),
    'ShaderNodeBsdfTranslucent': ('inputs', 0),
    'ShaderNodeBsdfVelvet': ('inputs', 0),
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

NODE_PATTERNS_TO_SKIP = {'Reroute',
                         'GroupInput',
                         'GroupOutput',
                         'NodeOutput',
                         'ShaderNodeShaderToRGB'}
