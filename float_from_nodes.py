import bpy
import numpy as np

from . import util


def clamp_float(*args):
    clamp_node, node_key, default_val = args

    value_socket = clamp_node.inputs[0]
    min_socket = clamp_node.inputs[1]
    max_socket = clamp_node.inputs[2]

    value_socket_val = get_float_from_socket(value_socket, node_key, default_val)
    min_socket_val = get_float_from_socket(min_socket, node_key, 0.0)
    max_socket_val = get_float_from_socket(max_socket, node_key, 1.0)

    if clamp_node.clamp_type == 'RANGE':
        new_min_socket_val = min(min_socket_val, max_socket_val)
        new_max_socket_val = max(min_socket_val, max_socket_val)
        min_socket_val, max_socket_val = new_min_socket_val, new_max_socket_val

    return min(max(value_socket_val, min_socket_val), max_socket_val)


def get_float_from_image(*args) -> float:
    """Calculates the maximum value in the image, excluding the alpha channel and pixels below an alpha threshold.

    :param curr_node: Image-like node
    """
    curr_node = args[0]
    if not hasattr(curr_node, 'image') or curr_node.image is None:
        return 0.0

    pixels = np.array(curr_node.image.pixels).reshape(-1, 4)

    # slice the pixels into the RGB channels, filter out transparent pixels, get mean
    ch_a = pixels[:, 3]
    pixels = pixels[(ch_a >= 0.7)]
    pixels = np.delete(pixels, 3, axis=1)

    return max(pixels.mean(axis=0))


def get_float_from_socket(curr_socket, node_key: dict, default_val: float) -> float:
    """Get float from node socket - either evaluating the default value or following the link.

    :param curr_socket: node socket object.
    :param node_key: config key of node ids and which sockets to retrieve the float value.
    :param default_val: default float value if no nodes match.
    :return: float value from socket
    """
    if curr_socket.is_linked and not curr_socket.is_output:
        next_node = curr_socket.links[0].from_node

        if next_node.bl_idname == 'NodeGroupInput':
            socket_index = util.get_socket_index(curr_socket.links[0].from_socket)
            raise util.GroupInputException(input_socket_index=socket_index)

        # if a group node, use the right socket index
        if hasattr(next_node, 'node_tree'):
            output = next(util.find_outputs(next_node.node_tree), None)
            socket_index = util.get_socket_index(curr_socket.links[0].from_socket)

            try:
                return get_float_from_socket(output.inputs[socket_index], node_key, default_val)
            except util.GroupInputException as gie:
                input_node_socket_index = gie.input_socket_index
                return get_float_from_socket(next_node.inputs[input_node_socket_index], node_key, default_val)

        return find_float(curr_socket.links[0].from_node, node_key, default_val)
    else:
        val = curr_socket.default_value
        try:
            _iter_test = iter(val)
        except TypeError:
            pass
        else:
            val = max(val[:-1])  # exclude alpha channel

        return val


def find_float(curr_node: bpy.types.Node, node_key: dict, default_val: float) -> float:
    """Find first float value found within node tree.

    :param curr_node: current node in recursive traversal.
    :param node_key: config key of node ids and which sockets to retrieve the float value.
    :param default_val: default float value if no nodes match.
    """

    # enter group nodes
    if hasattr(curr_node, 'node_tree'):
        output = next(util.find_outputs(curr_node.node_tree), None)
        group_val = find_float(output, node_key, default_val)

        # if the default value, try the first group inputs
        if group_val == default_val:
            socket = curr_node.inputs[0]
            return get_float_from_socket(socket, node_key, default_val)

    result = next((p for p in node_key.keys() if p in curr_node.bl_idname), None)
    if result is not None:
        if callable(node_key[result]):
            return node_key[result](curr_node, node_key, default_val)
        else:
            direction, albedo_idx = node_key[result]
            curr_socket = getattr(curr_node, direction)[albedo_idx]

            return get_float_from_socket(curr_socket, node_key, default_val)

    if len(curr_node.inputs) == 1:
        curr_socket = curr_node.inputs[0]
        return get_float_from_socket(curr_socket, node_key, default_val)

    return 0.0
