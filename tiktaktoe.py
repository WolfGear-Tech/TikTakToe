import pygame, sys
import numpy as np


class TikTakToe:
    def __init__(self) -> None:
        self.WIDTH = 600
        self.HEIGHT = 600
        self.BOARD_ROWS = 3
        self.BOARD_COLS = 3
        self.MARGIN = 20
        self.SPACE = 40
        self.LINE_WIDTH = 10
        self.CROSS_WIDTH = 20
        self.CIRCLE_RADIUS = 60
        self.CIRCLE_WIDTH = 15
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.BG_COLOR = (28, 170, 156)
        self.LINE_COLOR = (23, 145, 135)
        self.player = 1

        pygame.init()
        pygame.display.set_caption("Tik Tak Toe")
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.screen.fill(self.BG_COLOR)
        self.DrawBoard()

        self.board = np.zeros((self.BOARD_ROWS, self.BOARD_COLS))

    def DrawBoard(self):
        for line in range(1, 3):
            pygame.draw.line(
                self.screen,
                self.LINE_COLOR,
                (self.MARGIN, line * 200),
                (self.WIDTH - self.MARGIN, line * 200),
                self.LINE_WIDTH,
            )
            pygame.draw.line(
                self.screen,
                self.LINE_COLOR,
                (line * 200, self.MARGIN),
                (line * 200, self.HEIGHT - self.MARGIN),
                self.LINE_WIDTH,
            )

    def MarkSquare(self, row, col, player):
        if self.AvaialbleSquares(row, col):
            self.board[row][col] = player
            if player == 1:
                self.DrawX(row, col)
            if player == 2:
                self.DrawO(row, col)

    def AvaialbleSquares(self, row, col):
        return self.board[row][col] == 0

    def IsBoardFull(self):
        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                if self.board[row][col] == 0:
                    return False
        return True

    def CheckWiner(self, player):
        win = None

        n = len(self.board)

        # checking rows
        for i in range(n):
            win = True
            for j in range(n):
                if self.board[i][j] != player:
                    win = False
                    break
            if win:
                return win

        # checking columns
        for i in range(n):
            win = True
            for j in range(n):
                if self.board[j][i] != player:
                    win = False
                    break
            if win:
                return win

        # checking diagonals
        win = True
        for i in range(n):
            if self.board[i][i] != player:
                win = False
                break
        if win:
            return win

        win = True
        for i in range(n):
            if self.board[i][n - 1 - i] != player:
                win = False
                break
        if win:
            return win
        return False

    def DrawFigures(self):
        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                if self.board[row][col] == 1:
                    self.DrawX(row, col)
                elif self.board[row][col] == 2:
                    self.DrawO(row, col)

    def DrawX(self, row, col):
        pygame.draw.line(
            self.screen,
            self.RED,
            (col * 200 + self.SPACE, row * 200 + 200 - self.SPACE),
            (col * 200 + 200 - self.SPACE, row * 200 + self.SPACE),
            self.CROSS_WIDTH,
        )
        pygame.draw.line(
            self.screen,
            self.RED,
            (col * 200 + self.SPACE, row * 200 + self.SPACE),
            (col * 200 + 200 - self.SPACE, row * 200 + 200 - self.SPACE),
            self.CROSS_WIDTH,
        )

    def DrawO(self, row, col):
        pygame.draw.circle(
            self.screen, self.BLUE, (int(col * 200 + 100), int(row * 200 + 100)), self.CIRCLE_RADIUS, self.CIRCLE_WIDTH
        )

    def Start(self):
        while True:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX = event.pos[0]
                    mouseY = event.pos[1]
                    clicked_row = int(mouseY // 200)
                    clicked_col = int(mouseX // 200)
                    if self.AvaialbleSquares(clicked_row, clicked_col):
                        if self.player == 1:
                            self.MarkSquare(clicked_row, clicked_col, 1)
                            self.player = 2
                        elif self.player == 2:
                            self.MarkSquare(clicked_row, clicked_col, 2)
                            self.player = 1

            for player in range(1, 3):
                if self.CheckWiner(player):
                    print(f"Player {player} won")
                    pygame.quit()
                    sys.exit()
                elif self.IsBoardFull():
                    print("Draw")
                    pygame.quit()
                    sys.exit()

game = TikTakToe()
game.Start()
