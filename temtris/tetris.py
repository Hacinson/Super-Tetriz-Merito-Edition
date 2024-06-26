import pygame
import random

# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
screen_width = 800
screen_height = 700
play_width = 300  # 300 // 10 = 30 szerokość bloków
play_height = 600  # 600 // 20 = 20 wysokość bloków
block_size = 30

top_left_x = (screen_width - play_width) // 2
top_left_y = screen_height - play_height - 50

# Definicje kształtów
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

# Klasa definiująca kształty
class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for x in range(10)] for y in range(20)]
    
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in locked_positions:
                c = locked_positions[(x, y)]
                grid[y][x] = c
    return grid

def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]
    
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))
    
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    
    return positions

def valid_space(piece, grid):
    accepted_positions = [[(x, y) for x in range(10) if grid[y][x] == (0, 0, 0)] for y in range(20)]
    accepted_positions = [x for row in accepted_positions for x in row]
    
    formatted = convert_shape_format(piece)
    
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(text, size, color, surface):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    label = font.render(text, True, color)
    
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 
                         top_left_y + play_height / 2 - (label.get_height() / 2)))

def draw_grid(surface, grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x], 
                             (top_left_x + x * block_size, top_left_y + y * block_size, block_size, block_size), 0)
    
    draw_grid_lines(surface, grid)

def draw_grid_lines(surface, grid):
    for y in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (top_left_x, top_left_y + y * block_size), (top_left_x + play_width, top_left_y + y * block_size))
    for x in range(len(grid[0])):
        pygame.draw.line(surface, (128, 128, 128), (top_left_x + x * block_size, top_left_y), (top_left_x + x * block_size, top_left_y + play_height))

def clear_rows(grid, locked):
    increment = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            increment += 1
            ind = i
            for x in range(len(row)):
                try:
                    del locked[(x, i)]
                except:
                    continue
    
    if increment > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + increment)
                locked[newKey] = locked.pop(key)
    
    return increment

def draw_next_shape(piece, surface):
    font = pygame.font.Font(pygame.font.get_default_font(), 30)
    label = font.render('Next Shape', True, (255, 255, 255))
    
    start_x = top_left_x + play_width + 50
    start_y = top_left_y + (play_height / 2 - 100)
    
    format = piece.shape[piece.rotation % len(piece.shape)]
    
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, piece.color, 
                                 (start_x + j * block_size, start_y + i * block_size, block_size, block_size), 0)
    
    surface.blit(label, (start_x + 10, start_y - 30))

def draw_window(surface, grid, score=0):
    background_image = pygame.image.load('data/background.jpg')
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
    surface.blit(background_image, (0, 0))
    
    font = pygame.font.Font(pygame.font.get_default_font(), 60)
    label = font.render('Merito Tetris :3', True, (255, 255, 255))
    
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))
    
    font = pygame.font.Font(pygame.font.get_default_font(), 30)
    label = font.render('Score: ' + str(score), True, (255, 255, 255))
    
    start_x = top_left_x + play_width + 50
    start_y = top_left_y + play_height / 2 - 100
    
    surface.blit(label, (start_x + 20, start_y + 160))
    
    draw_grid(surface, grid)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

def main():
    pygame.mixer.init()
    pygame.mixer.music.stop()
    pygame.mixer.music.load('data/theme.mp3')
    pygame.mixer.music.play(-1)
    locked_positions = {}
    grid = create_grid(locked_positions)
    
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    level_time = 0
    down_time = 0
    down_pressed = False
    score = 0
    
    while run:
        grid = create_grid(locked_positions)
        fall_speed = 0.27
        down_speed = 0.05
        
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        down_time += clock.get_rawtime()
        clock.tick()
        
        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005
        
        # Zwykłe spadanie bloku
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
        
        # Przyspieszone spadanie bloku przy trzymaniu klawisza w dół
        if down_pressed and down_time / 1000 >= down_speed:
            down_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
                change_piece = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    down_pressed = True
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    down_pressed = False
        
        shape_pos = convert_shape_format(current_piece)
        
        for pos in shape_pos:
            x, y = pos
            if y > -1:
                grid[y][x] = current_piece.color
        
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10
        
        draw_window(win, grid, score)
        draw_next_shape(next_piece, win)
        pygame.display.update()
        
        if check_lost(locked_positions):
            run = False
            pygame.mixer.music.stop()
            game_over_sound = pygame.mixer.Sound('data/gameover.mp3')
            game_over_sound.play()
            game_over_image = pygame.image.load('data/gameover.png')
            win.blit(game_over_image, (top_left_x + play_width / 2 - game_over_image.get_width() / 2, top_left_y + play_height / 2 - game_over_image.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(2000)

    pygame.display.update()
    pygame.time.delay(2000)

def main_menu():
    run = True
    while run:
        #menu_image = pygame.image.load('data/menu.jpg')
        #win.blit(menu_image, (top_left_x + play_width / 2 - menu_image.get_width() / 2, top_left_y + play_height / 2 - menu_image.get_height() / 2))
        win.fill((0, 0, 0))
        draw_text_middle('Press Any Key To Play', 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
    pygame.display.quit()

win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Super Merito Tetris 4000')
main_menu()
