import torch
import random
import numpy as np
from env import Env, COLOR
from collections import dequeue

MAX_MEMORY = 100_000
BATCH_SIZE = 1_000
learning_rate = 0.001

class Agent:
    def __init__():
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0
        self.memory = dequeue(maxlen=MAX_MEMORY)
        #add model and trainer
    def get_state(self, game):
        pass
    def remember(self, state, action, reward, next_state, done):
        pass
    def train_long_memory(self):
        pass
    def train_short_memory(self):
        pass
    def get_action(self.state):
        pass

    
def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = Env()
    while True:
        state_old = agent.get_state(game)
        final_move = agent.get_action(state_old)
        r, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)
        agent.train_short_memory(state_old, final_move, r)
        agent.remember()
        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                #agent.model.save()
            print('Game: ', agent.n_games, ' Score: ' score, ' Record: ', record) #TODO: plot


if __name__ == '__main__':
    train()