from numpy import zeros

import gymnasium

import environment

from src.tictactoe import TicTacToeManager
from src.agent import TicTacToeAgent
from environment.tictactoe_gym.tictactoe_gym import display


# env = gymnasium.make('TicTacToe-v0')
# agent = TicTacToeAgent(env)
# agent.learn(10_000)
#
# agent.save('agent2_100k')

agent = TicTacToeAgent.load('agent10_1.5m_d3')
ttt = TicTacToeManager()
display(ttt.board.board, 3)
cmd = input('> ')

while cmd:
    args = cmd.split()
    match args[0]:
        case 'mv':
            ttt.make_move(int(args[1]))
            display(ttt.board.board, 3)
            if ttt.check_win():
                break
        case 'eval':
            print(agent.predict(ttt.board.get_uid(), ttt.find_legal_moves()))

    cmd = input('> ')
