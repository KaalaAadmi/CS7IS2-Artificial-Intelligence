from breadth_first_search import breadth_first_search
from depth_first_search import depth_first_search
from a_star import a_star

from pyamaze import maze
from timeit import timeit
import psutil

if __name__ == "__main__":
  memory_consumed_bfs=0
  time_comsumed_bfs=0
  length_of_path_bfs=0
  nodes_expanded_bfs=0
  memory_consumed_dfs=0
  time_comsumed_dfs=0
  length_of_path_dfs=0
  nodes_expanded_dfs=0
  memory_consumed_astar=0
  time_comsumed_astar=0
  length_of_path_astar=0
  nodes_expanded_astar=0
  rows = int(input('Enter the number of rows: '))
  cols = int(input('Enter the number of columns: '))
  for i in range (10):
    maze_object = maze(rows, cols)
    maze_object.CreateMaze(loopPercent=50)
    
    search_space_bfs, bfs_path = breadth_first_search(maze_object)
    mem_bfs = psutil.Process().memory_info().rss / 1024 ** 2
    memory_consumed_bfs+=mem_bfs
    length_of_path_bfs+=len(bfs_path)+1
    nodes_expanded_bfs+=((len(search_space_bfs)+1)/(rows*cols))

    search_space_dfs, dfs_path = depth_first_search(maze_object)
    mem_dfs = psutil.Process().memory_info().rss / 1024 ** 2
    memory_consumed_dfs+=mem_dfs
    length_of_path_dfs+=len(dfs_path)+1
    nodes_expanded_dfs+=((len(search_space_dfs)+1)/(rows*cols))
    
    seach_space_astar, astar_path = a_star(maze_object)
    mem_astar = psutil.Process().memory_info().rss / 1024 ** 2
    memory_consumed_astar+=mem_astar
    length_of_path_astar+=len(astar_path)+1
    nodes_expanded_astar+=((len(seach_space_astar)+1)/(rows*cols))

    t1 = timeit(stmt='depth_first_search(maze_object)', number=10, globals=globals())
    t2 = timeit(stmt='breadth_first_search(maze_object)', number=10, globals=globals())
    t3 = timeit(stmt='a_star(maze_object)', number=10, globals=globals())
    time_comsumed_bfs+=t2
    time_comsumed_dfs+=t1
    time_comsumed_astar+=t3

  print("BFS: ")
  print(f'Time Complexity: {time_comsumed_bfs/10}')
  print(f'Memory Complexity: {memory_consumed_bfs/10}')
  print(f'Nodes Expanded: {(nodes_expanded_bfs/10)*100}')
  print(f'Length Of Path: {length_of_path_bfs/10}')

  print("DFS: ")
  print(f'Time Complexity: {time_comsumed_dfs/10}')
  print(f'Memory Complexity: {memory_consumed_dfs/10}')
  print(f'Nodes Expanded: {(nodes_expanded_dfs/10)*100}')
  print(f'Length Of Path: {length_of_path_dfs/10}')

  print("A-Star: ")
  print(f'Time Complexity: {time_comsumed_astar/10}')
  print(f'Memory Complexity: {memory_consumed_astar/10}')
  print(f'Nodes Expanded: {(nodes_expanded_astar/10)*100}')
  print(f'Length Of Path: {length_of_path_astar/10}')

# maze_object.run()