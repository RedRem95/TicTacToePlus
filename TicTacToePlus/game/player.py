from typing import List, Dict
from copy import deepcopy


class Player:
    def __init__(self, max_val: int = 3, num_per_key: int = 3):
        if max_val < 1:
            raise ValueError("Cant set a max value for the players of under 3")
        if num_per_key < 0:
            raise ValueError("You need at least 1 key to play")
        self._keys: Dict[int, int] = {k: num_per_key for k in range(1, max_val + 1, 1)}
        self._max_val = max_val
        self._num_per_key = num_per_key

    def avail_keys(self) -> List[int]:
        return [k for k, v in self._keys.items() if v > 0]

    def can_play(self, key: int = None) -> bool:
        if key is None:
            return len(self.avail_keys()) > 0
        else:
            return self._keys.get(key, 0) > 0

    def to_string(self) -> List[str]:
        max_key_len = max(len(str(x)) for x in self._keys.keys())
        return [
            f"{k:{max_key_len}}: {v}/{self._num_per_key}" for k, v in sorted(self._keys.items(), key=lambda x: x[0])
        ]

    def __copy__(self) -> "Player":
        ret = Player(max_val=self._max_val, num_per_key=self._num_per_key)
        ret._keys = deepcopy(self._keys)
        return ret

    def played(self, key: int):
        if self.can_play(key=key):
            self._keys[key] = self._keys[key] - 1
        else:
            raise Exception(f"Player cant play {key}")
