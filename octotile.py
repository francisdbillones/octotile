from typing import List, Optional, Dict

from models import Board, BoardNode
import heapq


class BoardSolver:
    def __init__(self, initial_board: Board):
        self.initial_node = BoardNode(initial_board)

    def solve(self) -> List[BoardNode]:
        goal_node = self.astar_search(self.initial_node)
        if goal_node is None:
            raise ValueError("Board is unsolvable")
        return goal_node.path

    def astar_search(self, initial_node: BoardNode) -> Optional[BoardNode]:
        heap: List[BoardNode] = []

        # best path maps a BoardNode
        # to the lowest possible cost known to get to that node
        # from initial_node
        best_cost: Dict[BoardNode, int] = {}

        current_max_depth = 0

        for neighbour in initial_node.neighbours:
            heapq.heappush(heap, neighbour)
            best_cost[neighbour] = neighbour.cost

        while heap:
            node = heapq.heappop(heap)

            # log the current depth to stdout
            if node.depth > current_max_depth:
                current_max_depth = node.depth
                print(f"Current depth: {current_max_depth}")

            if node.is_goal():
                return node

            for neighbour in node.neighbours:
                if (
                    best_cost.get(neighbour) is None
                    or neighbour.cost < best_cost[neighbour]
                ):
                    best_cost[neighbour] = neighbour.cost
                    heapq.heappush(heap, neighbour)
        return None
