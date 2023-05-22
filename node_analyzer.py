import bpy
from mathutils import Vector
from typing import Iterator

from . import config


def get_color_from_socket(socket, direction: str) -> Vector:
    """Get color from node socket - either evaluating the default value or following the link.

    :param socket: node socket object.
    :param direction: direction of the socket, 'inputs' or 'outputs'
    :return: color value of socket
    """
    if socket.is_linked and direction == 'inputs':
        return find_color(socket.links[0].from_node)
    else:
        try:
            _iter_test = iter(socket.default_value)
        except TypeError:
            val = Vector((socket.default_value, socket.default_value, socket.default_value, 1.0))
        else:
            val = socket.default_value[:]
        return val


def get_float_from_socket(curr_socket, direction: str, node_key: dict, default_val: float) -> float:
    """Get float from node socket - either evaluating the default value or following the link.

    :param curr_socket: node socket object.
    :param direction: direction of the socket, 'inputs' or 'outputs'
    :param node_key: config key of node ids and which sockets to retrieve the float value.
    :param default_val: default float value if no nodes match.
    :return: float value from socket
    """
    if curr_socket.is_linked and direction == 'inputs':
        return find_float(curr_socket.links[0].from_node, node_key, default_val)
    else:
        val = curr_socket.default_value
        try:
            _iter_test = iter(val)
        except TypeError:
            pass
        else:
            val = max(val[:-1]) # exclude alpha channel

        return val


def find_color(curr_node: bpy.types.Node) -> Vector:
    """Find first albedo color within node tree.

    :param curr_node: current node in recursive traversal.
    """
    # enter group nodes
    if hasattr(curr_node, 'node_tree'):
        output = next(find_outputs(curr_node.node_tree), None)
        group_color = find_color(output)

        # if the default value, try the first group inputs
        if group_color == Vector((0.8, 0.8, 0.8, 1.0)):
            socket = curr_node.inputs[0]
            return get_color_from_socket(socket, 'inputs')

    result = next((p for p in config.ALBEDO_MAP.keys() if p in curr_node.bl_idname), None)
    if result is not None:
        if callable(config.ALBEDO_MAP[result]):
            return config.ALBEDO_MAP[result](curr_node)
        else:
            direction, albedo_idx = config.ALBEDO_MAP[result]
            curr_socket = getattr(curr_node, direction)[albedo_idx]

            return get_color_from_socket(curr_socket, direction)

    if len(curr_node.inputs) == 1:
        socket = curr_node.inputs[0]
        return get_color_from_socket(socket, 'inputs')

    return Vector((0.8, 0.8, 0.8, 1.0))


def find_float(curr_node: bpy.types.Node, node_key: dict, default_val: float) -> float:
    """Find first float value found within node tree.

    :param curr_node: current node in recursive traversal.
    :param node_key: config key of node ids and which sockets to retrieve the float value.
    :param default_val: default float value if no nodes match.
    """

    # enter group nodes
    if hasattr(curr_node, 'node_tree'):
        output = next(find_outputs(curr_node.node_tree), None)
        group_val = find_float(output, node_key, default_val)

        # if the default value, try the first group inputs
        if group_val == default_val:
            socket = curr_node.inputs[0]
            return get_float_from_socket(socket, 'inputs', node_key, default_val)

    result = next((p for p in node_key.keys() if p in curr_node.bl_idname), None)
    if result is not None:
        if callable(node_key[result]):
            return node_key[result](curr_node)
        else:
            direction, albedo_idx = node_key[result]
            curr_socket = getattr(curr_node, direction)[albedo_idx]

            return get_float_from_socket(curr_socket, direction, node_key, default_val)

    if len(curr_node.inputs) == 1:
        curr_socket = curr_node.inputs[0]
        return get_float_from_socket(curr_socket, 'inputs', node_key, default_val)

    return 0.0


def find_outputs(node_tree: bpy.types.NodeTree) -> Iterator[bpy.types.Node]:
    """Returns all output nodes in a node tree."""
    return (node for node in node_tree.nodes if 'Output' in node.bl_idname)
