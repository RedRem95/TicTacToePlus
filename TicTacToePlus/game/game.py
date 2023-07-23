from typing import List, Tuple, Dict, Optional

from .state import State
from .player import Player


class Game:

    def __init__(self, game_size: int = 3, max_val: int = 3, num_per_key: int = 3, num_player: int = 2):
        if num_player < 2:
            raise ValueError(f"You cant play with less than 2 players. {num_player} given")
        self._player: Dict[int, Player] = {k: Player(max_val=max_val, num_per_key=num_per_key) for k in range(1, num_player + 1, 1)}
        self._state = State(size=game_size)
        self._turn = 0
        self._num_player = num_player
        self._max_val = max_val
        self._game_size = game_size
        self._num_per_key = num_per_key

    @property
    def game_size(self):
        return self._game_size

    @property
    def num_player(self):
        return self._num_player

    def get_at(self, row, col) -> Tuple[Optional[int], int]:
        return self._state.get_at(row=row-1, col=col-1)

    def current_player_idx(self) -> int:
        return (self._turn % self._num_player) + 1

    def play(self, row, col, key) -> Tuple[bool, str]:
        win_check = self.check_won()
        if any(win_check.values()):
            return False, f"Player {' and '.join(str(k) for k, v in win_check.items() if v)} already won"
        current_player_idx = self.current_player_idx()
        if not self._player[current_player_idx].can_play(key=key):
            return False, f"Player {current_player_idx} cant play a {key}"
        if self._state.set(row=row-1, col=col-1, player_idx=current_player_idx, key=key):
            self._player[current_player_idx].played(key=key)
            self._turn += 1
            return True, ""
        else:
            return False, f"Player {current_player_idx} could not play at {row}x{col}. Is your key high enough?"

    def get_pos_moves(self) -> List[Dict[str, int]]:
        ret = []
        current_player_idx = self.current_player_idx()
        current_player = self._player[current_player_idx]
        for k in current_player.avail_keys():
            for i in range(self._game_size):
                for j in range(self._game_size):
                    if self._state.can_set(row=i, col=j, key=k):
                        ret.append({"row": i+1, "col": j+1, "key": k})
        return ret

    def get_best_move(self) -> Tuple[Dict[str, int], int, bool]:
        current_player_idx = self.current_player_idx()
        pos_games = []
        for move in self.get_pos_moves():
            n_game = self.__copy__()
            res, cause = n_game.play(**move)
            if not res:
                raise Exception(f"Error: {cause}")
            if n_game.check_won()[current_player_idx] is not None:
                return move, 1, True
            pos_games.append((move, n_game))
        for move, n_game in pos_games:
            n_game_best_move = n_game.get_best_move()
            pass
        return {}

    def check_won(self) -> Dict[int, Optional[Tuple[str, int]]]:
        return {k: self._state.player_won(player_idx=k) for k in self._player.keys()}

    def to_string(self) -> List[str]:
        current_player_idx = self.current_player_idx()
        player_strings = [
            f"Player {k}{' [A]' if k == current_player_idx else ''}" for k in sorted(self._player.keys())
        ]
        max_player_len = max(len(x) for x in player_strings)
        ret = [
            f"Turn {self._turn}",
            f" │ ".join(f"{ps:{max_player_len}}" for ps in player_strings)
        ]
        player_strings = [self._player[k].to_string() for k in sorted(self._player.keys())]
        for i in range(max(len(x) for x in player_strings)):
            ret.append(
                " │ ".join(f"{ps[i]:{max_player_len}}" if len(ps) > i else " " * max_player_len for ps in player_strings)
            )
        # ret.append("")
        ret.extend(self._state.to_string(max_val=self._max_val, player_count=self._num_player, add_idx=True))

        return ret

    def __str__(self):
        return "\n".join(self.to_string())

    def __copy__(self) -> "Game":
        ret = Game(
            game_size=self._game_size, num_per_key=self._num_per_key, num_player=self._num_player, max_val=self._max_val
        )
        ret._state = self._state.__copy__()
        ret._player = {k: v.__copy__() for k, v in self._player.items()}
        ret._turn = self._turn
        return ret
