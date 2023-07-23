from gymnasium.envs.registration import register

from .gym import TicTacToePlusGym

# check_env(TicTacToePlusGym, warn=True)

# Example for the CartPole environment
register(id="TicTacToePlus-v1", entry_point="TicTacToePlus.game.gym.gym:TicTacToePlusGym",)
