from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

from TicTacToePlus.game import Game, TicTacToePlusGym


class Player(ABC):

    def __init__(self, idx: int, game_args: Dict[str, Any]):
        self._idx = idx
        self._game = Game(**game_args)

    @abstractmethod
    def get_move(self) -> Optional[Dict[str, int]]:
        raise NotImplementedError()

    def get_idx(self) -> int:
        return self._idx

    def get_game(self) -> Game:
        return self._game

    def apply_move(self, move: Dict[str, int]):
        res, cause = self.get_game().play(**move)
        if not res:
            print(f"Could not play: {cause}")
            exit(1)


class Human(Player):

    def __init__(self, idx: int, game_args: Dict[str, Any]):
        super().__init__(idx=idx, game_args=game_args)

    def get_move(self) -> Optional[Dict[str, int]]:
        if self.get_game().current_player_idx() != self.get_idx():
            return None
        avail_moves = self.get_game().get_pos_moves()
        while True:
            inp = None
            try:
                inp = input("Please input your move (Format '<row>;<col>;<key>'): ")
                inp_split = inp.split(";")
                move = {
                    "row": int(inp_split[0]),
                    "col": int(inp_split[1]),
                    "key": int(inp_split[2]),
                }
                if move in avail_moves:
                    return move
                print(f"Your move is not possible. Your move {' '.join(f'{k}: {v}' for k, v in move.items())}")
            except (IndexError, ValueError):
                print(f"Could not understand {inp}. Please try again")


class KI(Player):

    def __init__(self, model_path: str, idx: int, game_args: Dict[str, Any]):
        super().__init__(idx, game_args)
        from stable_baselines3 import PPO
        self._env = TicTacToePlusGym(ki_player_idx=idx, game_args=game_args)
        self._model = PPO.load(path=model_path, env=self._env)
        self._env.reset()

    def get_move(self) -> Optional[Dict[str, int]]:
        if self.get_game().current_player_idx() != self.get_idx():
            return None
        action, _ = self._model.predict(observation=self._env.get_obs(game=self.get_game()), deterministic=True)
        best_action, _ = self._env.get_action_from_predict(avail_actions=self.get_game().get_pos_moves(), action=action)
        return best_action
