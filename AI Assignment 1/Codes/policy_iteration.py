from pyamaze import maze, agent,COLOR,textLabel
from timeit import timeit

def get_actions(maze,x,y):
    actions=maze.maze_map[(x,y)]
    s=[]
    for dir, bool in actions.items():
        if bool==1:
            s.append(dir)
    return s

def policy_evaluation(policy, maze, V, gamma, theta):
    while True:
        delta = 0
        for s in maze.maze_map.keys():
            v = 0
            for a, a_prob in policy[s].items():
                nxt = get_next_state(maze, s, a)
                v += a_prob * (maze.rewards.get(nxt, 0) + gamma * V[nxt])
            delta = max(delta, abs(v - V[s]))
            V[s] = v
        if delta < theta:
            break

def policy_improvement(maze, V, gamma):
    policy = {}
    for s in maze.maze_map.keys():
        policy[s] = {}
        for a in get_actions(maze, *s):
            policy[s][a] = 1.0 / len(get_actions(maze, *s))

    while True:
        policy_evaluation(policy, maze, V, gamma, theta=0.001)
        policy_stable = True
        for s in maze.maze_map.keys():
            old_action = max(policy[s], key=policy[s].get)
            action_values = {}
            for a in get_actions(maze, *s):
                nxt = get_next_state(maze, s, a)
                action_values[a] = maze.rewards.get(nxt, 0) + gamma * V[nxt]
            best_action = max(action_values, key=action_values.get)
            if old_action != best_action:
                policy_stable = False
            for a in policy[s]:
                policy[s][a] = 1 if a == best_action else 0
        if policy_stable:
            break
    return policy

def get_next_state(maze, state, action):
    if action == 'N':
        nxt = (state[0]-1, state[1])
    elif action == 'S':
        nxt = (state[0]+1, state[1])
    elif action == 'W':
        nxt = (state[0], state[1]-1)
    elif action == 'E':
        nxt = (state[0], state[1]+1)
    else:
        nxt = state
    if nxt in maze.maze_map:
        return nxt
    else:
        return state

def policy_iteration(maze):
    # Hyperparameters
    gamma = 0.9

    # Define rewards for all states
    maze.rewards = {}
    for state in maze.maze_map:
        if state == (1, 1):
            maze.rewards[state] = 1000
        else:
            maze.rewards[state] = -1

    # Define initial value function
    V = {}
    for state in maze.maze_map:
        V[state] = 0

    # Policy iteration
    policy = policy_improvement(maze, V, gamma)

    # Get the greedy path
    policy_path = []
    state = (maze.rows, maze.cols)
    policy_path.append(state)
    while state != (1, 1):
        action = max(policy[state], key=policy[state].get)
        state = get_next_state(maze, state, action)
        policy_path.append(state)
    return policy_path

if __name__=="__main__":
    
    rows = int(input('Enter the number of rows: '))
    cols = int(input('Enter the number of columns: '))
    maze = maze(rows, cols)
    maze.CreateMaze(loopPercent=50, theme=COLOR.light)
    path = policy_iteration(maze)
    t1 = timeit(stmt='policy_iteration(maze)',number=1000,globals=globals())
    textLabel(maze, 'Policy Iteration Time', t1)
    agent_path = agent(maze, footprints=True)
    a = agent(maze, footprints=True, shape='square', color=COLOR.green)
    maze.tracePath({agent_path: path}, delay=100)
    maze.run()
