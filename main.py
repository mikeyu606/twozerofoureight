import pygame
import random

pygame.init()

# initial set up
WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 24)

# 2048 game color library
colors = {0: (204, 192, 179),
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'other': (0, 0, 0),
          'bg': (187, 173, 160)}

# game variables initialize
score = 0
board_values = [[0 for _ in range(4)] for _ in range(4)]
spawn_new = True
init_count = 0
direction = ''

file = open('high_score.txt', 'r')
init_high = int(file.readline())
file.close()
high_score = init_high


# draw game over and restart text
def draw_over():
    pygame.draw.rect(screen, 'black', [50, 50, 300, 100], 0, 10)
    game_over_text1 = font.render('Game Over!', True, 'white')
    game_over_text2 = font.render('Press Enter to Restart', True, 'white')
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))


# Check if there are any valid moves left on the board
def is_game_over(board):
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return False
            if j > 0 and board[i][j] == board[i][j - 1]: # adjacent tiles to its left in row i
                return False
            if j < 3 and board[i][j] == board[i][j + 1]: # adjacent tiles to its right in row i
                return False
            if i > 0 and board[i][j] == board[i - 1][j]: #adjacent tiles at the top in col j
                return False
            if i < 3 and board[i][j] == board[i + 1][j]: #adjacent tiles at the bottom in col j
                return False
    return True


# take your turn based on direction
def take_turn(direction, board):
    global score
    merged = [[False for _ in range(4)] for _ in range(4)]

    if direction == 'UP':
        for j in range(4):  # columns
            for i in range(1, 4):  # rows (start from 1, not 0, since no cell above row 0)
                if board[i][j] == 0:
                    continue

                row_above = i - 1  # holds the position of the row above the current tile
                while row_above >= 0 and board[row_above][j] == 0:  # skips the 0 rows
                    row_above -= 1

                if row_above == -1:  # if, Move the cell to the topmost position
                    board[0][j] = board[i][j]
                    board[i][j] = 0
                elif board[row_above][j] == board[i][j] and not merged[row_above][j] and not merged[i][j]:
                    board[row_above][j] *= 2
                    score += board[row_above][j]
                    board[i][j] = 0
                    merged[row_above][j] = True
                elif row_above + 1 != i:  # checks if there is an 0 tile between current tile and the tile above it
                    board[row_above + 1][j] = board[i][j]
                    board[i][j] = 0

    elif direction == 'DOWN':
        for j in range(4):  # columns
            for i in range(2, -1, -1):  # rows (start from 2, not 3, since no cell below row 3)
                # this row also iterates through the entire column so checks for 0 after merges
                if board[i][j] == 0:
                    continue

                row_below = i + 1
                while row_below < 4 and board[row_below][
                    j] == 0:  # row_below is the index where a tile is or the border
                    row_below += 1

                if row_below == 4:  # Move the cell to the bottommost position
                    board[3][j] = board[i][j]
                    board[i][j] = 0
                elif board[row_below][j] == board[i][j] and not merged[row_below][j] and not merged[i][j]:
                    board[row_below][j] *= 2
                    score += board[row_below][j]
                    board[i][j] = 0
                    merged[row_below][j] = True
                elif row_below - 1 != i:
                    board[row_below - 1][j] = board[i][j]
                    board[i][j] = 0

    elif direction == 'LEFT':
        for i in range(4):  # rows
            for j in range(1, 4):  # columns (start from 1, not 0, since no cell to the left of column 0)
                if board[i][j] == 0:
                    continue

                left_cell = j - 1
                while left_cell >= 0 and board[i][left_cell] == 0:  # Skip the 0 cells to the left
                    left_cell -= 1

                if left_cell == -1:  # Move the cell to the leftmost position
                    board[i][0] = board[i][j]
                    board[i][j] = 0
                elif board[i][left_cell] == board[i][j] and not merged[i][left_cell] and not merged[i][j]:
                    board[i][left_cell] *= 2
                    score += board[i][left_cell]
                    board[i][j] = 0
                    merged[i][left_cell] = True
                elif left_cell + 1 != j:  # Checks if there is a 0 cell between the current cell and the cell to the left
                    board[i][left_cell + 1] = board[i][j]
                    board[i][j] = 0


    elif direction == 'RIGHT':
        for i in range(4):
            for j in range(2, -1, -1):  # cols start from 2 because 3 is the far right
                if board[i][j] == 0:
                    continue
                right_cell = j + 1
                while right_cell < 4 and board[i][right_cell] == 0:
                    right_cell += 1

                if right_cell == 4:
                    board[i][3] = board[i][j]
                    board[i][j] = 0
                elif board[i][right_cell] == board[i][j] and not merged[i][right_cell] and not merged[i][j]:
                    board[i][right_cell] *= 2
                    score += board[i][right_cell]
                    board[i][j] = 0
                    merged[i][right_cell] = True
                elif right_cell - 1 != j:
                    board[i][right_cell - 1] = board[i][j]
                    board[i][j] = 0
    return board


# spawn in new pieces randomly when turns start
def new_pieces(board):
    count = 0  # this variable keeps track of how many new tiles were created
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1  # indicates that a new tile was created
            # sets the value of the board to either 4 or 2
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2

    return board


# draw the background for the board
def draw_board():
    pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
    score_text = font.render(f'Score: {score}', True, 'black')
    high_score_text = font.render(f'High Score: {high_score}', True, 'black')
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))


def get_tile_color(value):
    if value > 8:
        return colors['light text']
    else:
        return colors['dark text']


def calculate_center_position(row, column):  # returns the center position of the tile
    x = column * 95 + 57
    y = row * 95 + 57
    return x, y


def draw_pieces(board):  # this method iterates over all of the value_board and then creates the tiles with respect to the values within the array
    flattened_board = [value for row in board for value in row]

    # iterate over all the tiles on the board
    for index, value in enumerate(flattened_board):
        row = index // 4  # since it is a 4 by 4 ex tile 13 / 4 will return row index 3
        column = index % 4

        color = colors[value] if value <= 2048 else colors[
            'other']  # Get the color associated with the current tile value from the colors dictionary
        pygame.draw.rect(screen, color, [column * 95 + 20, row * 95 + 20, 75, 75], 0,
                         5)  # Draw the colored rectangle representing the tile on the game board

        if value > 0:  # draws the value of the tile on top of the game board
            value_len = len(str(value))
            font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
            value_color = get_tile_color(value)
            value_text = font.render(str(value), True, value_color)
            center_x, center_y = calculate_center_position(row, column)
            text_rect = value_text.get_rect(center=(center_x, center_y))
            screen.blit(value_text, text_rect)
            pygame.draw.rect(screen, 'black', [column * 95 + 20, row * 95 + 20, 75, 75], 2, 5)  # Draw a black border
            # around the colored rectangle to visually separate adjacent tiles


# main game loop, when run = F then terminate
run = True
while run:
    timer.tick(fps)
    screen.fill('gray')
    draw_board()
    draw_pieces(board_values) # draw the board everytime with new values

    # spawns in pieces before merging and moving tiles
    if spawn_new or init_count < 2:
        board_values = new_pieces(board_values)
        spawn_new = False
        init_count += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = 'UP'
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'

    if direction != '':  # runs take_turn to merge or move take_turn
        board_values = take_turn(direction, board_values)  # change the values of the tiles after merging and shifting
        direction = ''
        spawn_new = True

    if is_game_over(board_values):
        draw_over()
        if high_score > init_high:
            file = open('high_score.txt', 'w')
            file.write(f'{high_score}')
            file.close()
            init_high = high_score

    if score > high_score:
        high_score = score

    pygame.display.flip()
pygame.quit()
