import os
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def postprocess_evaluation(target_dir: str, eval_rewards: List[float], plot_points: int = 100):
    print("Postprocessing")

    def _isint(_s):
        try:
            int(_s)
            return True
        except ValueError:
            pass
        return False

    monitor_dir = os.path.join(target_dir, "monitor")
    monitors = [x for x in os.listdir(monitor_dir) if _isint(x.split(".")[0]) and x.endswith(".csv")]
    monitors = sorted(monitors, key=lambda x: int(x.split(".")[0]))

    fig_reward, ax_reward = plt.subplots(1, 2)
    ax_reward: np.ndarray[plt.Axes] = np.ravel([ax_reward])
    fig_reward.set_size_inches(20, 10)

    fig_evaluation, ax_evaluation = plt.subplots(1, 1)
    ax_evaluation: np.ndarray[plt.Axes] = np.ravel([ax_evaluation])
    fig_evaluation.set_size_inches(10, 10)

    for monitor in monitors:
        idx = int(monitor.split(".")[0])
        monitor = os.path.join(monitor_dir, monitor)
        data = pd.read_csv(monitor, sep=",", comment='#')
        pts = np.linspace(start=0, stop=len(data), num=plot_points, endpoint=True).astype(int)
        x = [pts[k] + (pts[k+1]-pts[k])//2 for k in range(plot_points - 1)]

        reward_data = [np.mean(data["r"][pts[k]:pts[k+1]]) for k in range(plot_points - 1)]

        ax_reward[0].plot(x, reward_data, label=f"{idx}")
        if idx == 0:
            ax_reward[1].plot(x, reward_data)

    ax_evaluation[0].plot(eval_rewards)

    ax_reward[0].legend()
    ax_reward[0].set_title("Different trainings")
    ax_reward[1].set_title("Training 0")
    fig_reward.suptitle("Rewards")

    ax_evaluation[0].set_title("Rewards")
    fig_evaluation.suptitle("Evaluations")

    plot_dir = os.path.join(target_dir, "eval", "plots")
    os.makedirs(plot_dir, exist_ok=False)
    fig_reward.savefig(os.path.join(plot_dir, "train_reward.png"), format="PNG")
    fig_evaluation.savefig(os.path.join(plot_dir, "evaluation.png"), format="PNG")
