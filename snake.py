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
apple_coord = (500, 500, SNAKE_SIZE, SNAKE_SIZE)
apple_rect = pygame.draw.rect(display_surface, RED, apple_coord)

head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)
head_rect = pygame.draw.rect(display_surface, GREEN, head_coord)

body_coords = []


# The main game loop
running = True
is_paused = False

def move_snake(event):
    global snake_dx, snake_dy
    if event.type == pygame.KEYDOWN:
        key = event.key
        if pygame.K_LEFT:
            snake_dx = -SNAKE_SIZE
            snake_dy = 0
        elif pygame.K_RIGHT:
            snake_dx = SNAKE_SIZE
            snake_dy = 0
        elif pygame.K_UP:
             snake_dx = 0
             snake_dy = -SNAKE_SIZE
    elif pygame.K_DOWN:
             snake_dx = 0
             snake_dy = SNAKE_SIZE

def check_quit(event):
    global running
    if event.type == pygame. QUIT:
        running = False

def check_events():
    global running
    for event in pygame.event.get():
        check_quit(event)
        move_snake(event)


def handle_snake():
    global body_coords, head_x, head_y, head_coord
    body_coords.insert(0, head_coord)
    body_coords.pop()
    head_x += snake_dx
    head_y += snake_dy
    head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)

def reset_game_after_game_over(event):
    global is_paused, score, head_x, head_y, head_coord, body_coords, snake_dx, snake_dy
    if event.type == pygame.KEYDOWN:
        score = 0
        head_x = WINDOW_WIDTH // 2
        head_y = WINDOW_HEIGHT // 2 + 100
        head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)
        body_coords = []
        snake_dx = 0
        snake_dy = 0
        is_paused = False

def check_end_game_after_game_over(event):
    global is_paused, running
    if event.type == pygame.QUIT:
        is_paused = False
        running = False

def check_game_over():
    global head_rect, head_coord, body_coords, running, is_paused
    if head_rect.left < 0 or head_rect.right > WINDOW_WIDTH or head_rect.top < 0 or head_rect.bottom > WINDOW_HEIGHT or head_rect in body_coords:
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                reset_game_after_game_over(event)
                check_end_game_after_game_over(event)

def check_collisions():
    global score, apple_x, apple_y, apple_coord, body_coords
    if head_rect.colliderect(apple_rect):
        score += 1
        pick_up_sound.play()
        apple_x = random.randint(0, WINDOW_WIDTH - SNAKE_SIZE)
        apple_y = random.randint(0, WINDOW_HEIGHT - SNAKE_SIZE)
        apple_coord = (apple_x, apple_y, SNAKE_SIZE, SNAKE_SIZE)
        body_coords.append(head_coord)

def blit_hud():
    display_surface.blit(title_text, title_rect)
    display_surface.blit(score_text, score_rect)


def blit_assets():
    global head_rect, apple_rect
    for body in body_coords:
        pygame.draw.rect(display_surface, DARKGREEN, body)
        head_rect = pygame.draw.rect(display_surface, GREEN, head_coord)
        apple_rect = pygame.draw.rect(display_surface, RED, apple_coord)

def update_display_and_tick_clock():
    pygame.display.update()
    clock.tick(FPS)

while running:
    # Check pygame events
    check_events()

    # handle growing and manipulating the snake
    handle_snake()

    # Check for game over
    check_game_over()

    # Check for collisions
    check_collisions()

    # Update HUD
    score_text = font.render("Score: " + str(score), True, GREEN, DARKRED)

    # Fill the surface
    display_surface.fill(WHITE)

    # Blit HUD
    blit_hud()

    # Blit assets
    blit_assets()

    # Update display and tick clock
    update_display_and_tick_clock()

# End the game
pygame.quit()
