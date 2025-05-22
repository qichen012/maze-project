from collections import deque
from typing import List, Tuple, Optional, Dict
from .base_solver import MazeSolver

class BFSSolver(MazeSolver):
    def solve(self, maze: List[List[int]], 
             start: Tuple[int, int], 
             end: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        width, height = len(maze[0]), len(maze)
        queue = deque([start])
        came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
        
        while queue:
            current = queue.popleft()
            if current == end:
                break
            
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = current[0] + dx, current[1] + dy
                if (0 <= nx < width and 0 <= ny < height and 
                    maze[ny][nx] == 0 and (nx, ny) not in came_from):
                    came_from[(nx, ny)] = current
                    queue.append((nx, ny))
        
        return self._reconstruct_path(came_from, start, end)
    
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