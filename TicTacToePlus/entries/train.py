import argparse
import os

from TicTacToePlus.rl.train import train as run_training


def run(target_folder: str, train_steps: int, n_envs: int = 1):
    run_training(target_folder=target_folder, train_steps=train_steps, n_envs=n_envs)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run training")
    parser.add_argument("-t", "--target-folder", dest="target_folder", required=True,
                        help="Folder to create training results in (Will always create a subfolder to collect data)")
    parser.add_argument("-s", "--train-steps", dest="train_steps", required=True, type=int,
                        help="Amount of training steps to perform")
    parser.add_argument("--num-envs", dest="n_envs", required=False, type=int, default=os.cpu_count(),
                        help=f"Amount of parallel environments to use for training (Default: {os.cpu_count()})")
    args = parser.parse_args()

    run(target_folder=args.target_folder, train_steps=args.train_steps, n_envs=args.n_envs)
