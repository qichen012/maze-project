import unittest
from generators.dfs import DFSGenerator
from solvers import BFSSolver, DFSSolver, AStarSolver

class TestMazeSolvers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """生成一个固定的测试迷宫"""
        cls.generator = DFSGenerator(seed=42)
        cls.maze = cls.generator.generate(15, 15)  # 使用稍大的迷宫
        # 确保起点和终点是通路且不在同一位置
        cls.start = (1, 1)
        cls.end = (13, 13)
        cls.maze[cls.start[1]][cls.start[0]] = 0
        cls.maze[cls.end[1]][cls.end[0]] = 0

    def _validate_path(self, path):
        """验证路径是否合法"""
        self.assertIsInstance(path, list, "路径应该是列表")
        self.assertGreaterEqual(len(path), 2, "路径至少应包含起点和终点")
        
        # 检查起点终点
        self.assertEqual(path[0], self.start, "路径起点不正确")
        self.assertEqual(path[-1], self.end, "路径终点不正确")
        
        # 检查路径连续性
        for i in range(1, len(path)):
            dx = abs(path[i][0] - path[i-1][0])
            dy = abs(path[i][1] - path[i-1][1])
            self.assertEqual(dx + dy, 1, 
                          f"路径不连续：{path[i-1]} -> {path[i]}")

        # 检查路径是否都在通路上
        for x, y in path:
            self.assertEqual(self.maze[y][x], 0,
                          f"路径经过墙壁位置：({x}, {y})")

    def test_bfs_solver(self):
        """测试BFS求解器"""
        solver = BFSSolver()
        path = solver.solve(self.maze, self.start, self.end)
        
        self.assertIsNotNone(path, "BFS应能找到路径")
        self._validate_path(path)
        
        # BFS应找到最短路径
        if path:  # 防御性编程
            other_path = DFSSolver().solve(self.maze, self.start, self.end)
            if other_path:  # 只有当DFS也找到路径时比较
                self.assertLessEqual(len(path), len(other_path),
                                  "BFS路径应比DFS更短或等长")

    def test_dfs_solver(self):
        """测试DFS求解器"""
        solver = DFSSolver()
        path = solver.solve(self.maze, self.start, self.end)
        
        self.assertIsNotNone(path, "DFS应能找到路径")
        self._validate_path(path)

    def test_astar_solver(self):
        """测试A*求解器"""
        solver = AStarSolver()
        path = solver.solve(self.maze, self.start, self.end)
        
        self.assertIsNotNone(path, "A*应能找到路径")
        self._validate_path(path)
        
        # A*路径长度应与BFS相同（都是最短路径）
        if path:  # 防御性编程
            bfs_path = BFSSolver().solve(self.maze, self.start, self.end)
            if bfs_path:
                self.assertEqual(len(path), len(bfs_path),
                              "A*和BFS应找到相同长度的最短路径")

    def test_unsolvable_maze(self):
        """测试无解迷宫情况"""
        # 创建一个无解的迷宫（起点被隔离）
        unsolvable_maze = [row.copy() for row in self.maze]
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            unsolvable_maze[self.start[1]+dy][self.start[0]+dx] = 1
        
        for solver in [BFSSolver(), DFSSolver(), AStarSolver()]:
            path = solver.solve(unsolvable_maze, self.start, self.end)
            self.assertIsNone(path, f"{solver.__class__.__name__} 应返回None")

if __name__ == '__main__':
    unittest.main(failfast=True)  # 遇到第一个错误就停止