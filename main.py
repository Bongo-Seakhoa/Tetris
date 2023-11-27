import pygame
import random

# Tetris shapes
tetris_shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]]
]

shape_colors = {
    1: (255, 0, 0),    # Red
    2: (0, 255, 0),    # Green
    3: (0, 0, 255),    # Blue
    4: (255, 255, 0),  # Yellow
    5: (255, 0, 255),  # Magenta
    6: (0, 255, 255),  # Cyan
    7: (255, 165, 0)   # Orange
}

# Initialize the game
def create_board():
    return [[0 for _ in range(10)] for _ in range(20)]

def join_matrixes(mat1, mat2, mat2_off):
    off_x, off_y = mat2_off
    for y in range(len(mat2)):
        for x in range(len(mat2[y])):
            if mat2[y][x] != 0:
                mat1[y + off_y - 1][x + off_x] = mat2[y][x]
    return mat1

def check_collision(board, shape, offset):
    off_x, off_y = offset
    for y in range(len(shape)):
        for x in range(len(shape[y])):
            if shape[y][x] != 0:
                if y + off_y >= len(board) or \
                        x + off_x < 0 or x + off_x >= len(board[0]) or \
                        board[y + off_y][x + off_x] != 0:
                    return True
    return False

def rotate_shape(shape):
    return [ [ shape[y][x]
               for y in range(len(shape)) ]
             for x in range(len(shape[0]) - 1, -1, -1) ]

def new_piece():
    shape = random.choice(tetris_shapes)
    return {'shape': shape,
            'rotation': 0,
            'x': 5 - len(shape[0]) // 2,
            'y': 0}

def remove_row(board, row):
    del board[row]
    return [[0 for _ in range(10)]] + board

def check_rows(board):
    rows_to_remove = [i for i, row in enumerate(board) if 0 not in row]
    for row in rows_to_remove:
        board = remove_row(board, row)
    return len(rows_to_remove), board

# Pygame initialization
pygame.init()
width, height = 300, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption("Tetris")

# Game variables
board = create_board()
piece = new_piece()
score = 0
fall_time = 0
fall_speed = 0.5

# Home screen variables
show_home_screen = True

#Score
score = 0
font = pygame.font.Font(None, 36)

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))

    # Display score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 10))


    if show_home_screen:
        # Display home screen text
        font = pygame.font.Font(None, 36)
        play_text = font.render("Press P to Play", True, (255, 255, 255))
        high_scores_text = font.render("Press H for High Scores", True, (255, 255, 255))
        screen.blit(play_text, (80, 200))
        screen.blit(high_scores_text, (40, 250))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    show_home_screen = False  # Start the game
                elif event.key == pygame.K_h:
                    # Display high scores (add functionality here if you have high scores)
                    pass

    else:

        # Handling user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    piece['x'] -= 1
                    if check_collision(board, piece['shape'], (piece['x'], piece['y'])):
                        piece['x'] += 1
                elif event.key == pygame.K_RIGHT:
                    piece['x'] += 1
                    if check_collision(board, piece['shape'], (piece['x'], piece['y'])):
                        piece['x'] -= 1
                elif event.key == pygame.K_DOWN:
                    piece['y'] += 1
                    if check_collision(board, piece['shape'], (piece['x'], piece['y'])):
                        piece['y'] -= 1
                elif event.key == pygame.K_SPACE:
                    piece['rotation'] = (piece['rotation'] + 1) % len(piece['shape'])
                    rotated_shape = rotate_shape(piece['shape'])
                    if not check_collision(board, rotated_shape, (piece['x'], piece['y'])):
                        piece['shape'] = rotated_shape

    # Falling piece logic
    fall_time += clock.get_rawtime()
    if fall_time / 1000 >= fall_speed:
        fall_time = 0
        piece['y'] += 1
        if check_collision(board, piece['shape'], (piece['x'], piece['y'])):
            board = join_matrixes(board, piece['shape'], (piece['x'], piece['y']))
            num_rows_removed, board = check_rows(board)
            score += num_rows_removed * 100
            piece = new_piece()

    # Drawing the board
    for y, row in enumerate(board):
        for x, val in enumerate(row):
            if val != 0:
                pygame.draw.rect(screen, (255, 255, 255), (x * 30, y * 30, 30, 30))

    # Drawing the current piece
    for y, row in enumerate(piece['shape']):
        for x, val in enumerate(row):
            if val != 0:
                pygame.draw.rect(screen, shape_colors[val], ((piece['x'] + x) * 30, (piece['y'] + y) * 30, 30, 30))
                
    pygame.display.update()
    clock.tick(60)

pygame.quit()
