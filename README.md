# Path Planning
To use this software, run the following command inside src/ or any directory where
the PYTHON_PATH has been configured to find the modules therein:

`python3 main.py [-h] --input GRID --start START --goal GOAL [--search SEARCH]`

Any version of Python3.7+ should be sufficient. Python3.6 should also work but this
has not been verified. The only issue in that case would be the presence of type
annotations.

## PathPlanning class
The PathPlanning class has three search methods -- DFS, BFS, and A* --. These can be
called as static methods on the class. Additionally, PathPlanning may be instantiated and 
can be those functions may be called as methods on that object.