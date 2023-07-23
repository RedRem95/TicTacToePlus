from typing import Optional, Tuple, List
from copy import deepcopy
from functools import lru_cache


@lru_cache
def _get_idx(row: int, col: int, size: int):
    return row * size + col


class State:
    def __init__(self, size: int = 3):
        self._state: List[Tuple[Optional[int], int]] = [(None, 0) for _ in range(size * size)]
        self._size = size

    def player_won(self, player_idx: int, include_not_set: bool = False) -> Optional[Tuple[str, int]]:
        for i in range(self._size):
            line, column = True, True
            for j in range(self._size):
                if not line and not column:
                    break
                if line:
                    idx = _get_idx(row=i, size=self._size, col=j)
                    if line and include_not_set and self._state[idx][0] is None:
                        line = True
                    elif self._state[idx][0] != player_idx:
                        line = False
                if column:
                    idx = _get_idx(row=j, size=self._size, col=i)
                    if column and include_not_set and self._state[idx][0] is None:
                        column = True
                    elif self._state[idx][0] != player_idx:
                        column = False
            if line:
                return "line", i+1
            if column:
                return "column", i+1

        diag1, diag2 = True, True
        for i in range(self._size):
            if not diag1 and not diag2:
                break
            if diag1:
                idx = _get_idx(row=i, size=self._size, col=i)
                if diag1 and include_not_set and self._state[idx][0] is None:
                    diag1 = True
                elif self._state[idx][0] != player_idx:
                    diag1 = False
            if diag2:
                idx = _get_idx(row=(i+1), size=self._size, col=- i - 1)
                if diag2 and include_not_set and self._state[idx][0] is None:
                    diag2 = True
                elif self._state[idx][0] != player_idx:
                    diag2 = False
        if diag1:
            return "diagonal [left to right]", 0
        if diag2:
            return "diagonal [right to left]", 0
        return None

    def get_at(self, row, col):
        return self._state[_get_idx(row=row, col=col, size=self._size)]

    def set(self, row: int, col: int, player_idx: int, key: int) -> bool:
        idx = _get_idx(row=row, size=self._size, col=col)
        can_do = self.can_set(row=row, col=col, key=key)
        if can_do:
            self._state[idx] = (player_idx, key)
        return can_do

    def can_set(self, row: int, col: int, key: int) -> bool:
        idx = _get_idx(row=row, size=self._size, col=col)
        if self._state[idx][0] is None or self._state[idx][1] < key:
            return True
        return False

    def to_string(self, max_val: int = None, player_count: int = 2, add_idx: bool = False) -> List[str]:
        template = "{player_idx:%sd}@{key_idx:%sd}" \
                   % (1 if max_val is None else len(str(max_val)), len(str(player_count)))
        template_len = len(template.format(player_idx=0, key_idx=0))

        def idx_to_string(_i: int, _j: int) -> str:
            player_idx, key_idx = self._state[_i * self._size + _j]
            if player_idx is None:
                return ' ' * template_len
            return template.format(player_idx=player_idx, key_idx=key_idx)

        ret = []
        spacer = ""
        if add_idx:
            spacer = ' ' * len(str(self._size))
            ret.append(f"{spacer} {' '.join(f'{k+1:^{template_len}}' for k in range(self._size))}")
        ret.append(f"{spacer}╔{'╤'.join('═'*template_len for _ in range(self._size))}╗")
        for i in range(self._size):
            if i > 0:
                ret.append(f"{spacer}╟{'┼'.join('─'*template_len for _ in range(self._size))}╢")
            ret.append(f"{f'{i+1:{len(spacer)}}' if add_idx else ''}║{'│'.join(idx_to_string(_i=i, _j=j) for j in range(self._size))}║")
        ret.append(f"{spacer}╚{'╧'.join('═'*template_len for _ in range(self._size))}╝")
        return ret

    def __copy__(self) -> "State":
        ret = State(size=self._size)
        ret._state = deepcopy(self._state)
        return ret
