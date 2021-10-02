from __future__ import annotations
from typing import Callable, Dict, Optional
from itertools import product

from grids import *

# List alias for BFS and DFS since this object could be used
# as a queue or a stack but will always pop off a GridNode
NodeSet = List[GridNode]

# Alias for the return type of every search method
Solution = Tuple[
    Optional[GridPath],  # Path through the grid
    int                  # The total number of nodes traversed in this path
]

# Alias for the type each search method is, a callable that takes the
# parameters specified in the write-up -- start node, goal node, and the grid --
# and returns a solution
SearchMethod = Callable[
    [
        Position,         # The start position to search from
        Position,         # The goal position to search for
        Grid              # The grid to search in
    ],
    Solution
]


# Methods in this class can be called as the static methods they are or
# an instance of PathPlanning may be instantiated and they can be called on that object
class PathPlanning:
    # For determining the method based on its name through the CLI.\
    # Must be filled in after the class is initialized
    methods: Dict[
        str,          # The name of the search method (DFS, BFS, ASTAR, ALL)
        SearchMethod  # The search method itself
    ]

    @staticmethod
    def ordered_search(mode: str) -> SearchMethod:
        """A function factory for creating either a BFS or DFS function.
        It is done this way because BFS and DFS are nearly identical so various components -- such as which element is
        popped and how backtracking is performed -- can be plugged in
        @param mode: the type of ordered search -- dfs or bfs
        @return: a search method
        """

        # Type annotations for the queue-like or stack-like container
        # as well as the popping method
        nodeset: NodeSet = []
        pop: Callable[[], GridNode]

        # For DFS, we pop off the back of nodeset and
        # iterating through the node's path up to the ancestor that
        # has a child on the stack.
        # In other words, we kill the path up the point that we find
        # an ancestor node that is on a path we have yet to rule out
        if mode == 'dfs':
            pop = nodeset.pop

            def backtrack(node: GridNode):
                # Find the common ancestor between this node's ancestors and
                # the nodes in the queue that have yet to be visited
                try:
                    parent = next(
                        ancestor.parent

                        for ancestor, unvisited in product(
                            node.path(),
                            nodeset
                        ) if ancestor.parent == unvisited.parent
                    )
                # If we do not find such a parent, we make sure
                # parent is None so the while-loop works
                except StopIteration:
                    parent = None

                # Go up the path to this common ancestor (or stop
                # until node has no parent) and unmark these nodes
                # as visited and reset their parent field to None
                while node != parent:
                    node.visited = False
                    tmp = node.parent
                    node.parent = None
                    node = tmp
        # For BFS, we pop off the front of the queue-like container and
        # backtrack by simply unmarking the node as visited and resetting its parent field
        elif mode == 'bfs':
            def pop():
                return nodeset.pop(0)

            def backtrack(node: GridNode):
                node.visited = False
                node.parent = None
        # There is no reason this should happen but is good for debugging
        else:
            raise ValueError(f"unknown mode '{mode}'")

        def search(start: Position, goal: Position, grid: Grid) -> Solution:
            """The manufactured method for searching through the graph
            @param start: the position of the node we begin the search at
            @param goal: the position of the node we are searching for
            @param grid: the grid to search in
            @return: a solution of the form (path, num_traversed)
            """
            # In case we run multiple search methods over this grid
            grid.reset_visitation()

            # Translate from indices to the node objects themselves
            start, goal = (
                grid[row][col] for row, col in (start, goal)
            )
            # Initialize the queue or stack as well as the solution
            nodeset.append(start)
            start.visited = True
            result, traversed = None, 0

            while nodeset:
                node: GridNode = pop()
                traversed += 1

                # If we have made it to the goal node,
                # consider this solution compared to our best solution.
                if node == goal:
                    path = node.global_path()
                    if result is None or len(path) < len(result):
                        result = path
                    next_nodes = ()
                else:
                    # Visit each of the child nodes that are not
                    # marked as visited
                    next_nodes = node.adjacent_nodes()

                next_node = None
                for next_node in next_nodes:
                    # Add to the queue or stack and set their visitation and ancestry
                    nodeset.append(next_node)
                    next_node.parent = node
                    next_node.visited = True

                # If we found a solution or there are no more nodes to visit connected
                # to this node, then we have to kill this path to explore alternatives
                if next_node is None:
                    backtrack(node)

            return result, traversed

        return search

    @staticmethod
    def a_star(start: Position, goal: Position, grid: Grid) -> Solution:
        """Runs an A* search over the grid
        Each node is evaluated based on the length of its path and the distance from
        the goal node, using this Euclidean distance as a heuristic.
        """
        # In case we run multiple search methods over the grid
        grid.reset_visitation()

        # Translate from indices to the actual grid nodes
        start, goal = (
            grid[row][col] for row, col in (start, goal)
        )
        # Initialize the solution and queue
        queue: List[GridNode] = [start]
        traversed = 0

        while queue:
            node = queue.pop()
            node.visited = True
            traversed += 1

            if node == goal:
                return list(node.global_path()), traversed

            # Of all the nodes connected to this node,
            # consider the length of the path as well as their
            # Euclidean distance to the goal.
            best_g, best_h, best_node = None, None, None
            for next_node in node.adjacent_nodes():
                next_path = next_node.path()
                g, h = len(list(next_path)), next_node - goal
                if best_node is None or (g + h) < (best_g + best_h):
                    best_g, best_h, best_node = g, h, next_node

            if best_node is not None:
                queue.append(best_node)
                best_node.parent = node


# Add BFS and DFS as static methods
PathPlanning.depth_first_search = PathPlanning.ordered_search('dfs')
PathPlanning.breadth_first_search = PathPlanning.ordered_search('bfs')

# Initialize this dictionary so that the CLI can resolve the
# search methods by name, as well as simplify running them all
PathPlanning.methods = {
    key: method
    for key, method in [
        (key, getattr(PathPlanning, attr)) for key, attr in (
            ("DFS", "depth_first_search"),
            ("BFS", "breadth_first_search"),
            ("ASTAR", "a_star")
        )
    ] + [
        ("ALL", lambda start, goal, grid: tuple(
            method(start, goal, grid)

            for key, method in PathPlanning.methods.items() if key != "ALL"
        )),
    ]
}

__all__ = [
    "PathPlanning",
    "Solution",
    "SearchMethod"
]
