from typing import List, Tuple

def validate_maze_path(maze: List[List[int]], 
                      path: List[Tuple[int, int]]) -> bool:
    """验证路径是否合法"""
    for x, y in path:
        if maze[y][x] == 1:
            return False
    
    for i in range(1, len(path)):
        dx = abs(path[i][0] - path[i-1][0])
        dy = abs(path[i][1] - path[i-1][1])
        if dx + dy != 1:
            return False
    
    return True

def smooth_path(path: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """路径平滑处理（去除冗余拐点）"""
    if len(path) <= 2:
        return path.copy()
    
    smoothed = [path[0]]
    for i in range(1, len(path)-1):
        prev = smoothed[-1]
        next_ = path[i+1]
        # 如果三点不在一条直线，保留当前点
        if (prev[0] != path[i][0] or path[i][0] != next_[0]) and \
           (prev[1] != path[i][1] or path[i][1] != next_[1]):
            smoothed.append(path[i])
    smoothed.append(path[-1])
    return smoothed