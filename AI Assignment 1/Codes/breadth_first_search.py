from pyamaze import maze, COLOR, agent

def breadth_first_search(maze):
    start = (maze.rows, maze.cols)
    next_cell = [start]
    explored = [start]
    bfs_path = {}
    search_space = []
    while len(next_cell) > 0:
        current_cell = next_cell.pop(0)

        if current_cell == (1, 1):
            break
        for direction in 'ESNW':
            if maze.maze_map[current_cell][direction] == True:
                if direction == 'E':
                    child_cell = (current_cell[0], current_cell[1]+1)
                elif direction == 'W':
                    child_cell = (current_cell[0], current_cell[1]-1)
                elif direction == 'N':
                    child_cell = (current_cell[0]-1, current_cell[1])
                elif direction == 'S':
                    child_cell = (current_cell[0]+1, current_cell[1])
                if child_cell in explored:
                    continue
                next_cell.append(child_cell)
                explored.append(child_cell)
                bfs_path[child_cell] = current_cell
                search_space.append(child_cell)
    forward_path = {}
    cell = (1, 1)
    while cell != start:
        forward_path[bfs_path[cell]] = cell
        cell = bfs_path[cell]
    return search_space, forward_path


if __name__ == '__main__':
    rows = int(input('Enter the number of rows: '))
    cols = int(input('Enter the number of columns: '))
    maze = maze(rows, cols)
    maze.CreateMaze(loopPercent=50, theme=COLOR.light)
    search_space, path = breadth_first_search(maze)
    print(path)
    agent_path = agent(maze, footprints=True)
    a = agent(maze, footprints=True, shape='square', color=COLOR.green)
    maze.tracePath({a: search_space}, showMarked=True, delay=50)
    maze.tracePath({agent_path: path}, delay=100)
    maze.run()