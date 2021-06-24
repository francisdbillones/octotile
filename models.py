from __future__ import annotations

import copy
from functools import cached_property
from typing import List, Union, Tuple, Optional

Tile = Union[int, str]


class Board:
    def __init__(self, tiles: List[List[Tile]]):
        self.tiles: List[List[Tile]] = []
        self.blank = None

        self.height = len(tiles)
        self.width = len(tiles[0])

        for i, row in enumerate(tiles):
            self.tiles.append([])
            for j, tile in enumerate(row):
                if tile == "_":
                    self.blank = i, j

                self.tiles[i].append(tile)

    @cached_property
    def manhattan_distance(self) -> int:
        total_distance = 0
        for i, row in enumerate(self.tiles):
            for j, tile in enumerate(row):
                total_distance += self.manhattan_distance_at(tile, i, j)
        return total_distance

    def manhattan_distance_at(self, value: Tile, i: int, j: int) -> int:
        """
        Returns the manhattan distance of a cell at coordinates (i, j)
        given the value it holds.
        """
        if value == "_":
            goal_i, goal_j = self.height - 1, self.width - 1
        else:
            goal_i = (value - 1) // self.width
            goal_j = (value - 1) % self.width

        return abs(goal_i - i) + abs(goal_j - j)

    def __repr__(self) -> str:
        return str(self.tiles)

    @cached_property
    def actions(self) -> List[Tuple[int, int]]:
        blank_i, blank_j = self.blank

        # each element in each tuple represents a change in i and j
        # (-1, 0) -> i - 1, j, move blank tile up
        # (0, 1) -> i, j + 1, move blank tile right
        possible_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        allowed_actions = []
        for move in possible_moves:
            delta_i, delta_j = move

            if not (0 <= blank_i + delta_i < self.height):
                continue
            if not (0 <= blank_j + delta_j < self.width):
                continue

            allowed_actions.append((delta_i, delta_j))
        return allowed_actions

    def result_of(self, action: Tuple[int, int]) -> Board:
        """
        Returns the result of performing a certain action as a new Board
        instance.
        """
        blank_i, blank_j = self.blank
        delta_i, delta_j = action

        new_blank_i, new_blank_j = blank_i + delta_i, blank_j + delta_j

        tiles_copy = copy.deepcopy(self.tiles)

        # swap tiles
        tiles_copy[blank_i][blank_j], tiles_copy[new_blank_i][new_blank_j] = (
            tiles_copy[new_blank_i][new_blank_j],
            tiles_copy[blank_i][blank_j],
        )
        return Board(tiles_copy)

    def __hash__(self):
        return hash(tuple(row) for row in self.tiles)


class BoardNode:
    def __init__(
        self,
        board: Board,
        depth=0,
        action: Optional[Tuple[int, int]] = None,
        parent: Optional[BoardNode] = None,
    ):
        self.board = board
        self.depth = depth
        self.action = action
        self.parent = parent

        self.cost = self.depth + self.board.manhattan_distance

    @cached_property
    def neighbours(self) -> List[BoardNode]:
        _neighbours = []
        for action in self.board.actions:
            # if action is the inverse of this node's action, disregard the
            # action
            if self._is_inverse_action(action):
                continue
            resulting_board = self.board.result_of(action)
            resulting_board_node = BoardNode(
                resulting_board, self.depth + 1, action, self
            )
            _neighbours.append(resulting_board_node)
        return _neighbours

    def _is_inverse_action(self, action: Tuple[int, int]) -> bool:
        # if this node is the initial node, just return false as all actions
        # are allowed
        if self.action is None:
            return False

        other_delta_i, other_delta_j = action
        this_delta_i, this_delta_j = self.action

        if this_delta_i != 0 and this_delta_i == -other_delta_i:
            return True
        elif this_delta_j != 0 and this_delta_j == -other_delta_j:
            return True
        return False

    @cached_property
    def path(self) -> List[BoardNode]:
        """
        Returns a list of the path of BoardNodes that this instance took, in
        chronological order.
        """
        if self.parent is None:
            return [self]
        return self.parent.path + [self]

    def is_goal(self) -> bool:
        return self.board.manhattan_distance == 0

    def __lt__(self, other: BoardNode) -> bool:
        if not isinstance(other, BoardNode):
            raise TypeError(
                f"< not supported between instances of "
                f"'BoardNode' and {type(other).__name__}"
            )
        return self.cost < other.cost

    def __le__(self, other: BoardNode) -> bool:
        if not isinstance(other, BoardNode):
            raise TypeError(
                f"<= not supported between instances of "
                f"'BoardNode' and {type(other).__name__}"
            )
        return self.cost <= other.cost

    def __gt__(self, other: BoardNode) -> bool:
        if not isinstance(other, BoardNode):
            raise TypeError(
                f"> not supported between instances of "
                f"'BoardNode' and {type(other).__name__}"
            )
        return self.cost > other.cost

    def __ge__(self, other: BoardNode) -> bool:
        if not isinstance(other, BoardNode):
            raise TypeError(
                f">= not supported between instances of "
                f"'BoardNode' and {type(other).__name__}"
            )
        return self.cost >= other.cost

    def __repr__(self) -> str:
        return (
            f"BoardNode({self.board}, cost={self.cost}, depth"
            f"={self.depth}, action="
            f"{self.action})"
        )

    def __hash__(self):
        return hash(self.board)
