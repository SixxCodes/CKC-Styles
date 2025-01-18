import pygame
import random

#Initialize Pygame
pygame.init()

#Screen dimensions
WIDTH, HEIGHT = 400, 500
GRID_SIZE = 8  # 8x8 grid
BLOCK_SIZE = WIDTH // GRID_SIZE

#Game Colors
BOARD = (255, 255, 255)
GROUT = (85, 0, 43)
PLACED_BLOCK = (255, 217, 236)
BLOCK = (255, 79, 136)

#Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Blast 8x8 ni Indai Kini")

#Fonts
font = pygame.font.Font(None, 36)

# Grid and blocks
grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

shapes = [
    [[1]],  # Single block
    [[1, 1]],  # Horizontal block
    [[1], [1]],  # Vertical block
    [[1, 1], [1, 1]],  # 2x2 block
    [[1, 1, 1]],  # Horizontal triple block
    [[1], [1], [1]],  # Vertical triple block
    [[1, 0], [1, 1], [1, 0]],  # L shape
    [[0, 1], [0, 1], [1, 1]],  # Mirrored L shape
    [[1, 1, 1], [1, 1, 1], [1, 1, 1]],  # 3x3 block
]

# Generate random block
def generate_block():
    shape = random.choice(shapes)
    block = {
        "shape": shape,
        "x": WIDTH // 2 - len(shape[0]) * BLOCK_SIZE // 2,
        "y": HEIGHT - 3 * BLOCK_SIZE,
        "dragging": False,
    }
    return block

# Check if block can fit on the grid
def can_place_block(block, x, y):
    for row in range(len(block)):
        for col in range(len(block[row])):
            if block[row][col]:
                if not (0 <= x + col < GRID_SIZE and 0 <= y + row < GRID_SIZE):
                    return False
                if grid[y + row][x + col]:
                    return False
    return True

# Place block on grid
def place_block(block, x, y):
    for row in range(len(block)):
        for col in range(len(block[row])):
            if block[row][col]:
                grid[y + row][x + col] = 1

# Clear full rows and columns
def clear_lines():
    global grid
    cleared = 0
    # Check rows
    for y in range(GRID_SIZE):
        if all(grid[y]):
            cleared += 1
            grid[y] = [0] * GRID_SIZE
    # Check columns
    for x in range(GRID_SIZE):
        if all(grid[y][x] for y in range(GRID_SIZE)):
            cleared += 1
            for y in range(GRID_SIZE):
                grid[y][x] = 0
    return cleared

# Draw grid
def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, PLACED_BLOCK if grid[y][x] else BOARD, rect)
            pygame.draw.rect(screen, GROUT, rect, 1)

# Draw block
def draw_block(block):
    for row in range(len(block["shape"])):
        for col in range(len(block["shape"][row])):
            if block["shape"][row][col]:
                rect = pygame.Rect(
                    block["x"] + col * BLOCK_SIZE, block["y"] + row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE
                )
                pygame.draw.rect(screen, BLOCK, rect)
                pygame.draw.rect(screen, GROUT, rect, 1)

# Main loop
clock = pygame.time.Clock()
running = True
score = 0
current_block = generate_block()

while running:
    screen.fill(BOARD)
    draw_grid()
    draw_block(current_block)

    # Draw score
    score_text = font.render(f"Score: {score}", True, GROUT)
    screen.blit(score_text, (10, HEIGHT - 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (
                current_block["x"] <= mouse_x <= current_block["x"] + len(current_block["shape"][0]) * BLOCK_SIZE
                and current_block["y"] <= mouse_y <= current_block["y"] + len(current_block["shape"]) * BLOCK_SIZE
            ):
                current_block["dragging"] = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if current_block["dragging"]:
                current_block["dragging"] = False
                grid_x = current_block["x"] // BLOCK_SIZE
                grid_y = current_block["y"] // BLOCK_SIZE
                if can_place_block(current_block["shape"], grid_x, grid_y):
                    place_block(current_block["shape"], grid_x, grid_y)
                    score += clear_lines()
                    current_block = generate_block()

        elif event.type == pygame.MOUSEMOTION:
            if current_block["dragging"]:
                mouse_x, mouse_y = event.pos
                current_block["x"] = mouse_x - (len(current_block["shape"][0]) * BLOCK_SIZE) // 2
                current_block["y"] = mouse_y - (len(current_block["shape"]) * BLOCK_SIZE) // 2

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
