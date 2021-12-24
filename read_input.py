from __future__ import annotations

import numpy as np

from models import Board

def read_board_from_file(filename: str) -> Board:
    with open(filename, "r") as f:
        lines = f.readlines()

    if (error := validate_input(lines)) is not None:
        raise ValueError(error)
    
    return read_input(lines)

def read_input(lines: list[str]) -> Board:
    board = []

    height = len(lines)
    width = len(lines[0].split(","))

    for line in lines:
        tiles = [tile.strip() for tile in line.split(",")]

        board.extend([int(tile) for tile in tiles])
    return Board(np.array(board), height=height, width=width)

def validate_input(lines: list[str]) -> str | None:
    if not lines:
            return "File empty"

    seen = set()
    has_blank = False

    height = len(lines)
    width = len(lines[0].split(","))

    expected_nums = set(range(1, height * width))

    for line in lines:
        tiles = [tile.strip() for tile in line.split(",")]
        for tile in tiles:
            if tile == "0":
                if has_blank is True:
                    return "Too many blank tiles in input. Only one is allowed."
                    
                has_blank = True
                continue

            elif not tile.isnumeric():
                return "Non-blank tiles must be integers."

            elif tile in seen:
                return "Duplicate tiles"

            seen.add(int(tile))

    if seen != expected_nums:
        return "Incomplete/invalid tile values"
    
    if has_blank is not True:
        return "No blank tile in input"
