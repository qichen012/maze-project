from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

class MazeSolver(ABC):
    @abstractmethod
    def solve(self, maze: List[List[int]], 
             start: Tuple[int, int], 
             end: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """求解迷宫路径
        
        Args:
            maze: 二维迷宫矩阵（0=通路，1=墙壁）
            start: 起点坐标 (x, y)
            end: 终点坐标 (x, y)
            
        Returns:
            路径坐标列表（包含起点和终点），若无解返回None
        """
        pass