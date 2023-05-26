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

import bpy
from mathutils import Vector

from . import util


def assert_float(val) -> float:
    try:
        _iter_test = iter(val)
    except TypeError:
        return val
    else:  # is a color, exclude alpha channel
        return max(val[:-1])


def assert_color(val) -> Vector:
    try:
        _iter_test = iter(val)
    except TypeError:
        return Vector((val, val, val, 1.0))
    else:
        return val


def get_from_socket(curr_socket, node_key: dict, default_val):
    """Get value from node socket - either evaluating the default value or following the link.

    :param curr_socket: node socket object.
    :param node_key: config key of node ids and which sockets to retrieve the float value.
    :param default_val: default float value if no nodes match.
    :return: value from socket
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
                return get_from_socket(output.inputs[socket_index], node_key, default_val)
            except util.GroupInputException as gie:
                input_node_socket_index = gie.input_socket_index
                return get_from_socket(next_node.inputs[input_node_socket_index], node_key, default_val)

        return get_from_node(curr_socket.links[0].from_node, node_key, default_val)
    elif hasattr(curr_socket, 'default_value'):
        return curr_socket.default_value

    return default_val


def get_from_node(curr_node: bpy.types.Node, node_key: dict, default_val) -> float:
    """Find first float value found within node tree.

    :param curr_node: current node in recursive traversal.
    :param node_key: config key of node ids and which sockets to retrieve the float value.
    :param default_val: default float value if no nodes match.
    """

    # enter group nodes
    if hasattr(curr_node, 'node_tree'):
        output = next(util.find_outputs(curr_node.node_tree), None)
        group_val = get_from_node(output, node_key, default_val)

        # if the default value, try the first group inputs
        if group_val == default_val:
            socket = curr_node.inputs[0]
            return get_from_socket(socket, node_key, default_val)

    result = next((p for p in node_key.keys() if p == curr_node.bl_idname), None)
    if result is not None:
        if callable(node_key[result]):
            return node_key[result](curr_node, node_key, default_val)
        else:
            direction, albedo_idx = node_key[result]
            curr_socket = getattr(curr_node, direction)[albedo_idx]

            return get_from_socket(curr_socket, node_key, default_val)

    if len(curr_node.inputs) == 1:
        curr_socket = curr_node.inputs[0]
        return get_from_socket(curr_socket, node_key, default_val)

    return default_val
