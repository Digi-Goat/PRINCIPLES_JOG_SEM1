import pygame, random

# Initialize Pygame
pygame.init()

# Set display surface
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("~~Snake~~")

# Set FPS and clock
FPS = 20
clock = pygame.time.Clock()

# Set game values
SNAKE_SIZE = 20
head_x = WINDOW_WIDTH // 2
head_y = WINDOW_HEIGHT // 2 + 100
snake_dx = 0
snake_dy = 0
score = 0

# Set colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (10, 0, 10)
DARKRED = (150, 0, 0)

# Set fonts
font = pygame.font.SysFont('gabriola', 48)

# Set text
def create_text_and_rect(text, color, background_color, **locations):
    text = font.render(text, True, color, background_color)
    rect = text.get_rect()
    for location in locations.keys():
        if location == "center":
            rect.center = locations[location]
        elif location == "topleft":
            rect.topleft = locations[location]
    return text, rect

title_text, title_rect = create_text_and_rect("~~Snake~~", GREEN, DARKRED, center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
score_text, score_rect = create_text_and_rect("score: " + str(score), GREEN, DARKRED , topleft=(10, 10))
game_over_text, game_over_rect = create_text_and_rect("GAMEOVER", RED, DARKGREEN, center=(WINDOW_WIDTH //2, WINDOW_HEIGHT // 2))
continue_text, continue_rect = create_text_and_rect("Press any key to play again", RED, DARKGREEN, center=(WINDOW_WIDTH //2, WINDOW_HEIGHT // 2 + 64))

# Set sounds and music
pick_up_sound = pygame.mixer.Sound("pick_up_sound.wav")

# Set images
apple_x = random.randint(0, (WINDOW_WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
apple_y = random.randint(0, (WINDOW_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
apple_coord = (apple_x, apple_y, SNAKE_SIZE, SNAKE_SIZE)
apple_rect = pygame.Rect(apple_coord)

head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)
head_rect = pygame.Rect(head_coord)

body_coords = []

# The main game loop
running = True
is_paused = False
is_game_start = True  # Flag for game start

def move_snake(event):
    global snake_dx, snake_dy
    if event.type == pygame.KEYDOWN:
        key = event.key
        if key == pygame.K_LEFT and snake_dx == 0:  # Prevent reversing direction
            snake_dx = -SNAKE_SIZE
            snake_dy = 0
        elif key == pygame.K_RIGHT and snake_dx == 0:
            snake_dx = SNAKE_SIZE
            snake_dy = 0
        elif key == pygame.K_UP and snake_dy == 0:
            snake_dx = 0
            snake_dy = -SNAKE_SIZE
        elif key == pygame.K_DOWN and snake_dy == 0:
            snake_dx = 0
            snake_dy = SNAKE_SIZE

def check_quit(event):
    global running
    if event.type == pygame.QUIT:
        running = False

def check_events():
    global running, is_game_start
    for event in pygame.event.get():
        check_quit(event)
        move_snake(event)
        if is_game_start and event.type == pygame.KEYDOWN:
            is_game_start = False  # Start the game after the first key press

def handle_snake():
    global body_coords, head_x, head_y, head_coord, head_rect
    body_coords.insert(0, head_coord)
    if len(body_coords) > score + 1:  # Ensure the body grows when the score increases
        body_coords.pop()
    head_x += snake_dx
    head_y += snake_dy
    head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)
    head_rect = pygame.Rect(head_coord)

def reset_game_after_game_over(event):
    global is_paused, score, head_x, head_y, head_coord, body_coords, snake_dx, snake_dy, apple_x, apple_y, apple_coord, apple_rect
    if event.type == pygame.KEYDOWN:
        score = 0
        head_x = WINDOW_WIDTH // 2
        head_y = WINDOW_HEIGHT // 2 + 100
        head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)
        body_coords = []
        snake_dx = 0
        snake_dy = 0
        apple_x = random.randint(0, (WINDOW_WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        apple_y = random.randint(0, (WINDOW_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        apple_coord = (apple_x, apple_y, SNAKE_SIZE, SNAKE_SIZE)
        apple_rect = pygame.Rect(apple_coord)
        is_paused = False

def check_end_game_after_game_over(event):
    global is_paused, running
    if event.type == pygame.QUIT:
        is_paused = False
        running = False

def check_game_over():
    global running, is_paused
    if (head_x < 0 or head_x >= WINDOW_WIDTH or
        head_y < 0 or head_y >= WINDOW_HEIGHT or
        head_coord in body_coords[1:]):  # Ignore the head itself
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                reset_game_after_game_over(event)
                check_end_game_after_game_over(event)

def check_collisions():
    global score, apple_x, apple_y, apple_coord, apple_rect, body_coords
    if head_rect.colliderect(apple_rect):
        score += 1
        pick_up_sound.play()
        apple_x = random.randint(0, (WINDOW_WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        apple_y = random.randint(0, (WINDOW_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        apple_coord = (apple_x, apple_y, SNAKE_SIZE, SNAKE_SIZE)
        apple_rect = pygame.Rect(apple_coord)
        body_coords.append(head_coord)

def blit_hud():
    # Only blit the title text if the game has just started
    if is_game_start:
        display_surface.blit(title_text, title_rect)
    else:
        display_surface.blit(score_text, score_rect)

def blit_assets():
    for body in body_coords:
        pygame.draw.rect(display_surface, DARKGREEN, body)
    pygame.draw.rect(display_surface, GREEN, head_coord)  # Draw the snake's head
    pygame.draw.rect(display_surface, RED, apple_rect)    # Draw the apple

def update_display_and_tick_clock():
    pygame.display.update()
    clock.tick(FPS)

while running:

    check_events()

    handle_snake()

    check_game_over()

    check_collisions()

    # Update HUD
    score_text = font.render("Score: " + str(score), True, GREEN, DARKRED)

    display_surface.fill(WHITE)

    blit_hud()

    blit_assets()

    update_display_and_tick_clock()

pygame.quit()
