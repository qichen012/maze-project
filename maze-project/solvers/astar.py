import heapq
from typing import List, Tuple, Optional, Dict
from .base_solver import MazeSolver

class AStarSolver(MazeSolver):
    def solve(self, maze: List[List[int]], 
             start: Tuple[int, int], 
             end: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        width, height = len(maze[0]), len(maze)
        
        # 优先级队列: (f_score, x, y)
        open_set = []
        heapq.heappush(open_set, (0 + self._heuristic(start, end), start[0], start[1]))
        
        came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
        g_score: Dict[Tuple[int, int], float] = {start: 0}
        
        while open_set:
            _, x, y = heapq.heappop(open_set)
            current = (x, y)
            
            if current == end:
                break
            
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                neighbor = (x + dx, y + dy)
                if not (0 <= neighbor[0] < width and 0 <= neighbor[1] < height):
                    continue
                if maze[neighbor[1]][neighbor[0]] == 1:
                    continue
                    
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + self._heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score, neighbor[0], neighbor[1]))
        
        return self._reconstruct_path(came_from, start, end)
    
    def _heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """曼哈顿距离启发函数"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def _reconstruct_path(self, 
                        came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]],
                        start: Tuple[int, int],
                        end: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        current = end
        path = []
        while current != start:
            path.append(current)
            current = came_from.get(current, None)
            if current is None:
                return None
        path.append(start)
        path.reverse()
        return path