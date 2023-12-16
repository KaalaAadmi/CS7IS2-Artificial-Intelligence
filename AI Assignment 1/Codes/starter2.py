from value_iteration import value_iteration
from policy_iteration import policy_iteration

from pyamaze import maze, agent, textLabel, COLOR
from timeit import timeit
import psutil

rows = int(input('Enter the number of rows: '))
cols = int(input('Enter the number of columns: '))
maze = maze(rows, cols)
maze.CreateMaze(loopPercent=50, theme=COLOR.light)


value_path=value_iteration(maze)
mem_value = psutil.Process().memory_info().rss / 1024 ** 2
print(f"Maximum memory usage of Value Iteration: {mem_value} MB")

policy_path=policy_iteration(maze)
mem_policy = psutil.Process().memory_info().rss / 1024 ** 2
print(f"Maximum memory usage of Policy Iteration: {mem_policy} MB")

value_path_plot = agent(maze, footprints=True, color=COLOR.blue)
policy_path_plot = agent(maze, footprints=True, color=COLOR.green)
t4 = timeit(stmt='value_iteration(maze)',number=10,globals=globals())
t5 = timeit(stmt='policy_iteration(maze)',number=10,globals=globals())


textLabel(maze,'Value Iteration Path Length', len(value_path)+1)
textLabel(maze,'Policy Iteration Path Length', len(policy_path)+1)
textLabel(maze, 'Value Iteration Time', t4)
textLabel(maze, 'Policy Iteration Time', t5)

maze.tracePath({value_path_plot: value_path}, delay=100)
maze.tracePath({policy_path_plot: policy_path}, delay=100)

maze.run()