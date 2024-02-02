import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Gravity
gravity = 1

# Player variables
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size
player_velocity = 0

# Pygame setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Throwing Game")
clock = pygame.time.Clock()

#status
touch_ground = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()