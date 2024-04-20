from gymnasium.envs.registration import register

register(
    id='TicTacToe-v0',
    entry_point='env.tictactoe_gym:TicTacToeEnv'
)
