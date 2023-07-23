import random
import os
from datetime import datetime
from typing import Callable, List

import gymnasium
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.monitor import Monitor
import torch

from TicTacToePlus.game import TicTacToePlusGym
from .postprocess import postprocess_evaluation


def train(target_folder: str, train_steps: int, n_envs: int = 1, evaluation_steps: int = 10):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder, exist_ok=False)
    if not os.path.isdir(target_folder):
        raise Exception(f"Target folder has to be a folder: {target_folder}")

    def _make_env(idx, monitor: bool = False) -> Callable[[], gymnasium.Env]:
        def _create():
            env = TicTacToePlusGym(
                game_args={"game_size": 3, "max_val": 3, "num_per_key": 3, "num_player": 2},
                ki_player_idx=random.randint(1, 2)
            )
            if monitor:
                env = Monitor(env, filename=os.path.join(target_folder, "monitor", f"{idx}"))
            return env
        return _create

    vec_env = DummyVecEnv([_make_env(idx=i, monitor=True) for i in range(n_envs)])

    print(f"Training on {n_envs} environments")
    model_path = os.path.join(target_folder, f"model")

    policy_kwargs = dict(activation_fn=torch.nn.ReLU, net_arch=dict(pi=[256, 256, 256, 256], vf=[256, 256, 256, 256]))

    model = PPO("MlpPolicy", vec_env, verbose=1, policy_kwargs=policy_kwargs)
    model.learn(total_timesteps=train_steps)

    print(f"Saving model to {model_path}")
    model.save(model_path)

    del vec_env
    del model

    print("Evaluating model")

    eval_env = _make_env(idx=-1, monitor=False)()
    eval_model = PPO.load(path=model_path, env=eval_env)

    rewards: List[float] = []

    for i in range(evaluation_steps):
        obs, info = eval_env.reset()

        done, truncated = False, False
        while not (done or truncated):
            action, _state = eval_model.predict(obs, deterministic=True)
            obs, reward, done, truncated, info = eval_env.step(action)
            rewards.append(float(reward))

    print(f"Evaluation: {np.mean(rewards)} [{np.min(rewards)}; {np.max(rewards)}]")

    postprocess_evaluation(target_dir=target_folder, eval_rewards=rewards)


