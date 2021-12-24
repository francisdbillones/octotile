from __future__ import annotations

from math import inf

from models import Board, ActionNode
import heapq


def solve_board(initial_board: Board, log_depth=False) -> list[ActionNode]:
    initial_node = ActionNode(initial_board)

    goal_node = astar_search(initial_node, log_depth=log_depth)
    if goal_node is None:
        raise ValueError("Board is unsolvable")
    return goal_node.path


def astar_search(initial_node: ActionNode, log_depth=False) -> ActionNode | None:
    heap: list[ActionNode] = []

    # best path maps a BoardNode
    # to the lowest possible cost known to get to that node
    # from initial_node
    best_cost: dict[ActionNode, int] = {}

    current_max_depth = 0

    for neighbour in initial_node.neighbours:
        heapq.heappush(heap, neighbour)
        best_cost[neighbour] = neighbour.cost

    while heap:
        node = heapq.heappop(heap)

        # log the current depth to stdout
        if log_depth is True and node.depth > current_max_depth:
            current_max_depth = node.depth
            print(f"Current depth: {current_max_depth}")

        if node.is_goal:
            return node

        for neighbour in node.neighbours:
            if neighbour.cost < best_cost.get(neighbour, inf):
                best_cost[neighbour] = neighbour.cost
                heapq.heappush(heap, neighbour)
    return None
