# Tic-Tac-Toe with Multiple Agents

This project involves designing a Tic-Tac-Toe game using multiple agents such as Q-Learning in reinforcement learning, the Min-Max algorithm from adversarial search, and Alpha-Beta pruning. The project includes two AI players: one using the Minimax algorithm with Alpha-Beta Pruning, and the other using Q-learning reinforcement learning.

## Project Files

The project consists of several Python files:

- **`final.py`**: Implements the main Tic-Tac-Toe game loop, allowing the Minimax AI player to play against the Q-learning AI player.
- **`q-learn-algorithm.py`**: Defines a Q-learning player for reinforcement learning. The Q-learning player can be trained and then play against other players.
- **`min-max-algorithm.py`**: Contains the Minimax algorithm with Alpha-Beta Pruning for game tree traversal.
- **`q-learn.py`**: Defines the Q-learning player class, including methods for making moves, updating Q-values, and printing learned Q-values.

## How to Play

1. Run `q-learn.py` to run the Q-learning class.
2. Run `minimax.py` to observe the computer player using the minimax algorithm.
3. Run `q-learn-algorithm.py` to play a game with Q-learning AI.
4. Finally, Run `final.py` to observe the game between Minimax AI and Q-learning AI.
5. The computer players use the Minimax algorithm with Alpha-Beta pruning and Q-learning strategies to make optimal moves.
6. The game result is displayed at the end.

## Q-Learning Player

- The Q-learning player in `q-learn-algorithm.py` is implemented using reinforcement learning.
- It can be trained against other players and then used to play the game.

## Project Objectives

The main objectives of this project are as follows:

1. Implement a functional Tic-Tac-Toe game.
2. Develop an AI player using the Minimax algorithm with Alpha-Beta Pruning.
3. Implement a Q-learning player for reinforcement learning.
4. Allow the Minimax AI player to play against the Q-learning AI player for comparison.
5. Train the Q-learning player and evaluate its performance.

Command to run the tic-tac-toe game using different algorithms

For Windows:

1. python q-learn.py

2. Using min-max algorithm
   
   python min-max-algorithm.py

4. Using q-learn algorithm
   
   python q-learn-algorithm.py

6. Using best agent
   
   python final.py

For Mac:
1. python3 q-learn.py

2. Using min-max algorithm
   
   python3 min-max-algorithm.py

4. Using Q-learn algorithm
   
   python3 q-learn-algorithm.py

6. To find the best agent
   
   python3 final.py
