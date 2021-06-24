#! /usr/bin/python3

import sys
from typing import List
from models import Board
from octotile import BoardSolver

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

        for i, line in enumerate(lines):
            board.append([])
            tiles = [tile.strip() for tile in line.split(",")]

            for j, tile in enumerate(tiles):
                if tile == "_":
                    board[i].append(tile)
                else:
                    board[i].append(int(tile))
        return Board(board)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("Usage: ./run.py input.txt out.txt")
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
