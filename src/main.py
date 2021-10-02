"""
Path Planning driver code for searching within a grid
@author: Clark Hathaway
"""
from cli import *
from grids import *


def main():
    args = ARG_PARSER.parse_args()

    result = args.search(args.start, args.goal, args.grid)
    # Print the results
    # If we called all of the methods, we should expect a tuple of solutions so print
    # those individually
    for path, traversed in result if len(result) == 3 else (result,):
        print('\n'.join((
            f"{field}: {s}" for field, s in (
                ("Path", str(path)),
                ("Traversed", str(traversed))
            )
        )))


if __name__ == '__main__':
    main()
