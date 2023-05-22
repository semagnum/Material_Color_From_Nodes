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
from typing import Iterator


class GroupInputException(Exception):
    """Exception to allow to get the socket index when recursion runs inside a group input node.
    Enables higher-up code to get the group input socket of the higher node tree.
    """

    def __init__(self, input_socket_index):
        super().__init__('Ran into group input node')
        self.input_socket_index = input_socket_index


def get_socket_index(socket):
    return int(socket.path_from_id().split('[')[-1][:-1])  # extracts index from str


def find_outputs(node_tree: bpy.types.NodeTree) -> Iterator[bpy.types.Node]:
    """Returns all output nodes in a node tree."""
    return (node for node in node_tree.nodes if 'Output' in node.bl_idname)
