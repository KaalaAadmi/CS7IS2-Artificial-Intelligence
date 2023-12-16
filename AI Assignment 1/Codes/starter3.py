
from breadth_first_search import breadth_first_search
from depth_first_search import depth_first_search
from a_star import a_star
from value_iteration import value_iteration
from policy_iteration import policy_iteration

from pyamaze import maze, agent, textLabel, COLOR
from timeit import timeit
import psutil
import tracemalloc
# from memory_profiler import memory_usage,profile

rows = int(input('Enter the number of rows: '))
cols = int(input('Enter the number of columns: '))
maze = maze(rows, cols)
maze.CreateMaze(loopPercent=50, theme=COLOR.light)


# OPTION 2:
search_space_bfs, bfs_path = breadth_first_search(maze)
mem_bfs = psutil.Process().memory_info().rss / 1024 ** 2
print(f"Maximum memory usage of BFS: {mem_bfs} MB")

search_space_dfs, dfs_path = depth_first_search(maze)
mem_dfs = psutil.Process().memory_info().rss / 1024 ** 2
print(f"Maximum memory usage of DFS: {mem_dfs} MB")

seach_space_astar, astar_path = a_star(maze)
mem_astar = psutil.Process().memory_info().rss / 1024 ** 2
print(f"Maximum memory usage of A*: {mem_astar} MB")

value_path=value_iteration(maze)
mem_value = psutil.Process().memory_info().rss / 1024 ** 2
print(f"Maximum memory usage of Value Iteration: {mem_value} MB")

policy_path=policy_iteration(maze)
mem_policy = psutil.Process().memory_info().rss / 1024 ** 2
print(f"Maximum memory usage of Policy Iteration: {mem_policy} MB")

print('BFS Path Length', len(bfs_path)+1)
print('DFS Path Length', len(dfs_path)+1)
print('A-Star Path Length', len(astar_path)+1)
print('Value Iteration Path Length', len(value_path)+1)
print('Policy Iteration Path Length', len(policy_path)+1)
# textLabel(maze, 'DFS Search Space', len(search_space_dfs)+1)
# textLabel(maze, 'BFS Search Space', len(search_space_bfs)+1)
# textLabel(maze, 'A-Star Search Space', len(seach_space_astar)+1)

bfs_path_plot = agent(maze, footprints=True, color=COLOR.yellow)
dfs_path_plot = agent(maze, footprints=True, color=COLOR.red)
astar_path_plot = agent(maze, footprints=True, color=COLOR.light)
value_path_plot = agent(maze, footprints=True, color=COLOR.blue)
policy_path_plot = agent(maze, footprints=True, color=COLOR.green)

t1 = timeit(stmt='depth_first_search(maze)', number=10, globals=globals())
t2 = timeit(stmt='breadth_first_search(maze)', number=10, globals=globals())
t3 = timeit(stmt='a_star(maze)', number=10, globals=globals())
t4 = timeit(stmt='value_iteration(maze)',number=10,globals=globals())
t5 = timeit(stmt='policy_iteration(maze)',number=10,globals=globals())

textLabel(maze, 'BFS Time', t2)
textLabel(maze, 'DFS Time', t1)
textLabel(maze, 'A-Star Time', t3)
textLabel(maze, 'Value Iteration Time', t4)
textLabel(maze, 'Policy Iteration Time', t5)

maze.tracePath({bfs_path_plot: bfs_path}, delay=100)
maze.tracePath({dfs_path_plot: dfs_path}, delay=100)
maze.tracePath({astar_path_plot: astar_path}, delay=100)
maze.tracePath({value_path_plot: value_path}, delay=100)
maze.tracePath({policy_path_plot: policy_path}, delay=100)

maze.run()
