from __future__ import annotations

import numpy as np

from typing import Generator, Tuple

from helper import same_type_operation

Action = Tuple[int, int]

possible_moves = ((-1, 0), (1, 0), (0, -1), (0, 1))
inverse_actions = {(0, 1): (0, -1), (0, -1): (0, 1), (1, 0): (-1, 0), (-1, 0): (1, 0)}


class Board:
    def __init__(self, tiles: np.ndarray, height=3, width=3, blank=None):
        self.tiles = tiles

        self.blank = blank if blank is not None else tuple(tiles).index(0)

        self.height = height
        self.width = width

    @property
    def manhattan_distance(self) -> int:
        i = np.arange(self.height * self.width)[self.tiles != 0]
        i_cor, j_cor = divmod(i, self.width)
        goal_i, goal_j = divmod(self.tiles[self.tiles != 0] - 1, self.width)

        i_blank_cor, j_blank_cor = divmod(self.blank, self.width)

        return (
            np.sum(np.abs(goal_i - i_cor) + np.abs(goal_j - j_cor))
            + abs(i_blank_cor - (self.height - 1))
            + abs(j_blank_cor - (self.width - 1))
        )

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.tiles}, height={self.height}, width={self.width})"

    @property
    def actions(self) -> Generator[Action, None, None]:
        blank_i, blank_j = divmod(self.blank, self.width)

        # each element in each tuple represents a change in i and j
        # (-1, 0) -> i - 1, j, move blank tile up
        # (0, 1) -> i, j + 1, move blank tile right

        for move in possible_moves:
            delta_i, delta_j = move

            if not (0 <= blank_i + delta_i < self.height):
                continue

            if not (0 <= blank_j + delta_j < self.width):
                continue

            yield delta_i, delta_j

    def result_of(self, action: Action) -> Board:
        """
        Returns the result of performing a certain action as a new Board
        instance.
        """
        blank_i, blank_j = divmod(self.blank, self.width)
        delta_i, delta_j = action

        new_blank_i, new_blank_j = blank_i + delta_i, blank_j + delta_j

        tiles_copy = self.tiles.copy()

        # swap tiles
        (
            tiles_copy[blank_i * self.width + blank_j],
            tiles_copy[new_blank_i * self.width + new_blank_j],
        ) = (
            tiles_copy[new_blank_i * self.width + new_blank_j],
            tiles_copy[blank_i * self.width + blank_j],
        )
        return Board(
            tiles_copy,
            height=self.height,
            width=self.width,
            blank=new_blank_i * self.width + new_blank_j,
        )

    def __hash__(self):
        return hash(tuple(self.tiles))


class ActionNode:
    def __init__(
        self, board: Board, depth=0, action: Action = None, parent: ActionNode = None
    ):
        self.board = board
        self.depth = depth
        self.action = action
        self.parent = parent

        self.cost = self.depth + self.board.manhattan_distance

    @property
    def neighbours(self) -> Generator[ActionNode, None, None]:
        for action in self.board.actions:
            # if action is the inverse of this node's action, disregard the
            # action
            if self.action is not None and inverse_actions[self.action] == action:
                continue

            neighbor = ActionNode(
                self.board.result_of(action),
                depth=self.depth + 1,
                action=action,
                parent=self,
            )
            yield neighbor

    @property
    def path(self) -> Generator[ActionNode, None, None]:
        """
        Returns a list of the path of ActionNodes that this instance took, in
        chronological order.
        """
        if self.parent is not None:
            yield from self.parent.path
        yield self

    @property
    def is_goal(self) -> bool:
        return self.board.manhattan_distance == 0

    @same_type_operation("<")
    def __lt__(self, other: ActionNode) -> bool:
        return self.cost < other.cost

    @same_type_operation("<=")
    def __le__(self, other: ActionNode) -> bool:
        return self.cost <= other.cost

    @same_type_operation(">")
    def __gt__(self, other: ActionNode) -> bool:
        return self.cost > other.cost

    @same_type_operation(">=")
    def __ge__(self, other: ActionNode) -> bool:
        return self.cost >= other.cost

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self.board}, depth"
            f"={self.depth}, action="
            f"{self.action})"
        )

    def __hash__(self):
        return hash(self.board)
