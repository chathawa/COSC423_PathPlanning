from argparse import Action, ArgumentParser
from paths import *
from pathlib import Path
from grids import *

GRID_NODE_ARGS = ("start", "goal")


def parse_position(value: str) -> Position:
    r, c = (int(s) for s in value.split(','))
    return r, c


def parse_search_method(value: str) -> SearchMethod:
    try:
        return PathPlanning.methods[value]
    except KeyError:
        raise ValueError(f"Unknown search method '{value}'")


class ReadGrid(Action):
    def __call__(self, parser, namespace, path: Path, *args, **kwargs):
        with open(path, 'r') as fp:
            setattr(namespace, self.dest, Grid.load(fp))

        for arg in GRID_NODE_ARGS:
            node = getattr(namespace, arg)
            if type(node) == tuple:
                ResolveNode(
                    dest=arg,
                    option_strings=[]
                ).__call__(parser, namespace, node, *args, **kwargs)


class ResolveNode(Action):
    def __call__(self, parser, namespace, position: Position, *args, **kwargs):
        r, c = position
        if not (0 <= r < len(namespace.grid)):
            raise ValueError(f"row (y) position {r} is out of bounds")
        if not (0 <= c < len(namespace.grid[0])):
            raise ValueError(f"column (x) position {c} is out of bounds")

        setattr(namespace, self.dest, namespace.grid[r][c] if isinstance(namespace.grid, Grid) else position)


ARG_PARSER = ArgumentParser()
ARG_PARSER.add_argument(
    "--input",
    dest="grid",
    type=Path,
    action=ReadGrid,
    required=True
)
for _arg in GRID_NODE_ARGS:
    ARG_PARSER.add_argument(
        f"--{_arg}",
        type=parse_position,
        action=ResolveNode,
        required=True
    )
ARG_PARSER.add_argument(
    "--search",
    type=parse_search_method
)


__all__ = ['ARG_PARSER', 'Position']