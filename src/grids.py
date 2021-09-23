from __future__ import annotations
from typing import Tuple, TextIO, Callable, Optional

Position = Tuple[int, int]


class GridNode:

    def __init__(
            self,
            row: int,
            col: int
    ):
        self.row = row
        self.col = col
        self.visited = False
        self.left = None
        self.up = None
        self.right = None
        self.down = None

    def __iter__(self):
        return iter(
            node for node in (
                getattr(self, side) for side in ("left", "up", "right", "down")
            ) if node and not node.visited
        )

    def __sub__(self, other):
        if not isinstance(other, GridNode):
            raise ValueError(f"cannot subtract {type(other)} from GridNode", self, other)

        return ((self.row - other.row)**2 + (self.col - other.col)**2)**0.5

    def __eq__(self, other):
        if not isinstance(other, GridNode):
            raise ValueError(f"cannot compare {type(other)} with GridNode", self, other)

        return self.row == other.row and self.col == other.col


class Grid(tuple):
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

    def reset_visitation(self):
        for row in self:
            for node in row:
                if node:
                    node.visited = False
