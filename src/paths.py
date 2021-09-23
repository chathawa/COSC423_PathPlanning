from collections import OrderedDict
from grids import *
from typing import Callable, Dict, List

Solution = Tuple[
    List[Position],  # List of positions forming a path
    int              # The total number of nodes traversed in this path
]

SearchMethod = Callable[  # A search method function
    [
        GridNode,         # The start position to search from
        GridNode,         # The goal position to search for
        Grid              # The grid to search in
    ],
    Solution
]


class PathPlanning:
    methods: Dict[
        str,
        SearchMethod
    ]

    @staticmethod
    def depth_first_search(start: GridNode, goal: GridNode, grid: Grid) -> Solution:
        traversed, stack = 0, [[start]]
        dist, result = None, []

        grid.reset_visitation()
        while stack:
            path = stack.pop()
            node = path[-1]

            node.visited = True
            traversed += 1

            if node == goal and (dist is None or len(path) < dist):
                dist, result = len(path), path

            stack.extend((path + [n] for n in node))
        return [(node.row, node.col) for node in result], traversed

    @staticmethod
    def breadth_first_search(start: GridNode, goal: GridNode, grid: Grid) -> Solution:
        traversed, queue = 0, [(start, [start])]
        dist, result = None, []

        grid.reset_visitation()
        while queue:
            node, path = queue.pop(0)
            node.visited = True
            traversed += 1

            if node == goal and (dist is None or len(path) < dist):
                dist, result = len(path), path

            for n in node:
                queue.insert(0, (n, path + [n]))
        return [(node.row, node.col) for node in result], traversed

    @staticmethod
    def a_star_search(start: GridNode, goal: GridNode, grid: Grid) -> Solution:
        traversed, queue = 1, [(start, [start])]
        result = None

        grid.reset_visitation()
        while queue:
            node, path = queue.pop(0)

            if node == goal and (result is None or len(path) < len(result)):
                result = path

            node.visited = True
            traversed += 1

            min_cost, next_nodes = None, []
            for n in node:
                cost = goal - n
                if min_cost is None or cost < min_cost:
                    min_cost, next_nodes = cost, [n]
                elif cost == min_cost:
                    next_nodes.append(n)

            if min_cost is None:
                node.visited = False
                continue

            for n in next_nodes:
                queue.insert(0, (n, path + [n]))

        return [(node.row, node.col) for node in result], traversed

    @classmethod
    def all(cls, start: GridNode, goal: GridNode, grid: Grid):
        return tuple(method(start, goal, grid) for method in (
            cls.breadth_first_search,
            cls.depth_first_search,
            cls.a_star_search
        ))


PathPlanning.methods = OrderedDict((
    ("BFS", PathPlanning.breadth_first_search),
    ("DFS", PathPlanning.depth_first_search),
    ("ASTAR", PathPlanning.a_star_search),
    ("ALL", PathPlanning.all)
))
