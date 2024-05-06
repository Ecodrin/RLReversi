import environment
import gymnasium


env = gymnasium.make('TicTacToe-v0', depth=5, size=5, pieces_to_win=4)
observation, info = env.reset()
while True:
    action = int(input('Action: '))
    observation, reward, done, _, info = env.step(action)
    print(f'Reward: {reward}')
    if done:
        break
