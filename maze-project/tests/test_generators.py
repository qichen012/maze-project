import unittest
from generators import DFSGenerator, PrimGenerator

class TestMazeGenerators(unittest.TestCase):
    def test_dfs_generator(self):
        generator = DFSGenerator(seed=42)
        maze = generator.generate(21, 21)
        self.assertEqual(len(maze), 21)
        self.assertEqual(maze[1][1], 0)  # 起点应为通路
        self.assertEqual(maze[0][1], 1)   # 边界应为墙

    def test_prim_generator(self):
        generator = PrimGenerator()
        maze = generator.generate(21, 21)
        # Prim算法生成的迷宫应该有更多通路
        path_count = sum(row.count(0) for row in maze)
        self.assertGreater(path_count, 100)

if __name__ == '__main__':
    unittest.main()