from collections import OrderedDict
from grids import *
from typing import Callable, Dict, Optional

Solution = Tuple[
    Optional[GridPath],  # Path through the grid
    int                  # The total number of nodes traversed in this path
]

SearchMethod = Callable[  # A search method function
    [
        GridNode,         # The start position to search from
        GridNode,         # The goal position to search for
        Grid              # The grid to search in
    ],
    Solution
]


# Method factory for ordered search to minimize redundant code
# DFS and BFS are identical except for the data structure they use
# for visitation order.
# In Python, both a stack and a queue can be emulated with a list
# so the only difference in their implementations is how elements
# are popped off.
# DFS pops off the back, making the list stack-like
# while BFS pops off the front, making the list queue-like.
def _ordered_search(mode: str) -> SearchMethod:
    # Determine if this is DFS or BFS order
    container = []
    try:
        # If it is DFS, use the container as a stack
        # If it is BFS, use the container as a queue
        pop, backtrack = {
            "dfs": (
                lambda: container.pop(-1),
                None
            ),
            "bfs": (
                lambda: container.pop(0),
                lambda node, path:
            )
        }[mode]
    except KeyError:
        raise ValueError(f"unknown search order: {mode}")

    # Factory-made method
    def search(start: GridNode, goal: GridNode, grid: Grid) -> Solution:
        # Whenever the first or shortest path is found, update best_path
        best_path: Optional[GridPath] = None
        traversed = 0

        # Reset visited fields to False for every node in the grid
        grid.reset_visitation()

        # Initialize container with start node
        container.append((
            start,
            [start]
        ))

        # Visitation
        while container:
            # Get the current node and its path
            node, path = pop()

            # Determine if we have found the goal node and can mark this as a solution.
            # If it is a solution, also determine if it is the shortest path yet
            best_path, nodes = (
                path, ()         # Update the best path but do not search for nodes
            ) if node == goal and (best_path is None or len(path) < len(best_path)) else (
                best_path, node  # Do not update the best path but search for nodes
            )

            # Look for possible nodes to visit.
            # For every node that is found, it should be marked as traversed
            # and added to the container
            next_node = None
            for next_node in nodes:
                next_node.visited = True
                traversed += 1

                container.append((
                    next_node,
                    path + [next_node]
                ))

            # If we found a solution or there were no nodes that
            # could be visited from here, unmark this as visited.
            # This is because if no nodes are added, the only place to
            # In the path is back up which will happen as none of this node's
            # children are in the container so other paths may need to visit
            # this node.
            if next_node is None:
                node.visited = False
                while node !=

        # Return whatever path was found and
        # the number of nodes traversed.
        return [(node.row, node.col) for node in best_path], traversed

    # Return the factory-made method.
    return search


class PathPlanning:
    methods: Dict[
        str,
        SearchMethod
    ]

    # Create two search methods that take a start, goal, and grid parameter:
    # - One for DFS, and
    # - another for BFS.
    # This must be done after the class is initialized.
    depth_first_search: SearchMethod
    breadth_first_search: SearchMethod

    @staticmethod
    def a_star_search(start: GridNode, goal: GridNode, grid: Grid) -> Solution:
        pass

    @classmethod
    def all(cls, start: GridNode, goal: GridNode, grid: Grid):
        return tuple(method(start, goal, grid) for method in (
            cls.breadth_first_search,
            cls.depth_first_search,
            cls.a_star_search
        ))


for _method in ("depth_first_search", "breadth_first_search"):
    _mode = ''.join(word[0] for word in _method.split('_'))
    setattr(
        PathPlanning,
        _method,
        _ordered_search(_mode)
    )


PathPlanning.methods = OrderedDict((
    ("BFS", PathPlanning.breadth_first_search),
    ("DFS", PathPlanning.depth_first_search),
    ("ASTAR", PathPlanning.a_star_search),
    ("ALL", PathPlanning.all)
))
