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
