import random
from q import Q
from connect4 import Connect4
from tqdm import tqdm


class Agent:
    def __init__(self):
        self.epsilon = 1.0
        self.q_learner = Q()

    def get_actions(self, s, valid_actions):
        if random.random() < self.epsilon:
            return random.choice(valid_actions)
        best = self.q_learner.get_best_action(s)
        if best is None:
            return random.choice(valid_actions)
        return best

    def learn_one_game(self, start):
        game = Connect4()
        if start != 1:
            game.play(random.choice(game.get_valid_actions()))
        while True:
            s = game.get_state()
            act = self.get_actions(s, game.get_valid_actions())
            win = game.play(act)
            if win or game.is_ended():
                self.q_learner.update(s, act, game.get_state(), 100)
                break
            win = game.play(random.choice(game.get_valid_actions()))
            if win or game.is_ended():
                self.q_learner.update(s, act, game.get_state(), -100)
                break
            self.q_learner.update(s, act, game.get_state(), 0)

    def learn(self, start, n=100000):
        print('learning...')
        for i in tqdm(range(n)):
            self.learn_one_game(start)
            self.epsilon -= 0.0001
        print('done')
