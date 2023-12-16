from pyamaze import maze, COLOR, agent
from queue import PriorityQueue

def heuristic(cell1,cell2):
  x1,y1=cell1
  x2,y2=cell2
  return abs(x1-x2)+abs(y1-y2)

def a_star(maze):
  start=(maze.rows,maze.cols)
  g_score={cell:float('inf') for cell in maze.grid}
  g_score[start]=0
  f_score={cell:float('inf') for cell in maze.grid}
  f_score[start]=heuristic(start,(1,1))
  search_space=[start]

  open=PriorityQueue()
  open.put((heuristic(start,(1,1)),heuristic(start,(1,1)),start))
  a_path={}
  while not open.empty():
    current_cell=open.get()[2]
    search_space.append(current_cell)
    if current_cell==(1,1):
      break
    for direction in 'ESNW':
      if maze.maze_map[current_cell][direction]==True:
        if direction=='E':
          child_cell=(current_cell[0],current_cell[1]+1)
        elif direction=='W':
          child_cell=(current_cell[0],current_cell[1]-1)
        elif direction=='N':
          child_cell=(current_cell[0]-1,current_cell[1])
        elif direction=='S':
          child_cell=(current_cell[0]+1,current_cell[1])
        temp_g_score=g_score[current_cell]
        temp_f_score=temp_g_score+heuristic(child_cell,(1,1))
        if temp_f_score<f_score[child_cell]:
          g_score[child_cell]=temp_g_score
          f_score[child_cell]=temp_f_score
          open.put((temp_f_score,heuristic(child_cell,(1,1)),child_cell))
          a_path[child_cell]=current_cell
  forward_path={}
  cell=(1,1)
  while cell!=start:
    forward_path[a_path[cell]]=cell
    cell=a_path[cell]
  return search_space,forward_path


if __name__ == '__main__':
  rows = int(input('Enter the number of rows: '))
  cols = int(input('Enter the number of columns: '))
  maze = maze(rows, cols)
  maze.CreateMaze(loopPercent=50, theme=COLOR.light)
  search_space, path = a_star(maze)
  agent_path = agent(maze, footprints=True)
  a = agent(maze, footprints=True, shape='square', color=COLOR.green)
  maze.tracePath({a: search_space}, showMarked=True, delay=50)
  maze.tracePath({agent_path: path}, delay=100)
  maze.run()
