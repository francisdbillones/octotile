#! /usr/bin/env python3

from __future__ import annotations

import numpy as np

import sys
import time
from models import Board, ActionNode
from solver import solve_board
import random

from read_input import read_board_from_file

# map moves to English words
MOVES_TO_WORDS = {
    (0, 1): "move right",
    (0, -1): "move left",
    (1, 0): "move down",
    (-1, 0): "move up",
}


def benchmark():
    height = int(input("Board height: "))
    width = int(input("Board width: "))
    min_moves = int(input("Min moves: "))
    max_moves = int(input("Max moves: "))

    start = time.perf_counter_ns()

    count = 0

    while True:
        board = random_board(height, width, min_moves, max_moves)
        path = solve_board(board, log_depth=False)
        count += 1
        if (time.perf_counter_ns() - start) > 10e9:
            break

    end = time.perf_counter_ns()

    print(f"Solved {count} boards")
    print(
        f"Average time to solve board: {(end - start) / count}ns ("
        f"{(end - start) / 1e6 / count}ms)"
    )


def random_board(height: int, width: int, min_moves: int, max_moves: int):
    tiles = np.array([*range(1, height * width), 0])
    board = Board(tiles, height=height, width=width)
    node = ActionNode(board)

    move_count = random.randint(min_moves, max_moves)

    for _ in range(move_count):
        random_action = random.choice(tuple(node.board.actions))
        result_board = node.board.result_of(random_action)
        node = ActionNode(result_board, action=random_action)
    return node.board


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Benchmarking...")
        benchmark()
        sys.exit(0)

    if len(sys.argv) != 3:
        output_filename = "moves.txt"
    else:
        output_filename = sys.argv[2]
    input_filename = sys.argv[1]

    board = read_board_from_file(input_filename)

    path = solve_board(board, log_depth=True)

    with open(output_filename, "w") as writer:
        print("writing")
        for node in path:
            action = node.action
            if action is None:
                continue
            writer.write(MOVES_TO_WORDS[action] + "\n")
