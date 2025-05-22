from typing import List, Tuple, Optional, Dict
from .base_solver import MazeSolver

class DFSSolver(MazeSolver):
    def solve(self, maze: List[List[int]], 
             start: Tuple[int, int], 
             end: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        width, height = len(maze[0]), len(maze)
        stack = [start]
        came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
        visited = set([start])
        
        while stack:
            current = stack.pop()
            if current == end:
                break
            
            # 随机探索顺序（使每次求解路径可能不同）
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            import random
            random.shuffle(directions)
            
            for dx, dy in directions:
                neighbor = (current[0] + dx, current[1] + dy)
                if (0 <= neighbor[0] < width and 0 <= neighbor[1] < height and
                    maze[neighbor[1]][neighbor[0]] == 0 and 
                    neighbor not in visited):
                    came_from[neighbor] = current
                    visited.add(neighbor)
                    stack.append(neighbor)
        
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