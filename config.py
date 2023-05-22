# Copyright (C) 2023 Spencer Magnusson
# semagnum@gmail.com
# Created by Spencer Magnusson
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

from . import color_from_nodes as color_node, float_from_nodes as float_node

ALPHA_THRESHOLD = 0.7

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
    'ShaderNodeClamp': float_node.clamp_float
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
    'ShaderNodeBsdfHairPrincipled': FIRST_INPUT,
    'ShaderNodeBsdfRefraction': FIRST_INPUT,
    'ShaderNodeSubsurfaceScattering': FIRST_INPUT,
    'ShaderNodeBsdfTranslucent': FIRST_INPUT,
    'ShaderNodeBsdfVelvet': FIRST_INPUT,
    'ShaderNodeTexImage': color_node.get_color_from_image,
    'ShaderNodeTexEnvironment': color_node.get_color_from_image,
}

METALLIC_MAP = {
    'ShaderNodeBsdfPrincipled': ('inputs', 6),
    'ShaderNodeTexImage': float_node.get_float_from_image,
    'ShaderNodeTexEnvironment': float_node.get_float_from_image,
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
    'ShaderNodeTexImage': float_node.get_float_from_image,
    'ShaderNodeTexEnvironment': float_node.get_float_from_image,
}

ALBEDO_MAP.update(UNIVERSAL_MAP)
METALLIC_MAP.update(UNIVERSAL_MAP)
ROUGHNESS_MAP.update(UNIVERSAL_MAP)
