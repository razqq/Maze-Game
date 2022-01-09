import copy
import sys
import pygame
from pygame.locals import *
import a_star_solver as astar

CLOCK = pygame.time.Clock()
HEIGHT, WIDTH = 800, 1000

pygame.init()
pygame.display.set_caption('Maze Game')
screen = pygame.display.set_mode((WIDTH, HEIGHT))

font100 = pygame.font.SysFont(None, 100)
font32 = pygame.font.SysFont(None, 32)
font20 = pygame.font.SysFont(None, 20)


def draw_text(text, font, color, surface, x, y):
    text_object = font.render(text, 1, color)
    text_rectangle = text_object.get_rect(center=(x, y))
    surface.blit(text_object, text_rectangle)
    return text_rectangle


BG_COLOR = (125, 107, 145)
TEXT_COLOR = (39, 40, 56)
RECT_COLOR = (152, 159, 206)
START_COLOR = (124, 252, 0)
END_COLOR = (220, 20, 60)
PATH_COLOR = (197, 231, 226)


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

        draw_text('Generate Maze', font32, TEXT_COLOR, screen, WIDTH // 2, HEIGHT // 6 + 5.5 * rec_size[1])
        button_generate_maze = pygame.Rect(WIDTH // 2 - rec_size[0] // 2, HEIGHT // 6 + 5 * rec_size[1], rec_size[0],
                                           rec_size[1])

        draw_text('Load Maze', font32, TEXT_COLOR, screen, WIDTH // 2, HEIGHT // 6 + 7.5 * rec_size[1])
        button_load_maze = pygame.Rect(WIDTH // 2 - rec_size[0] // 2, HEIGHT // 6 + 7 * rec_size[1], rec_size[0],
                                       rec_size[1])

        draw_text('Credits', font32, TEXT_COLOR, screen, WIDTH // 2, HEIGHT // 6 + 9.5 * rec_size[1])
        button_credits = pygame.Rect(WIDTH // 2 - rec_size[0] // 2, HEIGHT // 6 + 9 * rec_size[1], rec_size[0],
                                     rec_size[1])

        if button_draw_maze.collidepoint((mx, my)):
            if click:
                draw_maze()
        if button_generate_maze.collidepoint((mx, my)):
            if click:
                options()
        if button_load_maze.collidepoint((mx, my)):
            if click:
                pass

        pygame.draw.rect(screen, RECT_COLOR, button_draw_maze, 1)
        pygame.draw.rect(screen, RECT_COLOR, button_generate_maze, 1)
        pygame.draw.rect(screen, RECT_COLOR, button_load_maze, 1)
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


def drawGridLegend(grid):
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

    pass


def drawGrid(grid, start, end, path):
    drawGridLegend(grid)
    blockSize = 15  # Set the size of the grid block
    cx, cy = WIDTH // 2 - len(grid) * blockSize // 2, HEIGHT // 1.65 - len(grid[0]) * blockSize // 2
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            rect = pygame.Rect(cx + x * blockSize, cy + y * blockSize, blockSize, blockSize)
            if (x, y) == start:
                pygame.draw.rect(screen, START_COLOR, rect, 0)
            elif (x, y) == end:
                pygame.draw.rect(screen, END_COLOR, rect, 0)
            elif path and (x, y) in path:
                pygame.draw.rect(screen, PATH_COLOR, rect, 0)
            else:
                pygame.draw.rect(screen, RECT_COLOR, rect, grid[x][y])


def getRectangleClicked(grid, mx, my):
    blockSize = 15
    cx, cy = WIDTH // 2 - len(grid) * blockSize // 2, HEIGHT // 1.65 - len(grid[0]) * blockSize // 2
    x_res = (mx - cx) // blockSize
    y_res = (my - cy) // blockSize
    if 0 <= x_res < len(grid) and 0 <= y_res < len(grid[0]):
        return int(x_res), int(y_res)
    return None, None


def dfs(grid, node, end, visited):
    if node is None or end is None:
        return None
    print(node, end, node == end)

    visited.append(node)
    dirs = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    for a, b in dirs:
        if 0 <= node[0] + a < len(grid) and 0 <= node[1] + b < len(grid[0]) and (node[0] + a, node[1] + b) not in visited and grid[node[0]][node[1]] > 0:
            if visited[-1] == end:
                return visited
            visited = dfs(grid, (node[0] + a, node[1] + b), end, visited)

    return visited



def draw_maze():
    path = []
    running = True
    size_x, size_y = 20, 20
    start, end = None, None
    clower1 = [WIDTH // 2, HEIGHT // 8]
    drawn_grid = [[1 for i in range(size_y)] for j in range(size_x)]

    while running:
        screen.fill(BG_COLOR)
        drawGrid(drawn_grid, start, end, path)
        mx, my = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            rx, ry = getRectangleClicked(drawn_grid, mx, my)
            if rx is not None and ry is not None:
                if pygame.key.get_pressed()[pygame.K_LCTRL]:
                    if start is not None:
                        drawn_grid[start[0]][start[1]] = 1
                    start = (rx, ry)
                elif start != (rx, ry) and end != (rx, ry):
                    drawn_grid[rx][ry] = 0

        elif pygame.mouse.get_pressed()[2]:
            rx, ry = getRectangleClicked(drawn_grid, mx, my)
            if rx is not None and ry is not None:
                if pygame.key.get_pressed()[pygame.K_LCTRL]:
                    if end is not None:
                        drawn_grid[end[0]][end[1]] = 1
                    end = (rx, ry)
                elif end != (rx, ry) and start != (rx, ry):
                    drawn_grid[rx][ry] = 1

        draw_text('Draw Maze', font100, TEXT_COLOR, screen, WIDTH // 2, HEIGHT // 10)
        x = (clower1[0] + 50, clower1[1])
        y = (clower1[0] + 25, clower1[1] - 25)
        z = (clower1[0] + 25, clower1[1] + 25)
        draw_text(str(size_x), font100, TEXT_COLOR, screen, 390, 140)
        draw_text(str(size_y), font100, TEXT_COLOR, screen, 580, 140)
        lower_1 = pygame.draw.polygon(screen, RECT_COLOR, points=[(310, 140), (335, 115), (335, 165)])
        higher_1 = pygame.draw.polygon(screen, RECT_COLOR, points=[(470, 140), (445, 115), (445, 165)])
        lower_2 = pygame.draw.polygon(screen, RECT_COLOR, points=[(500, 140), (525, 115), (525, 165)])
        higher_2 = pygame.draw.polygon(screen, RECT_COLOR, points=[(660, 140), (635, 115), (635, 165)])
        # pygame.draw.polygon(screen, RECT_COLOR, points=[x, y, z])

        draw_text('Reset Maze', font32, TEXT_COLOR, screen, WIDTH // 2 + 350, HEIGHT // 10)
        button_reset_maze = pygame.Rect(WIDTH // 2 + 250, HEIGHT // 10 - 25, 200, 50)
        button_reset_maze = pygame.draw.rect(screen, END_COLOR, button_reset_maze, 1)
        draw_text('Solve Maze', font32, TEXT_COLOR, screen, WIDTH // 2 + 350, HEIGHT // 10 + 60)
        button_solve_maze = pygame.Rect(WIDTH // 2 + 250, HEIGHT // 10 - 25 + 60, 200, 50)
        button_solve_maze = pygame.draw.rect(screen, START_COLOR, button_solve_maze, 1)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_DOWN:
                    clower1[1] += 10
                if event.key == K_UP:
                    clower1[1] -= 10
                if event.key == K_LEFT:
                    clower1[0] -= 10
                if event.key == K_RIGHT:
                    clower1[0] += 10
                print(clower1)
                print(x, y, z)
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if lower_1.collidepoint((mx, my)):
                        if size_x > 3:
                            size_x -= 1
                            drawn_grid.pop()
                    elif higher_1.collidepoint((mx, my)):
                        if size_x < 50:
                            size_x += 1
                            drawn_grid.append([1 for i in range(size_y)])
                    elif lower_2.collidepoint((mx, my)):
                        if size_y > 3:
                            for x in range(len(drawn_grid)):
                                drawn_grid[x].pop()
                            size_y -= 1
                    elif higher_2.collidepoint((mx, my)):
                        if size_y < 40:
                            size_y += 1
                            for x in range(len(drawn_grid)):
                                drawn_grid[x].append(1)
                    elif button_reset_maze.collidepoint((mx, my)):
                        drawn_grid = [[1 for i in range(size_y)] for j in range(size_x)]
                        path = []
                        for i in drawn_grid:
                            print(i)
                        start = None
                        end = None

                    elif button_solve_maze.collidepoint((mx, my)):
                        path = astar.astar(copy.deepcopy(drawn_grid), start, end)
        pygame.display.update()
        CLOCK.tick(60)


def options():
    running = True
    while running:
        screen.fill((0, 0, 0))

        draw_text('TODO', font32, (255, 255, 255), screen, HEIGHT // 2, WIDTH // 2)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        CLOCK.tick(60)


main_menu()
