import bpy
from mathutils import Vector
import numpy as np

from . import util


def get_color_from_image(*args) -> Vector:
    """Calculates the mean RGB in the image, excluding pixels below an alpha threshold.

    :param curr_node: Image-like node
    """
    curr_node = args[0]
    if not hasattr(curr_node, 'image') or curr_node.image is None:
        return Vector((1.0, 0.0, 1.0, 1.0))  # typical "cannot find the texture" color

    pixels = np.array(curr_node.image.pixels).reshape(-1, 4)

    # slice the pixels into the RGB channels, filter out transparent pixels, get mean
    ch_a = pixels[:, 3]
    pixels = pixels[(ch_a >= 0.7)]
    pixels = np.delete(pixels, 3, axis=1)

    return Vector(tuple(list(pixels.mean(axis=0)) + [1.0]))


def get_color_from_socket(socket, albedo_map: dict) -> Vector:
    """Get color from node socket - either evaluating the default value or following the link.

    :param socket: node socket object.
    :return: color value of socket
    """
    if socket.is_linked and not socket.is_output:
        next_node = socket.links[0].from_node

        if next_node.bl_idname == 'NodeGroupInput':
            socket_index = util.get_socket_index(socket.links[0].from_socket)
            raise util.GroupInputException(input_socket_index=socket_index)

        # if a group node, use the right socket index
        if hasattr(next_node, 'node_tree'):
            output = next(util.find_outputs(next_node.node_tree), None)
            socket_index = util.get_socket_index(socket.links[0].from_socket)

            try:
                return get_color_from_socket(output.inputs[socket_index], albedo_map)
            except util.GroupInputException as gie:
                input_node_socket_index = gie.input_socket_index
                return get_color_from_socket(next_node.inputs[input_node_socket_index], albedo_map)

        return find_color(socket.links[0].from_node, albedo_map)
    else:
        try:
            _iter_test = iter(socket.default_value)
        except TypeError:
            val = Vector((socket.default_value, socket.default_value, socket.default_value, 1.0))
        else:
            val = socket.default_value[:]
        return val


def find_color(curr_node: bpy.types.Node, albedo_map: dict) -> Vector:
    """Find first albedo color within node tree.

    :param curr_node: current node in recursive traversal.
    :param albedo_map: config key of node ids and which sockets to retrieve color.
    """
    # enter group nodes
    if hasattr(curr_node, 'node_tree'):
        output = next(util.find_outputs(curr_node.node_tree), None)
        group_color = find_color(output, albedo_map)

        # if the default value, try the first group inputs
        if group_color == Vector((0.8, 0.8, 0.8, 1.0)):
            socket = curr_node.inputs[0]
            return get_color_from_socket(socket, albedo_map)

    result = next((p for p in albedo_map.keys() if p in curr_node.bl_idname), None)
    if result is not None:
        if callable(albedo_map[result]):
            return albedo_map[result](curr_node, albedo_map)
        else:
            direction, albedo_idx = albedo_map[result]
            curr_socket = getattr(curr_node, direction)[albedo_idx]

            return get_color_from_socket(curr_socket, albedo_map)

    if len(curr_node.inputs) == 1:
        socket = curr_node.inputs[0]
        return get_color_from_socket(socket, albedo_map)

    return Vector((0.8, 0.8, 0.8, 1.0))
