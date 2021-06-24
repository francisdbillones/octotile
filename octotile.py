from typing import List, Optional

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

    @staticmethod
    def astar_search(initial_node: BoardNode) -> Optional[BoardNode]:
        heap: List[BoardNode] = []
        seen = set()

        for neighbour in initial_node.neighbours:
            heapq.heappush(heap, neighbour)
            seen.add(neighbour)

        while heap:
            node = heapq.heappop(heap)

            if node.is_goal():
                return node

            for neighbour in node.neighbours:
                if neighbour not in seen:
                    heapq.heappush(heap, neighbour)
                    seen.add(neighbour)
        return None
