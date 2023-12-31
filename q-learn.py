
class QLearningPlayer():
    def __init__(self):
        # Initialize Q-Learning player with parameters
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

     # Choose an action based on the Q-values and exploration-exploitation strategy
    def action(self, state, actions):
        state = tuple(state)
        self.last_state = state

        r = random.uniform(0, 1)
        if r > self.epsilon:
            if self.q.get(state):
                # Exploit: Choose the action with the highest Q-value
                i = np.argmax([self.q[state][a] for a in actions])
                action = actions[i]
            else:
                # Initialize Q-values if not available
                self.q[state] = [self.init_q] * self.action_n
                action = random.choice(actions)
        else:
            # Explore: Choose a random action
            action = random.choice(actions)

        self.last_action = action
        return action

    # Update Q-values based on the received reward using the Q-learning update formula
    def reward(self, reward, state):
        if self.last_action >= 0:
            if reward == 1:
                self.win_n += 1

            state = tuple(state)
            if self.q.get(self.last_state):
                q = self.q[self.last_state][self.last_action]
            else:
                self.q[self.last_state] = [self.init_q] * self.action_n
                q = self.init_q

            self.q[self.last_state][self.last_action] = q + self.lr * (reward + self.gamma * np.max(self.q.get(state, [self.init_q]*self.action_n)) - q)

    # Decay epsilon for exploration-exploitation balance over episodes
    def episode_end(self, episode):
        # epsilon decay
        self.epsilon = self.min_epsilon + (self.max_epsilon - self.min_epsilon) * np.exp(-self.decay_rate*(episode+1))

    # Print the learned Q-values for debugging or analysis
    def print_q(self):
        for k,v in self.q.items():
            print(k,v)
