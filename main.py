import os
from time import perf_counter
from datetime import timedelta, datetime

from TicTacToePlus import Game
from TicTacToePlus.game import TicTacToePlusGym
from TicTacToePlus.rl.train import train


def play():
    game = Game(game_size=3, max_val=3, num_player=2, num_per_key=3)
    print(game)
    t1 = perf_counter()
    # print(game.get_best_move())
    t2 = perf_counter()
    print(timedelta(seconds=t2-t1))
    exit()
    move(game=game, row=1, col=1, key=3)
    print(game.get_best_move())
    move(game=game, row=1, col=2, key=3)
    print(game.get_best_move())
    move(game=game, row=2, col=1, key=3)
    print(game.get_best_move())
    move(game=game, row=2, col=3, key=3)
    print(game.get_best_move())
    move(game=game, row=1, col=3, key=3)
    print(game.get_best_move())


def move(game, row, col, key):
    player = game.current_player_idx()
    play_suc, play_suc_cause = game.play(row=row, col=col, key=key)
    if not play_suc:
        print(f"Could not play: {play_suc_cause}")
    print(game)
    win_check = game.check_won()[player]
    if win_check is not None:
        print(f"Player {player} won on {win_check[0]} {win_check[1]}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # play()
    train(
        f"C:\\Users\\alexa\\PycharmProjects\\TicTacToe+\\_results\\train_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        train_steps=50_000_000,
        n_envs=os.cpu_count() if True else 1
    )
