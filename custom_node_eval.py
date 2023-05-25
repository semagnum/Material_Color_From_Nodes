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
    curr_node, _, default_val = args
    if not hasattr(curr_node, 'image') or curr_node.image is None:
        return Vector((1.0, 0.0, 1.0, 1.0))  # typical "cannot find the texture" color

    pixels = np.array(curr_node.image.pixels).reshape(-1, 4)

    # slice the pixels into the RGB channels, filter out transparent pixels, get mean
    ch_a = pixels[:, 3]
    pixels = pixels[(ch_a >= 0.7)]
    pixels = np.delete(pixels, 3, axis=1)

    color_mean = pixels.mean(axis=0)

    if not np.all(np.isfinite(color_mean)):
        return default_val

    return Vector(tuple(list(color_mean) + [1.0]))


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


def mix_node(*args) -> Vector:
    # We're just going to mix the two socket values based on factor.
    node, node_key, default_val = args

    data_type = node.data_type
    factor_value = node_eval.assert_float(node_eval.get_from_socket(node.inputs[0], node_key, default_val))

    if data_type == 'RGBA':
        a_socket = node.inputs[6]
        b_socket = node.inputs[7]
    elif data_type == 'VECTOR':
        a_socket = node.inputs[4]
        b_socket = node.inputs[5]
    else:
        a_socket = node.inputs[2]
        b_socket = node.inputs[3]

    a_factor = 1 - factor_value
    if data_type == 'FLOAT':
        a_val = node_eval.assert_float(node_eval.get_from_socket(node.inputs[2], node_key, default_val))
        b_val = node_eval.assert_float(node_eval.get_from_socket(node.inputs[3], node_key, default_val))
        val = (b_val * factor_value) + (a_val * a_factor)
    else:
        a_factor = 1 - factor_value
        a_val = [v * a_factor
                 for v in node_eval.assert_color(node_eval.get_from_socket(a_socket, node_key, default_val))]
        b_val = [v * factor_value
                 for v in node_eval.assert_color(node_eval.get_from_socket(b_socket, node_key, default_val))]
        val = Vector([a + b for a,b in zip(a_val, b_val)])

    return val
