from abc import ABC, abstractmethod
from typing import List

class MazeGenerator(ABC):
    """所有迷宫生成器的基类"""
    
    @abstractmethod
    def generate(self, width: int, height: int) -> List[List[int]]:
        """生成迷宫矩阵
        
        Args:
            width: 迷宫宽度（最终会调整为奇数）
            height: 迷宫高度（最终会调整为奇数）
            
        Returns:
            二维数组，0表示通路，1表示墙壁
        """
        pass

    @staticmethod
    def _ensure_odd(n: int) -> int:
        """确保输入数字为奇数"""
        return n if n % 2 == 1 else n - 1