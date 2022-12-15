from copy import copy
from enum import IntEnum


class Moves(IntEnum):
    NO_MOVE = 0
    UP = 1
    DOWN = 3
    LEFT = 5
    RIGHT = 9
    UP_LEFT = 6
    UP_RIGHT = 10
    DOWN_LEFT = 8
    DOWN_RIGHT = 12


moves_dict = {"R": Moves.RIGHT, "U": Moves.UP, "D": Moves.DOWN, "L": Moves.LEFT}


def get_tail_move(head: list, tail: list) -> Moves:
    move = 0
    if head[0] > tail[0]:
        move += Moves.UP
    if head[0] < tail[0]:
        move += Moves.DOWN
    if head[1] > tail[1]:
        move += Moves.RIGHT
    if head[1] < tail[1]:
        move += Moves.LEFT
    return Moves(move)


def _take_move(move: Moves, position: list, position2: list) -> None:
    tmp = copy(position)
    if move in [Moves.UP, Moves.UP_LEFT, Moves.UP_RIGHT]:
        tmp[0] += 1
    if move in [Moves.DOWN, Moves.DOWN_RIGHT, Moves.DOWN_LEFT]:
        tmp[0] -= 1
    if move in [Moves.LEFT, Moves.UP_LEFT, Moves.DOWN_LEFT]:
        tmp[1] -= 1
    if move in [Moves.RIGHT, Moves.UP_RIGHT, Moves.DOWN_RIGHT]:
        tmp[1] += 1
    if tmp != position2:
        position[0] = tmp[0]
        position[1] = tmp[1]


def take_move(move: Moves, head: list, tail: list) -> None:
    _take_move(move, head, [None, None])
    tail_move = get_tail_move(head, tail)
    _take_move(tail_move, tail, head)


def take_move_long_tail(move: Moves, head: list, tails: list) -> None:
    _take_move(move, head, [None, None])
    tmp_head = head
    for tail in tails:
        tail_move = get_tail_move(tmp_head, tail)
        _take_move(tail_move, tail, tmp_head)
        tmp_head = tail


with open("data_test", "r") as f:
    raw_data = f.read().split("\n")
tail_moves = []
tail_tail_moves = []
H_state = [0, 0]
T_state = [0, 0]
H2_state = [0, 0]
T_state_list = [[0, 0] for _ in range(9)]
for line in raw_data:
    move, count = line.split(" ")
    move = moves_dict[move]
    for _ in range(int(count)):
        take_move(move, H_state, T_state)
        if T_state not in tail_moves:
            tail_moves.append(copy(T_state))
        take_move_long_tail(move, H2_state, T_state_list)
        if T_state_list[-1] not in tail_tail_moves:
            tail_tail_moves.append(copy((T_state_list[-1])))

print(len(tail_moves))
print(len(tail_tail_moves))
