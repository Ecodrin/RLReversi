from gymnasium.envs.registration import register

register(
    id='TicTacToe-v0',
    entry_point='environment.tictactoe_gym:TicTacToeEnv'
)
