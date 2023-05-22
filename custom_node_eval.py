from . import node_eval

from mathutils import Vector
import numpy as np


def color_ramp(*args):
    """Calculates the mean RGB in the image, excluding pixels below an alpha threshold.

    :param curr_node: Image-like node
    """

    node, node_key, default_val = args
    factor_val = node_eval.assert_float(node_eval.get_from_socket(node.inputs[0], node_key, 0.5))
    return node_eval.assert_color(node.color_ramp.evaluate(factor_val))


def image_node(*args) -> Vector:
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


def clamp_node(*args):
    node, node_key, default_val = args

    value_socket = node.inputs[0]
    min_socket = node.inputs[1]
    max_socket = node.inputs[2]

    value_socket_val = node_eval.assert_float(node_eval.get_from_socket(value_socket, node_key, default_val))
    min_socket_val = node_eval.assert_float(node_eval.get_from_socket(min_socket, node_key, 0.0))
    max_socket_val = node_eval.assert_float(node_eval.get_from_socket(max_socket, node_key, 1.0))

    if node.clamp_type == 'RANGE':
        new_min_socket_val = min(min_socket_val, max_socket_val)
        new_max_socket_val = max(min_socket_val, max_socket_val)
        min_socket_val, max_socket_val = new_min_socket_val, new_max_socket_val

    return min(max(value_socket_val, min_socket_val), max_socket_val)
