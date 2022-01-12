import collections
import copy
import random
import sys
import time
import pygame
from pygame.locals import *
import a_star_solver as astar

CLOCK = pygame.time.Clock()
HEIGHT, WIDTH = 800, 1000

BG_COLOR = (125, 107, 145)
TEXT_COLOR = (39, 40, 56)
RECT_COLOR = (152, 159, 206)
START_COLOR = (124, 252, 0)
END_COLOR = (220, 20, 60)
PATH_COLOR = (197, 231, 226)
PATH_COLOR2 = (250, 231, 226)
GRAY_COLOR = (220, 220, 220)
HISTORY_COLOR = (54, 1, 103)
OPEN_CELL_COLOR = (100, 150, 35)
HISTORY_COLOR2 = (251, 140, 171)

ITERATIE_ANIMATIE = 0
LUNGIME_ANIMATIE = 0


pygame.init()
pygame.display.set_caption('Maze Game')
screen = pygame.display.set_mode((WIDTH, HEIGHT))

font100 = pygame.font.SysFont(None, 100)
font32 = pygame.font.SysFont(None, 32)
font20 = pygame.font.SysFont(None, 20)


def load_maze_data(file):
    maze_temp = []
    with open(file) as m:
        d = m.readline()
        while d:
            maze_temp.append([int(c) for c in d if c.isdigit()])
            d = m.readline()
    return maze_temp


maze1_data = load_maze_data('maze1.txt')
maze2_data = load_maze_data('maze2.txt')


def draw_text(text, font, color, surface, x, y):
    text_object = font.render(text, 1, color)
    text_rectangle = text_object.get_rect(center=(x, y))
    surface.blit(text_object, text_rectangle)
    return text_rectangle


def main_menu():
    rec_size = (300, 50)

    click = False
    while True:

        screen.fill(BG_COLOR)
        draw_text('Maze Game', font100, TEXT_COLOR, screen, WIDTH // 2, HEIGHT // 6)

        mx, my = pygame.mouse.get_pos()

        draw_text('Draw Maze', font32, TEXT_COLOR, screen, WIDTH // 2, HEIGHT // 6 + 3.5 * rec_size[1])
        button_draw_maze = pygame.Rect(WIDTH // 2 - rec_size[0] // 2, HEIGHT // 6 + 3 * rec_size[1], rec_size[0],
                                       rec_size[1])

        draw_text('Credits', font32, TEXT_COLOR, screen, WIDTH // 2, HEIGHT // 6 + 5.5 * rec_size[1])
        button_credits = pygame.Rect(WIDTH // 2 - rec_size[0] // 2, HEIGHT // 6 + 5 * rec_size[1], rec_size[0],
                                     rec_size[1])

        if button_draw_maze.collidepoint((mx, my)):
            if click:
                draw_maze()
        elif button_credits.collidepoint((mx, my)):
            if click:
                menu_credits()

        pygame.draw.rect(screen, RECT_COLOR, button_draw_maze, 1)
        pygame.draw.rect(screen, RECT_COLOR, button_credits, 1)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        CLOCK.tick(60)


def menu_credits():
    running = True

    while running:
        screen.fill(BG_COLOR)
        draw_text('Proiect Inteligenta Artificiala 2022 @UAIC', font32, TEXT_COLOR, screen, WIDTH // 2, HEIGHT // 6)
        draw_text('Grupa 3A2', font32, TEXT_COLOR, screen, WIDTH // 2, HEIGHT // 5.2)
        draw_text('Maze Game', font100, TEXT_COLOR, screen, WIDTH // 2, HEIGHT // 4)
        draw_text('Croitoru Razvan', font100, (8, 96, 95), screen, WIDTH // 2, HEIGHT // 2.5)
        draw_text('Barat Narcis', font100, (23, 126, 137), screen, WIDTH // 2, HEIGHT // 2.05)
        draw_text('Vasilica Alex', font100, (89, 131, 129), screen, WIDTH // 2, HEIGHT // 1.7)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        CLOCK.tick(60)


def drawGridLegend():
    """
    Draws function legend in the upper left corner with instructions on how to draw every type of block
    """
    blockSize = 15
    cx, cy = 50, 50
    empty = pygame.Rect(cx, cy, blockSize, blockSize)
    pygame.draw.rect(screen, RECT_COLOR, empty, 1)
    draw_text('Empty     Hold right click to draw', font20, TEXT_COLOR, screen, cx + 60, cy + 7)
    wall = pygame.Rect(cx, cy + 2 * blockSize, blockSize, blockSize)
    pygame.draw.rect(screen, RECT_COLOR, wall, 0)
    draw_text('Wall      Hold left click to draw', font20, TEXT_COLOR, screen, cx + 60, cy + 2 * blockSize + 7)
    start = pygame.Rect(cx, cy + 4 * blockSize, blockSize, blockSize)
    pygame.draw.rect(screen, START_COLOR, start, 0)
    draw_text('Start       Hold LCtrl + left click to draw', font20, TEXT_COLOR, screen, cx + 80,
              cy + 4 * blockSize + 7)
    end = pygame.Rect(cx, cy + 6 * blockSize, blockSize, blockSize)
    pygame.draw.rect(screen, END_COLOR, end, 0)
    draw_text('End        Hold LCtrl + right click to draw', font20, TEXT_COLOR, screen, cx + 85,
              cy + 6 * blockSize + 7)


def drawGrid(grid, start, end, path, h, h2):
    """
    Given a maze, a start point, an end point and a path, it draws the corresponding blocks on the maze
    """
    order = {}
    global ITERATIE_ANIMATIE
    if path:  # Generate order for every element in path to calculate gradient
        for idx, x in enumerate(path):
            order[x] = idx

    if path:  # Generate gradient for path
        diff = (PATH_COLOR2[0] - PATH_COLOR[0]) / len(path)

    if h:  # Generate gradient for current searched cell
        if LUNGIME_ANIMATIE:
            gradient_animatie = int((HISTORY_COLOR2[0] - HISTORY_COLOR[0]) / LUNGIME_ANIMATIE * ITERATIE_ANIMATIE)
            gradient_animatie2 = int((HISTORY_COLOR2[1] - HISTORY_COLOR[1]) / LUNGIME_ANIMATIE * ITERATIE_ANIMATIE)
            gradient_animatie3 = int((HISTORY_COLOR2[2] - HISTORY_COLOR[2]) / LUNGIME_ANIMATIE * ITERATIE_ANIMATIE)
        else:
            gradient_animatie = 0
            gradient_animatie2 = 0
            gradient_animatie3 = 0

        culoare_animatie = (HISTORY_COLOR[0] + gradient_animatie, HISTORY_COLOR[1] + gradient_animatie2, HISTORY_COLOR[2] + gradient_animatie3)

    drawGridLegend()
    blockSize = 15  # Set the size of the grid block
    cx, cy = WIDTH // 2 - len(grid) * blockSize // 2, HEIGHT // 1.65 - len(grid[0]) * blockSize // 2  # Generate offset so maze is always centered
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            rect = pygame.Rect(cx + x * blockSize, cy + y * blockSize, blockSize, blockSize)
            if (x, y) == start:  # Draw start block
                pygame.draw.rect(screen, START_COLOR, rect, 0)
            elif (x, y) == end:  # Draw end block
                pygame.draw.rect(screen, END_COLOR, rect, 0)
            elif not h and path and (x, y) in path:  # Draw path block
                pygame.draw.rect(screen, (PATH_COLOR[0] + int(order[x, y] * diff), PATH_COLOR[1], PATH_COLOR[2]), rect, 0)
            elif h and (x, y) in h[0]:  # Draw block from open list
                pygame.draw.rect(screen, OPEN_CELL_COLOR, rect, 0)
            elif h2 and (x, y) in h2:  # Draw block from closed list
                pygame.draw.rect(screen, h2[x, y], rect, 0)
            else:  # Draw normal block (wall / empty)
                pygame.draw.rect(screen, RECT_COLOR, rect, grid[x][y])

    if h:
        for i in h[0]:
            h2[i] = culoare_animatie  # Store nodes from open list in closed list with their color
        if len(h) == 1:
            for i in h[0]:
                del h2[i]
        del h[0]
        ITERATIE_ANIMATIE += 1


def getRectangleClicked(len1, len2, mx, my):
    """
    Returns the block in the grid that the mouse is over at that moment
    """
    blockSize = 15
    cx, cy = WIDTH // 2 - len1 * blockSize // 2, HEIGHT // 1.65 - len2 * blockSize // 2
    x_res = (mx - cx) // blockSize
    y_res = (my - cy) // blockSize
    if 0 <= x_res < len1 and 0 <= y_res < len2:
        return int(x_res), int(y_res)
    return None, None


def draw_maze():
    """
    Main function that runs the Draw Maze submenu
    """
    global LUNGIME_ANIMATIE, ITERATIE_ANIMATIE
    size_x, size_y = 50, 40  # Default maze shape
    start, end = None, None  # Start and end points for maze
    drawn_grid = [[1 for _ in range(size_y)] for _ in range(size_x)]  # Maze
    path, path_drawn = [], False
    distance_type = 1
    history, history2 = [], {}
    deactivate_mouse = False
    running = True

    while running:
        screen.fill(BG_COLOR)  # Set the background color
        mx, my = pygame.mouse.get_pos()

        if not history and not deactivate_mouse:  # Check if the animation has finished
            if pygame.mouse.get_pressed()[0]:  # Check if left click is pressed
                rx, ry = getRectangleClicked(len(drawn_grid), len(drawn_grid[0]), mx, my)  # Get block under mouse
                if rx is not None and ry is not None:
                    if pygame.key.get_pressed()[pygame.K_LCTRL]:  # If Ctrl is pressed, set the start point
                        if start:
                            drawn_grid[start[0]][start[1]] = 1
                        start = (rx, ry)
                        if start and end and path_drawn:
                            path, history = astar.astar(copy.deepcopy(drawn_grid), start, end, distance_type)  # Dinamically generate the maze on start point update
                            history2 = {}
                            LUNGIME_ANIMATIE, ITERATIE_ANIMATIE = len(history), 0
                            path_drawn, deactivate_mouse = True, True
                    elif start != (rx, ry) and end != (rx, ry):
                        drawn_grid[rx][ry] = 0  # Set the block under the mouse as a wall

            elif pygame.mouse.get_pressed()[2]:  # Check if right click is pressed
                rx, ry = getRectangleClicked(len(drawn_grid), len(drawn_grid[0]), mx, my)  # Get block under mouse
                if rx is not None and ry is not None:
                    if pygame.key.get_pressed()[pygame.K_LCTRL]:  # If Ctrl is pressed, set the end point
                        if end is not None:
                            drawn_grid[end[0]][end[1]] = 1
                        end = (rx, ry)
                        if start and end and path_drawn:
                            path, history = astar.astar(copy.deepcopy(drawn_grid), start, end, distance_type)  # Dinamically generate the maze on end point update
                            history2 = {}
                            LUNGIME_ANIMATIE,ITERATIE_ANIMATIE = len(history), 0
                            path_drawn, deactivate_mouse = True, True
                    elif end != (rx, ry) and start != (rx, ry):
                        drawn_grid[rx][ry] = 1  # Set the block under the mouse as empty

        drawGrid(drawn_grid, start, end, path, history, history2)  # Draw the maze grid
        if not history:  # If the animation has finished, reactivate the mouse
            deactivate_mouse = False

        # Draw title
        draw_text('Draw Maze', font100, TEXT_COLOR, screen, WIDTH // 2, HEIGHT // 10 - 45)

        # Draw maze 1 example button
        draw_text('Maze 1', font32, TEXT_COLOR, screen, 390, 155)
        maze1_button = pygame.Rect(340, 135, 100, 40)
        maze1_button = pygame.draw.rect(screen, PATH_COLOR2, maze1_button, 1)

        # Draw maze 2 example button
        draw_text('Maze 2', font32, TEXT_COLOR, screen, 580, 155)
        maze2_button = pygame.Rect(530, 135, 100, 40)
        maze2_button = pygame.draw.rect(screen, PATH_COLOR2, maze2_button, 1)

        # Draw buttons to change maze size and maze size text
        draw_text(str(size_x), font100, TEXT_COLOR, screen, 390, 95)
        draw_text(str(size_y), font100, TEXT_COLOR, screen, 580, 95)
        lower_1 = pygame.draw.polygon(screen, RECT_COLOR, points=[(310, 95), (335, 70), (335, 120)])
        higher_1 = pygame.draw.polygon(screen, RECT_COLOR, points=[(470, 95), (445, 70), (445, 120)])
        lower_2 = pygame.draw.polygon(screen, RECT_COLOR, points=[(500, 95), (525, 70), (525, 120)])
        higher_2 = pygame.draw.polygon(screen, RECT_COLOR, points=[(660, 95), (635, 70), (635, 120)])

        # Draw reset button
        draw_text('Reset Maze', font32, TEXT_COLOR, screen, WIDTH // 2 + 350, HEIGHT // 10 - 50)
        button_reset_maze = pygame.Rect(WIDTH // 2 + 250, HEIGHT // 10 - 25 - 50, 200, 50)
        button_reset_maze = pygame.draw.rect(screen, END_COLOR, button_reset_maze, 1)

        # Draw euclidian distance button
        draw_text('Euclidian', font20, TEXT_COLOR, screen, WIDTH // 2 + 295, HEIGHT // 10)
        draw_text('Distance', font20, TEXT_COLOR, screen, WIDTH // 2 + 295, HEIGHT // 10 + 20)
        button_euclidian = pygame.Rect(WIDTH // 2 + 250, HEIGHT // 10 - 25 + 60 - 50, 90, 50)
        if distance_type == 0:
            button_euclidian = pygame.draw.rect(screen, START_COLOR, button_euclidian, 5)
        else:
            button_euclidian = pygame.draw.rect(screen, GRAY_COLOR, button_euclidian, 1)

        # Draw manhattan distance button
        draw_text('Manhattan', font20, TEXT_COLOR, screen, WIDTH // 2 + 405, HEIGHT // 10)
        draw_text('Distance', font20, TEXT_COLOR, screen, WIDTH // 2 + 405, HEIGHT // 10 + 20)
        button_manhattan = pygame.Rect(WIDTH // 2 + 360, HEIGHT // 10 - 25 + 60 - 50, 90, 50)
        if distance_type == 1:
            button_manhattan = pygame.draw.rect(screen, START_COLOR, button_manhattan, 5)
        else:
            button_manhattan = pygame.draw.rect(screen, GRAY_COLOR, button_manhattan, 1)

        # Draw solve button
        draw_text('Solve Maze', font32, TEXT_COLOR, screen, WIDTH // 2 + 350, HEIGHT // 10 + 70)
        button_solve_maze = pygame.Rect(WIDTH // 2 + 250, HEIGHT // 10 - 25 + 70, 200, 50)
        button_solve_maze = pygame.draw.rect(screen, START_COLOR, button_solve_maze, 1)

        # If the animation has finished, display the path length / error mesage
        if path_drawn:
            if not history:
                if not path:
                    draw_text('No path found', font32, END_COLOR, screen, 100, 25)
                else:
                    draw_text(f'Path length is {len(path)}', font32, START_COLOR, screen, 100, 25)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Handle logic for button presses
                    if lower_1.collidepoint((mx, my)):  # Lower x size
                        if size_x > 3:
                            size_x -= 1
                            drawn_grid.pop()
                    elif higher_1.collidepoint((mx, my)):  # Raise x size
                        if size_x < 50:
                            size_x += 1
                            drawn_grid.append([1 for i in range(size_y)])
                    elif lower_2.collidepoint((mx, my)):  # Lower y size
                        if size_y > 3:
                            for x in range(len(drawn_grid)):
                                drawn_grid[x].pop()
                            size_y -= 1
                    elif higher_2.collidepoint((mx, my)):  # Raise y size
                        if size_y < 40:
                            size_y += 1
                            for x in range(len(drawn_grid)):
                                drawn_grid[x].append(1)

                    elif button_reset_maze.collidepoint((mx, my)):  # Check if reset button is pressed
                        drawn_grid = [[1 for i in range(size_y)] for j in range(size_x)]  # Reset maze
                        path, path_drawn = [], False  # Reset solution path
                        start, end = None, None  # Reset start and end point
                        history, history2, LUNGIME_ANIMATIE, ITERATIE_ANIMATIE = [], {}, 0, 0  # Reset animation

                    elif button_solve_maze.collidepoint((mx, my)):  # Check if solve button is pressed
                        if start and end:
                            path, history = astar.astar(copy.deepcopy(drawn_grid), start, end, distance_type) # Generate path
                            history2, ITERATIE_ANIMATIE, LUNGIME_ANIMATIE = {}, 0, len(history)
                            path_drawn = True

                    elif button_euclidian.collidepoint((mx, my)):
                        distance_type = 0
                    elif button_manhattan.collidepoint((mx, my)):
                        distance_type = 1

                    elif maze1_button.collidepoint((mx, my)):  # Load maze 1 example
                        history, history2, ITERATIE_ANIMATIE, LUNGIME_ANIMATIE = [], {}, 0, 0
                        drawn_grid = copy.deepcopy(maze1_data)
                        size_x, size_y = len(maze1_data), len(maze1_data[0])
                        start, end = (0, 0), (39, 29)
                        path, path_drawn = [], False

                    elif maze2_button.collidepoint((mx, my)):
                        history, history2, ITERATIE_ANIMATIE, LUNGIME_ANIMATIE = [], {}, 0, 0
                        drawn_grid = copy.deepcopy(maze2_data)
                        size_x, size_y = len(maze2_data), len(maze2_data[0])
                        start, end = (0, 0), (21, 31)
                        path, path_drawn = [], False

        pygame.display.update()
        CLOCK.tick(60)


main_menu()
