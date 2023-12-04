import numpy as np
import random

def createGame(game_name):
    # Factory function to create instances of different games
    if game_name == 'TicTacToe':
        return TicTacToegame()

class TicTacToegame():

    def __init__(self):
        # Initialize the TicTacToe game
        self.resetGame()

    # Render the current state of the TicTacToe board
    def createBoard(self):
        line = '\n-----------\n'
        row = " {} | {} | {}"
        print((row + line + row + line + row).format(*self.state))
        print(self.info)

    def checkStep(self, action):
        # Apply the move to the game state and check for the end of the game
        self.state[action] = self.cur_player
        self.action_space.remove(action)
        self.checkEndState()
        # Update game information based on the game state
        if self.is_end:
            if self.is_win:
                self.info = 'player{} win!'.format(self.cur_player)
            else:
                self.info = 'players draw'
        else:
            self.info = 'player{} turn'.format(self.cur_player)
        
        # Return the current game state and information
        return (self.state, self.is_win, self.is_end, self.info)
    
    
    # Reset the game to its initial state
    def resetGame(self, X=None, O=None):
        self.state = [' '] * 9
        self.action_space = list(range(9))
        self.is_end = False
        self.is_win = False
        self.info = 'new game'
        self.playerX = X
        self.playerO = O
        self.cur_player = random.choice(['O','X'])
        return (self.state, self.is_win, self.is_end, self.info)


    # Generator function to alternate player turns
    def playerTurn(self):
        while 1:
            if self.cur_player == 'O':
                cur = self.playerO
                oth = self.playerX
            else:
                cur = self.playerX
                oth = self.playerO
            
            self.info = 'player{} turn'.format(self.cur_player) 
            yield (cur, oth)

            # Switch to the other player for the next turn
            self.cur_player = 'OX'.replace(self.cur_player, '')

    # Check if the game has reached an end state (win or draw)
    def checkEndState(self):
        for a,b,c in [(0,1,2), (3,4,5), (6,7,8),
                      (0,3,6), (1,4,7), (2,5,8),
                      (0,4,8), (2,4,6)]:
            if self.cur_player == self.state[a] == self.state[b] == self.state[c]:
                self.is_win = True
                self.is_end = True
                return

        if not any([s == ' ' for s in self.state]):
            self.is_win = False
            self.is_end = True
            return

class RandomPlayer():
    def __init__(self):
        self.name = 'Random'
        self.win_n = 0

    # Randomly select a move from the available actions
    def action(self, state, actions):
        return random.choice(actions)

    # Update player's statistics based on the game outcome
    def reward(self, reward, state):
        if reward == 1:
            self.win_n += 1

    #  No specific action at the end of each episode for the random player
    def endEpisode(self, episode):
        pass

class QLearningPlayer():
    def __init__(self):
        self.name = 'Q-Learning'
        self.q = {}
        self.init_q = 1
        self.lr = 0.3
        self.gamma = 0.9
        self.epsilon = 1.0
        self.max_epsilon = 1.0
        self.min_epsilon = 0.01
        self.decay_rate = 0.01
        self.action_n = 9
        self.win_n = 0

        self.last_state = (' ',) * 9
        self.last_action = -1

    # Make a move based on Q-learning strategy
    def action(self, state, actions):
        state = tuple(state)
        self.last_state = state

        r = random.uniform(0, 1)
        if r > self.epsilon:
            if self.q.get(state):
                # Exploit known Q-values if available
                i = np.argmax([self.q[state][a] for a in actions])
                action = actions[i]
            else:
                # Initialize Q-values if not available
                self.q[state] = [self.init_q] * self.action_n
                action = random.choice(actions)
        else:
            # Explore with random action
            action = random.choice(actions)

        self.last_action = action
        return action

    # Update Q-values based on the received reward
    def reward(self, reward, state):
        if self.last_action >= 0:
            if reward == 1:
                self.win_n += 1

            # Initialize Q-values if not available
            state = tuple(state)
            if self.q.get(self.last_state):
                q = self.q[self.last_state][self.last_action]
            else:
                # Q-value update based on the Q-learning formula
                self.q[self.last_state] = [self.init_q] * self.action_n
                q = self.init_q

            self.q[self.last_state][self.last_action] = q + self.lr * (reward + self.gamma * np.max(self.q.get(state, [self.init_q]*self.action_n)) - q)

    def endEpisode(self, episode):
        # Decay epsilon for exploration-exploitation balance
        self.epsilon = self.min_epsilon + (self.max_epsilon - self.min_epsilon) * np.exp(-self.decay_rate*(episode+1))

    # Print the learned Q-values for debugging or analysis
    def print_q(self):
        for k,v in self.q.items():
            print(k,v)

class HumanPlayer():
    def __init__(self):
        self.name = 'Human'
        
    # Allow the human player to input their move
    def action(self, state, actions):
        a = int(input('your move:')) - 1
        return a


# Train the agents through a specified number of episodes
def train(trails_num, p1, p2, env):
    for episode in range(trails_num):
        
        state, win, done, info = env.resetGame(X=p1, O=p2)

        for (cur_player, oth_player) in env.playerTurn():
            #env.render()
            action = cur_player.action(state, env.action_space)
            state, win, done, info = env.checkStep(action)

            if done:
                if win:
                    cur_player.reward(1, state)
                    oth_player.reward(-1, state)
                else:
                    cur_player.reward(0.5, state)
                    oth_player.reward(0.5, state)
                break
            else:
                oth_player.reward(0, state)
        
        env.playerX.endEpisode(episode)
        env.playerO.endEpisode(episode)
    
    # Display training results
    print('='*20)
    print('Train result - %d episodes' % trails_num)
    print('{} win rate: {}'.format(play_1.name, play_1.win_n / trails_num))
    print('{} win rate: {}'.format(play_2.name, play_2.win_n / trails_num))
    print('players draw rate: {}'.format((trails_num - play_1.win_n - play_2.win_n) / trails_num))
    print('='*20)

# Play a single game between two trained agents
def playGame(play_1, play_2, env):
    while 1:
        state, win, done, info = env.resetGame(X=play_1, O=play_2)
        for (cp, op) in env.playerTurn():
            print()
            env.createBoard()
            action = cp.action(state, env.action_space)
            state, win, done, info = env.checkStep(action)
            if done:
                env.createBoard()
                break

if __name__ == '__main__':
    env = createGame('TicTacToe')
    play_1 = QLearningPlayer()
    play_2 = QLearningPlayer()
    play_3 = HumanPlayer()
    play_4 = RandomPlayer()
    train(10, play_1, play_4, env)
    playGame(play_1, play_3, env)
