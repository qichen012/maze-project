import random
from typing import List
from .base_generator import MazeGenerator

class PrimGenerator(MazeGenerator):
    """使用Prim算法生成迷宫（生成更多分支的复杂迷宫）"""
    
    def generate(self, width: int, height: int) -> List[List[int]]:
        width = self._ensure_odd(width)
        height = self._ensure_odd(height)
        
        maze = [[1 for _ in range(width)] for _ in range(height)]
        frontier = []
        
        # 随机选择起点
        start_x, start_y = random.randrange(1, width, 2), random.randrange(1, height, 2)
        maze[start_y][start_x] = 0
        frontier.extend(self._get_frontier_cells(start_x, start_y, width, height, maze))
        
        while frontier:
            x, y = frontier.pop(random.randrange(len(frontier)))
            neighbors = self._get_connected_neighbors(x, y, maze)
            
            if neighbors:
                nx, ny = random.choice(neighbors)
                maze[(y + ny)//2][(x + nx)//2] = 0
                maze[y][x] = 0
                frontier.extend(self._get_frontier_cells(x, y, width, height, maze))
        
        return maze

    def _get_frontier_cells(self, x: int, y: int, width: int, height: int, 
                           maze: List[List[int]]) -> list:
        """获取可以作为新边界的单元格"""
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        frontier = []
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < width and 0 < ny < height and maze[ny][nx] == 1:
                frontier.append((nx, ny))
        return frontier

    def _get_connected_neighbors(self, x: int, y: int, 
                               maze: List[List[int]]) -> list:
        """获取已连接的邻居点（距离1格）"""
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        connected = []
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze):
                if maze[ny][nx] == 0:
                    connected.append((nx, ny))
        return connected