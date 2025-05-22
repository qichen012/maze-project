import pygame
import sys
import time
from generators import DFSGenerator, PrimGenerator
from solvers import BFSSolver, DFSSolver, AStarSolver

# 颜色定义
COLORS = {
    'background': (40, 40, 40),
    'wall': (20, 20, 60),
    'path': (100, 200, 255),
    'solution': (255, 100, 100),
    'start': (50, 255, 50),
    'end': (255, 50, 50),
    'text': (255, 255, 255),
    'button': (70, 70, 70),
    'button_hover': (100, 100, 100)
}

class MazeDemo:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("迷宫生成与求解演示")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 20)
        
        # 算法选择
        self.generators = {
            'DFS': DFSGenerator(),
            'Prim': PrimGenerator()
        }
        self.solvers = {
            'BFS': BFSSolver(),
            'DFS': DFSSolver(),
            'A*': AStarSolver()
        }
        
        # 默认参数
        self.maze_size = 31  # 推荐奇数
        self.current_gen = 'DFS'
        self.current_solver = 'A*'
        self.maze = None
        self.path = None
        self.gen_time = 0
        self.solve_time = 0
        self.show_solution = True
        
        # UI元素 - 修改了键名以匹配算法名称
        self.buttons = {
            'generate': {'rect': pygame.Rect(20, 20, 150, 40), 'text': '生成迷宫'},
            'solve': {'rect': pygame.Rect(190, 20, 150, 40), 'text': '求解迷宫'},
            'gen_dfs': {'rect': pygame.Rect(20, 80, 100, 30), 'text': 'DFS生成'},
            'gen_prim': {'rect': pygame.Rect(130, 80, 100, 30), 'text': 'Prim生成'},
            'sol_bfs': {'rect': pygame.Rect(240, 80, 80, 30), 'text': 'BFS'},
            'sol_dfs': {'rect': pygame.Rect(330, 80, 80, 30), 'text': 'DFS'},
            'sol_astar': {'rect': pygame.Rect(420, 80, 80, 30), 'text': 'A*'}  # 修改为astar
        }
        
        self.generate_maze()
    
    def generate_maze(self):
        """生成新迷宫"""
        start_time = time.time()
        self.maze = self.generators[self.current_gen].generate(
            self.maze_size, self.maze_size
        )
        self.gen_time = time.time() - start_time
        self.path = None
        self.solve_time = 0
        
        # 设置起点和终点
        self.start = (1, 1)
        self.end = (self.maze_size-2, self.maze_size-2)
        self.maze[self.start[1]][self.start[0]] = 0
        self.maze[self.end[1]][self.end[0]] = 0
    
    def solve_maze(self):
        """求解迷宫"""
        if not self.maze:
            return
            
        start_time = time.time()
        self.path = self.solvers[self.current_solver].solve(
            self.maze, self.start, self.end
        )
        self.solve_time = time.time() - start_time
    
    def draw_maze(self):
        """绘制迷宫和路径"""
        if not self.maze:
            return
            
        cell_size = min(
            (self.width - 300) // self.maze_size,
            (self.height - 150) // self.maze_size
        )
        offset_x, offset_y = 50, 150
        
        # 绘制迷宫
        for y in range(len(self.maze)):
            for x in range(len(self.maze[0])):
                rect = pygame.Rect(
                    offset_x + x * cell_size,
                    offset_y + y * cell_size,
                    cell_size, cell_size
                )
                color = COLORS['wall'] if self.maze[y][x] == 1 else COLORS['background']
                pygame.draw.rect(self.screen, color, rect)
                
                # 标记路径
                if self.show_solution and self.path and (x, y) in self.path:
                    pygame.draw.rect(self.screen, COLORS['solution'], rect)
        
        # 标记起点和终点
        start_rect = pygame.Rect(
            offset_x + self.start[0] * cell_size,
            offset_y + self.start[1] * cell_size,
            cell_size, cell_size
        )
        end_rect = pygame.Rect(
            offset_x + self.end[0] * cell_size,
            offset_y + self.end[1] * cell_size,
            cell_size, cell_size
        )
        pygame.draw.rect(self.screen, COLORS['start'], start_rect)
        pygame.draw.rect(self.screen, COLORS['end'], end_rect)
        
        # 绘制网格线
        for y in range(len(self.maze)):
            for x in range(len(self.maze[0])):
                rect = pygame.Rect(
                    offset_x + x * cell_size,
                    offset_y + y * cell_size,
                    cell_size, cell_size
                )
                pygame.draw.rect(self.screen, (60, 60, 60), rect, 1)
    
    def draw_ui(self):
        """绘制用户界面"""
        # 绘制按钮
        for name, btn in self.buttons.items():
            color = COLORS['button_hover'] if btn['rect'].collidepoint(pygame.mouse.get_pos()) else COLORS['button']
            pygame.draw.rect(self.screen, color, btn['rect'], border_radius=5)
            text = self.font.render(btn['text'], True, COLORS['text'])
            text_rect = text.get_rect(center=btn['rect'].center)
            self.screen.blit(text, text_rect)
        
        # 修正这里：使用统一的算法名称映射
        gen_button_map = {'DFS': 'gen_dfs', 'Prim': 'gen_prim'}
        sol_button_map = {'BFS': 'sol_bfs', 'DFS': 'sol_dfs', 'A*': 'sol_astar'}
        
        # 标记当前选择的算法
        if self.current_gen in gen_button_map:
            pygame.draw.rect(self.screen, (200, 200, 0), 
                            self.buttons[gen_button_map[self.current_gen]]['rect'], 2, 5)
        if self.current_solver in sol_button_map:
            pygame.draw.rect(self.screen, (200, 200, 0), 
                            self.buttons[sol_button_map[self.current_solver]]['rect'], 2, 5)
        
        # 显示信息
        info_text = [
            f"迷宫大小: {self.maze_size}x{self.maze_size}",
            f"生成算法: {self.current_gen} ({self.gen_time:.3f}s)",
            f"求解算法: {self.current_solver}",
            f"求解时间: {self.solve_time:.8f}s" if self.path else "",
            f"路径长度: {len(self.path)}" if self.path else ""
        ]
        
        for i, text in enumerate(info_text):
            if text:
                text_surface = self.font.render(text, True, COLORS['text'])
                self.screen.blit(text_surface, (20, 130 + i * 25))
    
    def handle_events(self):
        """处理用户输入"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    for name, btn in self.buttons.items():
                        if btn['rect'].collidepoint(event.pos):
                            if name == 'generate':
                                self.generate_maze()
                            elif name == 'solve':
                                self.solve_maze()
                            elif name.startswith('gen_'):
                                self.current_gen = name[4:].upper()
                            elif name.startswith('sol_'):
                                # 特殊处理A*按钮
                                if name == 'sol_astar':
                                    self.current_solver = 'A*'
                                else:
                                    self.current_solver = name[4:].upper()
    
    def run(self):
        """主循环"""
        while True:
            self.screen.fill(COLORS['background'])
            self.handle_events()
            self.draw_maze()
            self.draw_ui()
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    demo = MazeDemo()
    demo.run()