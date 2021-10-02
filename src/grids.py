from __future__ import annotations
from typing import Generator, List, Tuple, TextIO, Union, Iterable
from itertools import chain

Position = Tuple[int, int]


# Represents a linked node in the grid
class GridNode:
    def __init__(
            self,
            row: int,
            col: int
    ):
        self.row, self.col = row, col
        self.visited = False
        # References to the parent in the current path, and its neighbors which are fixed
        self.parent, self.left, self.up, self.right, self.down = (
            None for _ in range(5)
        )

    # Helper function for iterating through the ancestors
    def _ancestors(self, include_self=False) -> Generator[GridNode]:
        if include_self:
            yield self

        node = self.parent
        while node is not None:
            yield node
            node = node.parent

    # All the nodes going back up the path starting with this node
    def path(self) -> Iterable[GridNode]:
        return iter(self._ancestors(include_self=True))

    # All the nodes represented as their indices going back up the path
    def global_path(self) -> List[Position]:
        result = [
            (node.row, node.col) for node in self.path()
        ]
        result.reverse()
        return result

    # Helper function for iterating over unvisited neighbor nodes
    def _neighbors(self) -> Generator[GridNode]:
        return (
            node for node in (
                getattr(self, side) for side in (
                    "left",
                    "up",
                    "right",
                    "down"
                )
            ) if node and not node.visited
        )

    # All the neighboring nodes that have not been visited
    def adjacent_nodes(self) -> Iterable[GridNode]:
        return tuple(self._neighbors())

    # Take the Euclidean distance between this node and another
    def __sub__(self, other):
        if not isinstance(other, GridNode):
            raise ValueError(f"cannot subtract {type(other)} from GridNode", self, other)

        return ((self.row - other.row)**2 + (self.col - other.col)**2)**0.5

    # Comparison between node object and another object, possibly NoneType or Tuple
    # Useful for debugging and necessary when looking for nodes in a list
    def __eq__(self, other):
        if other is None:
            return False
        elif type(other) is tuple:
            row, col = other
            return self.row == row and self.col == col
        elif isinstance(other, GridNode):
            return self.row == other.row and self.col == other.col
        else:
            raise ValueError(f"cannot compare {type(other)} with GridNode", self, other)


# Alias for the return type of GridNode.global_path
GridPath = List[Position]


# Subtype of tuple, because this is a tuple of rows (tuples) of GridNode instances
class Grid(tuple):
    # Load the .dat file representation
    @classmethod
    def load(cls, fp: TextIO) -> Grid:
        result = Grid(
            tuple(
                GridNode(row, col) if s == '0' else None for col, s in enumerate(line.strip().split(','))
            )
            for row, line in enumerate(fp.readlines())
        )

        prev_row = None
        for r, row in enumerate(result):
            for c, node in enumerate(row):
                if not node:
                    continue

                if 0 < c and row[c - 1]:
                    left = row[c - 1]
                    node.left = left
                    left.right = node

                if prev_row and prev_row[c]:
                    up = prev_row[c]
                    node.up = up
                    up.down = node

            prev_row = row
        return result

    # Reset ancestry and visitation
    def reset_visitation(self):
        for row in self:
            for node in row:
                if node:
                    node.visited = False
                    node.parent = None
