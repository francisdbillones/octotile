#! /usr/bin/python3

import sys
import time
from typing import List
from models import Board, BoardNode
from octotile import BoardSolver
import random

# map moves to English words
MOVES_TO_WORDS = {
    (0, 1): "move right",
    (0, -1): "move left",
    (1, 0): "move down",
    (-1, 0): "move up",
}


class BoardInputReader:
    """
    Parse user input into a Board instance.
    """

    def __init__(self):
        return

    def __call__(self, in_filename):
        with open(in_filename, "r") as reader:
            lines = reader.readlines()

        BoardInputReader._validate(lines)
        return BoardInputReader._to_board(lines)

    @staticmethod
    def _validate(lines: List[str]):
        if not lines:
            raise ValueError("File empty")
        seen = set()
        has_blank = False

        height = len(lines)
        width = len(lines[0].split(","))

        expected_nums = set(range(1, height * width))

        for i, line in enumerate(lines):
            tiles = [tile.strip() for tile in line.split(",")]
            for j, tile in enumerate(tiles):
                if tile == "_":
                    if has_blank:
                        raise ValueError(
                            "Too many blank tiles in input. Only one is allowed."
                        )
                    has_blank = True
                    continue
                elif not tile.isnumeric():
                    raise ValueError("Non-blank tiles must be integers.")
                elif tile in seen:
                    raise ValueError("Duplicate tiles")
                seen.add(int(tile))

        if seen != expected_nums:
            raise ValueError("Incomplete/invalid tile values")

    @staticmethod
    def _to_board(lines: List[str]):
        board = []

        height = len(lines)
        width = len(lines[0].split(","))
        print(height, width)

        for i, line in enumerate(lines):
            tiles = [tile.strip() for tile in line.split(",")]

            for j, tile in enumerate(tiles):
                if tile == "_":
                    board.append(tile)
                else:
                    board.append(int(tile))
        return Board(board, height=height, width=width)


def benchmark():
    height = int(input("Board height: "))
    width = int(input("Board width: "))
    min_moves = int(input("Min moves: "))
    max_moves = int(input("Max moves: "))
    times = []
    for _ in range(1_000):
        board = random_board(height, width, min_moves, max_moves)
        solver = BoardSolver(board, log_depth=False)

        start = time.perf_counter_ns()
        solver.solve()
        end = time.perf_counter_ns()

        times.append(end - start)

    average_time = sum(times) / 1_000

    print(f"Average time to solve board: {average_time}ns (" f"{average_time / 1e6}ms)")


def random_board(height, width, min_moves, max_moves):
    tiles = [*range(1, height * width), "_"]
    initial_board = Board(tiles, height=height, width=width)
    node = BoardNode(initial_board)

    move_count = random.randrange(min_moves, max_moves + 1)

    for _ in range(move_count):
        random_action = random.choice(node.board.actions)
        result_board = node.board.result_of(random_action)
        node = BoardNode(result_board, action=random_action)
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

    input_reader = BoardInputReader()
    board = input_reader(input_filename)

    solver = BoardSolver(board)

    path = solver.solve()

    with open(output_filename, "w") as writer:
        print("writing")
        for node in path:
            action = node.action
            if action is None:
                continue
            writer.write(MOVES_TO_WORDS[action] + "\n")
