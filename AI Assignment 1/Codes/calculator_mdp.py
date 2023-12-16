from value_iteration import value_iteration
from policy_iteration import policy_iteration

from pyamaze import maze
from timeit import timeit
import psutil

if __name__ == "__main__":
  memory_consumed_value=0
  time_comsumed_value=0
  length_of_path_value=0

  memory_consumed_policy=0
  time_comsumed_policy=0
  length_of_path_policy=0
  
  rows = int(input('Enter the number of rows: '))
  cols = int(input('Enter the number of columns: '))
  for i in range (10):
    maze_object = maze(rows, cols)
    maze_object.CreateMaze(loopPercent=50)
    
    value_path=value_iteration(maze_object)
    mem_value = psutil.Process().memory_info().rss / 1024 ** 2
    memory_consumed_value+=mem_value
    length_of_path_value+=len(value_path)+1
    
    policy_path=policy_iteration(maze_object)
    mem_policy = psutil.Process().memory_info().rss / 1024 ** 2
    memory_consumed_policy+=mem_policy
    length_of_path_policy+=len(policy_path)+1
    
    t1 = timeit(stmt='value_iteration(maze_object)', number=10, globals=globals())
    t2 = timeit(stmt='policy_iteration(maze_object)', number=10, globals=globals())
    time_comsumed_value+=t1
    time_comsumed_policy+=t2
    
  print()
  print("Value Iteration: ")
  print(f'Time Complexity: {time_comsumed_value/10}')
  print(f'Memory Complexity: {memory_consumed_value/10}')
  print(f'Length Of Path: {length_of_path_value/10}')
  print()
  print("Policy Iteration: ")
  print(f'Time Complexity: {time_comsumed_policy/10}')
  print(f'Memory Complexity: {memory_consumed_policy/10}')
  print(f'Length Of Path: {length_of_path_policy/10}')

# maze_object.run()