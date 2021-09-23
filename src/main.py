from cli import *
from grids import *


def main():
    args = ARG_PARSER.parse_args()
    result = args.search(args.start, args.goal, args.grid)
    for path, traversed in result if len(result) == 3 else (result,):
        print('\n'.join((
            f"{field}: {s}" for field, s in (
                ("Path", str(path)),
                ("Traversed", str(traversed))
            )
        )))


if __name__ == '__main__':
    main()
