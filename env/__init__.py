from gymnasium.envs.registration import register

register(
    id='TTT-V0',
    entry_point='env.TicTacToe_gymnasium:tictactoe_env.py'
)
