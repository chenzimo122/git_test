import pygame
import random

# Game Constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Color Definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Tetris Pieces
SHAPES = [
    [[1, 1, 1, 1]],  # I Shape
    [[1, 1], [1, 1]],  # O Shape
    [[0, 1, 0], [1, 1, 1]],  # T Shape
    [[1, 1, 0], [0, 1, 1]],  # S Shape
    [[0, 1, 1], [1, 1, 0]],  # Z Shape
    [[1, 0, 0], [1, 1, 1]],  # L Shape
    [[0, 0, 1], [1, 1, 1]],  # J Shape
]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.board = [[0] * (SCREEN_WIDTH // BLOCK_SIZE) for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
        self.current_piece = self.new_piece()
        self.current_position = [0, SCREEN_WIDTH // BLOCK_SIZE // 2 - 1]

    def new_piece(self):
        shape = random.choice(SHAPES)
        return shape

    def rotate_piece(self):
        self.current_piece = list(zip(*self.current_piece[::-1]))

    def collision(self, offset):
        for i, row in enumerate(self.current_piece):
            for j, val in enumerate(row):
                if val:
                    x = j + self.current_position[1] + offset[1]
                    y = i + self.current_position[0] + offset[0]
                    if x < 0 or x >= len(self.board[0]) or y >= len(self.board):
                        return True
                    if y >= 0 and self.board[y][x]:
                        return True
        return False

    def merge_piece(self):
        for i, row in enumerate(self.current_piece):
            for j, val in enumerate(row):
                if val:
                    self.board[i + self.current_position[0]][j + self.current_position[1]] = 1

    def clear_lines(self):
        new_board = [row for row in self.board if sum(row) < len(row)]
        lines_cleared = len(self.board) - len(new_board)
        self.board = [[0] * len(self.board[0])] * lines_cleared + new_board

    def run(self):
        pygame.init()
        while True:
            self.screen.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return  

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                if not self.collision((0, -1)):
                    self.current_position[1] -= 1
            if keys[pygame.K_RIGHT]:
                if not self.collision((0, 1)):
                    self.current_position[1] += 1
            if keys[pygame.K_DOWN]:
                if not self.collision((1, 0)):
                    self.current_position[0] += 1
            if keys[pygame.K_UP]:
                self.rotate_piece()

            if not self.collision((1, 0)):
                self.current_position[0] += 1
            else:
                self.merge_piece()
                self.clear_lines()
                self.current_piece = self.new_piece()
                self.current_position = [0, SCREEN_WIDTH // BLOCK_SIZE // 2 - 1]

            for i, row in enumerate(self.board):
                for j, val in enumerate(row):
                    if val:
                        pygame.draw.rect(self.screen, BLACK, (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

            pygame.display.flip()
            self.clock.tick(10)

# Start the game
if __name__ == '__main__':
    Tetris().run()