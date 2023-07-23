from typing import Optional, List
import argparse
import os

from TicTacToePlus.entries.player import Player, Human, KI

_human_player_key = "human"


def play(player1: Optional[str], player2: Optional[str]):
    game_args = {"game_size": 3, "max_val": 3, "num_per_key": 3, "num_player": 2}
    player_list: List[Player] = [
        Human(idx=1, game_args=game_args) if player1 is None else KI(idx=1, game_args=game_args, model_path=player1),
        Human(idx=2, game_args=game_args) if player2 is None else KI(idx=2, game_args=game_args, model_path=player2),
    ]

    current_player_idx = 1
    current_player: Player = player_list[current_player_idx-1]
    while True:
        print(current_player.get_game())
        move = current_player.get_move()

        if move is None:
            print(f"Player {current_player_idx} could not play anymore. Remi")

        print(f"Player {current_player_idx} played {' '.join(f'{k} {v}' for k, v in move.items())}")
        for p in player_list:
            p.apply_move(move=move)

        wins = current_player.get_game().check_won()
        if any(x is not None for x in wins.values()):
            print(current_player.get_game())
            for player_idx, where in sorted(wins.items(), key=lambda x: x[0]):
                if where is not None:
                    print(f"Player {player_idx} won {where}")
            return

        current_player_idx = current_player_idx + 1
        if current_player_idx > len(player_list):
            current_player_idx = 1
        current_player = player_list[current_player_idx-1]


def _parse_player_type(data: str):
    if data == _human_player_key:
        return None
    if os.path.exists(data):
        if os.path.isfile(data) and data.endswith(".zip"):
            return data
        raise argparse.ArgumentTypeError(f"Model data has to be a valid trained model zip file")
    raise argparse.ArgumentTypeError(f"Could not read {data} as player type. "
                                     f"Options are {_human_player_key} or a valid path to a trained model zip")


def main():
    parser = argparse.ArgumentParser(description="Run training")
    parser.add_argument("-p1", "--player1", dest="player1", required=True, type=_parse_player_type,
                        help=f"Type of player 1. Options are '{_human_player_key}' or '/path/to/model.zip'")
    parser.add_argument("-p2", "--player2", dest="player2", required=True, type=_parse_player_type,
                        help=f"Type of player 2. Options are '{_human_player_key}' or '/path/to/model.zip'")
    args = parser.parse_args()

    play(player1=args.player1, player2=args.player2)


if __name__ == "__main__":
    main()
