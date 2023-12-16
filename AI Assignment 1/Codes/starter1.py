from breadth_first_search import breadth_first_search
from depth_first_search import depth_first_search
from a_star import a_star

from pyamaze import maze, agent, textLabel, COLOR
from timeit import timeit
import psutil

rows = int(input('Enter the number of rows: '))
cols = int(input('Enter the number of columns: '))
maze = maze(rows, cols)
maze.CreateMaze(loopPercent=50, theme=COLOR.light)

search_space_bfs, bfs_path = breadth_first_search(maze)
mem_bfs = psutil.Process().memory_info().rss / 1024 ** 2
print(f"Maximum memory usage of BFS: {mem_bfs} MB")

search_space_dfs, dfs_path = depth_first_search(maze)
mem_dfs = psutil.Process().memory_info().rss / 1024 ** 2
print(f"Maximum memory usage of DFS: {mem_dfs} MB")

seach_space_astar, astar_path = a_star(maze)
mem_astar = psutil.Process().memory_info().rss / 1024 ** 2
print(f"Maximum memory usage of A*: {mem_astar} MB")

print('DFS Path Length', len(dfs_path)+1)
print('BFS Path Length', len(bfs_path)+1)
print('A-Star Path Length', len(astar_path)+1)

textLabel(maze, 'BFS Path Length', len(bfs_path)+1)
textLabel(maze, 'DFS Path Length', len(dfs_path)+1)
textLabel(maze, 'A-Star Path Length', len(astar_path)+1)
textLabel(maze, 'DFS Search Space', len(search_space_dfs)+1)
textLabel(maze, 'BFS Search Space', len(search_space_bfs)+1)
textLabel(maze, 'A-Star Search Space', len(seach_space_astar)+1)

bfs_path_plot = agent(maze, footprints=True, color=COLOR.yellow)
dfs_path_plot = agent(maze, footprints=True, color=COLOR.red)
astar_path_plot = agent(maze, footprints=True, color=COLOR.light)

t1 = timeit(stmt='depth_first_search(maze)', number=10, globals=globals())
t2 = timeit(stmt='breadth_first_search(maze)', number=10, globals=globals())
t3 = timeit(stmt='a_star(maze)', number=10, globals=globals())

textLabel(maze, 'DFS Time', t1)
textLabel(maze, 'BFS Time', t2)
textLabel(maze, 'A-Star Time', t3)

maze.tracePath({bfs_path_plot: bfs_path}, delay=100)
maze.tracePath({dfs_path_plot: dfs_path}, delay=100)
maze.tracePath({astar_path_plot: astar_path}, delay=100)

maze.run()