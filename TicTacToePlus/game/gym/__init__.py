import gymnasium
from gym.envs.registration import register
from stable_baselines3.common.env_checker import check_env

from .gym import TicTacToePlusGym

# check_env(TicTacToePlusGym, warn=True)

# Example for the CartPole environment
register(id="TicTacToePlus-v1", entry_point="TicTacToePlus.game.gym.gym:TicTacToePlusGym",)
