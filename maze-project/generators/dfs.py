import random
from .base_generator import MazeGenerator
from typing import List, Optional

class DFSGenerator(MazeGenerator):
    """使用深度优先搜索(DFS)算法生成迷宫"""
    
    def __init__(self, seed: Optional[int] = None):
        """
        Args:
            seed: 随机种子（用于重现相同迷宫）
        """
        self.seed = seed
        if seed is not None:
            random.seed(seed)

    def generate(self, width: int, height: int) -> List[List[int]]:
        # 调整尺寸为奇数
        width = self._ensure_odd(width)
        height = self._ensure_odd(height)
        
        # 初始化全墙迷宫
        maze = [[1 for _ in range(width)] for _ in range(height)]
        stack = [(1, 1)]  # 起点
        maze[1][1] = 0

        while stack:
            x, y = stack[-1]
            # 获取未访问的相邻点（间隔2格）
            neighbors = self._get_unvisited_neighbors(x, y, maze)
            
            if neighbors:
                nx, ny = random.choice(neighbors)
                # 打通当前点和选中点之间的墙
                maze[(y + ny)//2][(x + nx)//2] = 0
                maze[ny][nx] = 0
                stack.append((nx, ny))
            else:
                stack.pop()
        
        return maze

    def _get_unvisited_neighbors(self, x: int, y: int, maze: List[List[int]]) -> list:
        """获取未访问的相邻点"""
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        neighbors = []
        width, height = len(maze[0]), len(maze)
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < width and 0 < ny < height and maze[ny][nx] == 1:
                neighbors.append((nx, ny))
        return neighbors