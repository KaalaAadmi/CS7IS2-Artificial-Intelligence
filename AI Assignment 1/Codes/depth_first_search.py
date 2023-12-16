from pyamaze import maze, COLOR, agent

def depth_first_search(maze):
    start = (maze.rows, maze.cols)
    explored = [start]
    next_cell = [start]
    dfs_path = {}
    search_space = []
    while len(next_cell) > 0:
        current_cell = next_cell.pop()
        if current_cell == (1, 1):
            break
        for direction in 'ESNW':
            if maze.maze_map[current_cell][direction] == True:
                if direction == 'E':
                    child_cell = (current_cell[0], current_cell[1]+1)
                elif direction == 'W':
                    child_cell = (current_cell[0], current_cell[1]-1)
                elif direction == 'S':
                    child_cell = (current_cell[0]+1, current_cell[1])
                elif direction == 'N':
                    child_cell = (current_cell[0]-1, current_cell[1])
                if child_cell in explored:
                    continue
                explored.append(child_cell)
                next_cell.append(child_cell)
                dfs_path[child_cell] = current_cell
                search_space.append(current_cell)

    forward_path = {}
    cell = (1, 1)
    while cell != start:
        forward_path[dfs_path[cell]] = cell
        cell = dfs_path[cell]
    return search_space, forward_path


if __name__ == '__main__':
    rows = int(input('Enter the number of rows: '))
    cols = int(input('Enter the number of columns: '))
    maze = maze(rows, cols)
    maze.CreateMaze(loopPercent=50, theme=COLOR.light)
    search_space, path = depth_first_search(maze)
    agent_path = agent(maze, footprints=True)
    a = agent(maze, footprints=True, shape='square', color=COLOR.green)
    maze.tracePath({a: search_space}, showMarked=True, delay=50)
    maze.tracePath({agent_path: path}, delay=100)
    maze.run()
