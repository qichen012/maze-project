from typing import List, Optional

def print_maze(maze: List[List[int]], path: Optional[List[tuple]] = None) -> None:
    """在控制台打印迷宫（调试用）
    
    Args:
        maze: 迷宫矩阵
        path: 路径坐标列表（可选，会标出路径）
    """
    path = path or []
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if (x, y) in path:
                print("◇", end="")
            elif maze[y][x] == 1:
                print("██", end="")
            else:
                print("  ", end="")
        print()

def save_maze_to_file(maze: List[List[int]], filename: str) -> None:
    """将迷宫保存到文本文件"""
    with open(filename, 'w') as f:
        for row in maze:
            f.write("".join(str(cell) for cell in row) + "\n")