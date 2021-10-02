from argparse import Action, ArgumentParser
from paths import *
from grids import *


# Load Grid from file when it's passed as an argument
def grid_file(value: str):
    with open(value, 'r') as fp:
        return Grid.load(fp)


# Return a tuple of indices when the node position is passed as an argument
def parse_position(value: str) -> Position:
    r, c = (int(s) for s in value.split(','))
    return r, c


# Return the function for the search method when it's passed as an argument
def parse_search_method(value: str) -> SearchMethod:
    try:
        return PathPlanning.methods[value]
    except KeyError:
        raise ValueError(f"Unknown search method '{value}'")


# We only need one instance so we might as well declare it here with
# the type functions defined above
ARG_PARSER = ArgumentParser()
ARG_PARSER.add_argument(
    "--input",
    dest="grid",
    type=grid_file,
    required=True,
    help="The .dat file containing the grid to search in"
)

ARG_PARSER.add_argument(
    f"--start",
    type=parse_position,
    required=True,
    help="The position R,C in the grid to begin the search at"
)

ARG_PARSER.add_argument(
    f"--goal",
    type=parse_position,
    required=True,
    help="The position R,C of the goal node in the grid."
)

ARG_PARSER.add_argument(
    "--search",
    type=parse_search_method,
    help="The search method to use, one of BFS, DFS, ASTAR, ALL"
)


__all__ = ['ARG_PARSER', 'Position']