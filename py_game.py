import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1920, 1080
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Gravity
gravity = 1

def char_setting():
    global player_size_x,player_size_y,player_x,player_y,player_velocity,player_touch_ground
    # Player variables
    player_size_x = 30
    player_size_y = 60
    player_x = WIDTH // 2 - player_size_x // 2
    player_y = HEIGHT - player_size_y
    player_velocity = 0
    player_touch_ground = True


    global arrow_radius,arrow_x,arrow_y,arrow_velocity_y,arrow_velocity_x,arrow_angle,arrow_touch_ground
    #arrom variables
    arrow_radius = 10
    #arrow_size_x = 40
    #arrow_size_y = 10
    arrow_x = (WIDTH // 2 - arrow_radius // 2) + player_size_x * 0.8
    arrow_y = (HEIGHT - arrow_radius) - player_size_y * 0.5
    arrow_velocity_y = 0
    arrow_velocity_x = 0
    arrow_angle = 0
    arrow_touch_ground = True

char_setting()

# Pygame setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Throwing Game")
clock = pygame.time.Clock()

throw_angle = 0
throw_power = 0

font = pygame.font.Font('freesansbold.ttf', 32)

# create a text surface object,
# on which text is drawn on it.


# Main game loop
while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_q]:
            pygame.quit()
            sys.exit()


        '''if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and player_touch_ground:
                player_velocity -= 15
                player_touch_ground = False

            if event.key == pygame.K_j and arrow_touch_ground:
                arrow_velocity_y -= 20
                arrow_touch_ground = False'''

    if keys[pygame.K_w]:
        throw_angle += 1
    if keys[pygame.K_s]:
        throw_angle -= 1
    if keys[pygame.K_a]:
        throw_power -= 1
    if keys[pygame.K_d]:
        throw_power += 1
    if keys[pygame.K_f]:
        arrow_velocity_x += throw_power * math.cos(math.radians(throw_angle))
        arrow_velocity_y -= throw_power * math.sin(math.radians(throw_angle))
        print(f'x = {arrow_velocity_x} , y = {arrow_velocity_y}')
        throw_angle = 0
        throw_power = 0
        arrow_touch_ground = False
    if keys[pygame.K_r]:
        char_setting()

    text = font.render(f'POW : {throw_power} / AN : {throw_angle}', True, GREEN, BLUE)

    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()

    # set the center of the rectangular object.
    textRect.center = (WIDTH // 2, HEIGHT // 2)


    # Update player position and velocity with gravity
    player_y += player_velocity
    player_velocity += gravity

    if not arrow_touch_ground:
        arrow_y += arrow_velocity_y
        arrow_velocity_y +=gravity
        arrow_x += arrow_velocity_x

    # Keep player within screen boundaries
    if player_y > HEIGHT - player_size_y:
        player_y = HEIGHT - player_size_y
        player_velocity = 0
        player_touch_ground = True

    if arrow_y > HEIGHT - arrow_radius:
        arrow_y = HEIGHT - arrow_radius
        arrow_velocity_y = 0
        arrow_velocity_x = 0
        arrow_touch_ground = True


    # Clear the screen
    screen.fill(WHITE)

    # Draw the player
    pygame.draw.rect(screen, RED, (player_x, player_y, player_size_x, player_size_y))
    pygame.draw.circle(screen, BLUE, [arrow_x, arrow_y], arrow_radius, 0)

    screen.blit(text, textRect)
    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
