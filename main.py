import time
import pygame
from backtracking import BackTracking
from button import Button
import field
from dfs import DFS
from field import Board, create_field

pygame.init()


initial_field = Board()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.SysFont(None, 24)

DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)


START_X = 128
START_Y = 128
GAP = 8
SIZE = 64
BUTTON_GAP = GAP


back = BackTracking()
dfs = DFS()
dfs_button = Button('DFS')
backtrack_button = Button('Backtrack')
reset_button = Button('Reset')
buttons = [dfs_button, backtrack_button, reset_button]

ready_field = []
for row in initial_field.board:
    for cell in row:
        if cell.value == 0:
            ready_field.append(cell)


def events(board: Board):
    cursor_x, cursor_y = pygame.mouse.get_pos()
    if backtrack_button.is_under_cursor(cursor_x, cursor_y):
        a = time.time()
        print("Can I solve it? -",
              back.back_tracking(ready_field, 0, initial_field, draw_board))
        print("Count of steps ", back.step)
        b = time.time()
        print("Time to solve it : ", b-a)
        back.step = 0
    elif dfs_button.is_under_cursor(cursor_x, cursor_y):
        a = time.time()
        print("Can I solve it? -",
              dfs.dfs(ready_field, 0, initial_field, draw_board))
        print("Count of steps ", dfs.step)
        b = time.time()
        print("Time to solve it : ", b-a)
        dfs.step = 0
    elif reset_button.is_under_cursor(cursor_x, cursor_y):
        board.load_next_field()
        ready_field.clear()
        for row in initial_field.board:
            for cell in row:
                if cell.value == 0:
                    ready_field.append(cell)


def handle(board: Board):
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            events(board)
        if event.type == pygame.QUIT:
            return True


def update_game(board: Board):
    game_exit = handle(board)
    if game_exit:
        return True
    draw_board(board)
    return False


def draw_button(button: Button):
    pygame.draw.rect(screen, DARK_GRAY if button.is_disabled else GREEN, pygame.Rect(
        button.left, button.top, button.width, button.height), 2)
    text = font.render(button.text, True, GREEN)
    text_left = button.left + button.width / 2 - text.get_size()[0] / 2
    text_top = button.top + button.height / 2 - text.get_size()[1] / 2
    screen.blit(text, (text_left, text_top))


def draw_board(board: Board):
    screen.fill(DARK_GRAY)
    for i, row in enumerate(board.board):
        for j, cell in enumerate(row):
            cell = row[j]
            pos_x = START_X + (GAP + SIZE) * j
            pos_y = START_Y + (GAP + SIZE) * i
            if type(cell) is not field.SumCell and cell.value == -1:
                pygame.draw.rect(screen, LIGHT_GRAY, pygame.Rect(
                    pos_x, pos_y, SIZE, SIZE), 0)
            elif type(cell) is not field.SumCell:
                pygame.draw.rect(screen, BLACK, pygame.Rect(
                    pos_x, pos_y, SIZE, SIZE), 0)
                img = font.render(str(cell.value), True, WHITE)
                screen.blit(img, (pos_x + SIZE / 2 - img.get_size()
                            [0] / 2, pos_y + SIZE / 2 - img.get_size()[1] / 2))
            else:
                img = font.render(str(cell.value), True, GREEN)
                pygame.draw.rect(screen, GREEN, pygame.Rect(
                    pos_x, pos_y, SIZE, SIZE), 2)
                pygame.draw.line(screen, GREEN, (pos_x, pos_y),
                                 (pos_x + SIZE - 1, pos_y + SIZE - 1))
                if cell.direction == field.DIRECTION_DOWN:
                    screen.blit(img, (pos_x + SIZE / 4 - img.get_size()
                                [0] / 2, pos_y + SIZE / 4 * 3 - img.get_size()[1] / 2))
                else:
                    screen.blit(img, (pos_x + SIZE / 4 * 3 - img.get_size()
                                [0] / 2, pos_y + SIZE / 4 - img.get_size()[1] / 2))
    for button in buttons:
        draw_button(button)
    pygame.time.delay(0)
    pygame.event.pump()
    pygame.display.flip()


def main():
    for i, button in enumerate(buttons):
        button.left = START_X + 500
        button.width = 140
        button.height = SIZE
        button_y = START_Y + (SIZE + BUTTON_GAP) * i
        button.top = button_y
    game = True
    while game:
        event = update_game(initial_field)
        if event:
            game = False
    pygame.quit()


if __name__ == '__main__':
    main()
