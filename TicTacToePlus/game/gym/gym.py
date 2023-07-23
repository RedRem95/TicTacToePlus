import numpy as np
from typing import Dict, Any, Tuple, Optional, List
from random import choice

import gymnasium
from gymnasium import spaces

from TicTacToePlus.game.game import Game


class TicTacToePlusGym(gymnasium.Env):

    def __init__(self, game_args: Dict[str, Any], ki_player_idx: int):
        super(TicTacToePlusGym, self).__init__()

        self._game_args = game_args
        self._ki_player_idx = ki_player_idx
        self._game = Game(**self._game_args)
        if ki_player_idx > self._game.num_player:
            raise ValueError(f"KI plays as {ki_player_idx}, but game has only {self._game.num_player} player slots")

        print(f"KI is player {ki_player_idx}/{self._game.num_player}")
        self._actions = self._game.get_pos_moves()
        self.action_space = spaces.Box(low=0, high=1, shape=(len(self._actions),), dtype=float)
        self.observation_space = spaces.Box(low=0, high=255, shape=(self._game.game_size, self._game.game_size, 2), dtype=np.uint8)
        self.reset()

    @property
    def game(self) -> Game:
        return self._game

    def get_obs(self, game: Game = None) -> np.ndarray:
        if game is None:
            game = self.game
        ret = np.zeros(self.observation_space.shape, self.observation_space.dtype)
        for i in range(ret.shape[0]):
            for j in range(ret.shape[1]):
                player_id, key = game.get_at(row=i+1, col=j+1)
                if player_id is not None:
                    player_id -= (self._ki_player_idx - 1)
                    if player_id < 1:
                        player_id = game.num_player - player_id
                    ret[i, j] = [player_id, key]
        return ret

    def get_action_from_predict(
            self, avail_actions: List[Dict[str, int]], action: np.ndarray
    ) -> Tuple[Optional[Dict[str, int]], int]:
        best_action: Tuple[Optional[Dict[str, int]], int] = None, -1
        for i, act in enumerate(self._actions):
            if act in avail_actions:
                if action[i] > best_action[1]:
                    best_action = act, action[i]
        return best_action

    def step(self, action):
        info = {}

        if self._game.current_player_idx() != self._ki_player_idx:
            raise ValueError(f"KI should play but its not its move ({self._game.current_player_idx()} != {self._ki_player_idx})")
        avail_actions = self._game.get_pos_moves()

        if len(avail_actions) <= 0:
            info["KI-Winner"] = False
            info["Winner"] = -1
            info["Win-Cause"] = ("KI no moves left", -1)
            return self.get_obs(), 0, True, False, info

        best_action = self.get_action_from_predict(avail_actions=avail_actions, action=action)

        if best_action[0] is None:
            raise ValueError("KI had no legal move. What the fuck")

        res, cause = self._game.play(**best_action[0])
        if not res:
            raise ValueError(f"Could not play: {cause}")
        check_won = self._game.check_won()[self._ki_player_idx]
        if check_won is not None :
            info["KI-Winner"] = True
            info["Winner"] = self._ki_player_idx
            info["Win-Cause"] = check_won
            return self.get_obs(), 1, True, False, info

        rng_play = self._play_random(n=self._game.num_player - 1)
        if rng_play is not None:
            i, _info = rng_play
            info.update(_info)
            return self.get_obs(), -1 if i else 0, True, False, info

        return self.get_obs(), 0, False, False, info

    def _play_random(self, n: int):
        info = {}
        for i in range(n):
            avail_actions = self._game.get_pos_moves()
            if len(avail_actions) <= 0:
                info["KI-Winner"] = False
                info["Winner"] = -1
                info["Win-Cause"] = (f"Someone else no moves left", -1)
                return False, info
            rng_move = choice(avail_actions)
            res, cause = self._game.play(**rng_move)
            if not res:
                raise ValueError(f"Could not play: {cause}")
            check_won = self._game.check_won()[(self._ki_player_idx + i) % self._game.num_player + 1]
            if check_won is not None:
                info["KI-Winner"] = False
                info["Winner"] = (self._ki_player_idx + i) % self._game.num_player + 1
                info["Win-Cause"] = check_won
                return True, info
        return None

    def reset(self, **kwargs):
        self._game = Game(**self._game_args)
        rng_play = self._play_random(self._ki_player_idx - 1)
        if rng_play is not None:
            raise ValueError("Could not prepare game")
        return self.get_obs(), {}

    def render(self, mode='console'):
        if mode != "console":
            raise NotImplemented()
        print(str(self._game))

    def close(self):
        pass
