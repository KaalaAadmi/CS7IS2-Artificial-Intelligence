import numpy as np
from pyamaze import maze, agent, COLOR

def get_actions(maze,x,y):
    actions=maze.maze_map[(x,y)]
    s=[]
    for direction, bool in actions.items():
        if bool==1:
            s.append(direction)
    return s

def value_iteration(maze):
    #Hyperparameters
    threshold = 0.005 # Threshold. if change is less than this value then break.
    decay = 0.9    # decay

    #Define all states
    cell_list=list(maze.maze_map.keys())

    #Define rewards for all states
    rewards = {}
    for i in cell_list:
        if i == (1,1):
            rewards[i] = 1000
        else:
            rewards[i] = -1

    #Dictionnary of possible actions. We have two "end" states (1,2 and 2,2)
    actions = {}

    for i in range(1,maze.rows+1):
        for j in range(1,maze.cols+1):
            currCell = (i,j)
            actions[currCell] = ()
            for direction in 'ESNW':
                if maze.maze_map[currCell][direction]==True:
                    actions[currCell]=get_actions(maze,i,j)

    #Define an initial policy
    # From any cell, which is the best next cell to go to 
    policy={}
    for action in actions.keys():
        policy[action] = np.random.choice(actions[action])

    #Define initial value function 
    value={}
    for cell in cell_list:
        if cell in actions.keys():
            value[cell] = -1
        if cell ==(1,1):
            value[cell]= 10000

    iteration = 0

    while True:
        delta = 0
        for cell in cell_list:
            
            old_v = value[cell]
            new_value = 0
            
            for action in actions[cell]:
                if action == 'N':
                    nxt = [cell[0]-1, cell[1]]
                if action == 'S':
                    nxt = [cell[0]+1, cell[1]]
                if action == 'W':
                    nxt = [cell[0], cell[1]-1]
                if action == 'E':
                    nxt = [cell[0], cell[1]+1]

                #Calculate the value
                v = rewards[cell] + (decay * value[tuple(nxt)])
                if v > new_value: #Is this the best action so far? If so, keep it
                    new_value = v
                    policy[cell] = action

            #Save the best of all actions for the state                                
            value[cell] = new_value
            delta = max(delta, np.abs(old_v - value[cell]))

                
        #See if the loop should stop now         
        if delta < threshold:
            break
        iteration += 1


# Get the greedy path
    value_path = []
    current_cell = (maze.rows,maze.cols)
    value_path.append(current_cell)
    while True:
        dir = policy[current_cell]
        if dir == 'N':
            current_cell = (current_cell[0]-1, current_cell[1])
        if dir == 'E':
            current_cell = (current_cell[0], current_cell[1]+1)
        if dir == 'S':
            current_cell = (current_cell[0]+1, current_cell[1])
        if dir == 'W':
            current_cell = (current_cell[0], current_cell[1]-1)
        
        value_path.append(current_cell)

        if current_cell == (1,1):
            break
    return value_path

if __name__ == '__main__':
    rows = int(input('Enter the number of rows: '))
    cols = int(input('Enter the number of columns: '))
    maze = maze(rows, cols)
    maze.CreateMaze(loopPercent=50, theme=COLOR.light)
    path = value_iteration(maze)
    print(path)
    agent_path = agent(maze, footprints=True)
    a = agent(maze, footprints=True, shape='square', color=COLOR.green)
    # maze.tracePath({a: search_space}, showMarked=True, delay=50)
    maze.tracePath({agent_path: path}, delay=100)
    maze.run()
