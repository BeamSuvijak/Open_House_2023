import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
global WIDTH, HEIGHT
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

class Player:
    #player_size_x, player_size_y, player_x, player_y, player_velocity, player_touch_ground
    # Player variables
    player_size_x = 30
    player_size_y = 60
    player_x = WIDTH // 2 - player_size_x // 2
    player_y = HEIGHT - player_size_y
    player_velocity = 0
    player_touch_ground = True
    Color = BLACK
    TURN = True
    health = 100

    def __init__(self,sizex,sizey,x,y,velo,touch,color):
        self.player_size_x = sizex
        self.player_size_y = sizey
        self.player_x = x
        if y != -1:
            self.player_y = y
        self.player_velocity = velo
        self.player_touch_ground = touch
        self.Color = color

    def player_gravity(self):
        self.player_y += self.player_velocity
        self.player_velocity += gravity

    def display(self):
        pygame.draw.rect(screen, self.Color, (self.player_x, self.player_y, self.player_size_x, self.player_size_y))

    def keepin(self):
        if self.player_y > HEIGHT - self.player_size_y:
            self.player_y = HEIGHT - self.player_size_y
            self.player_velocity = 0
            self.player_touch_ground = True

    def is_turn(self):
        return self.TURN
class arrow:
    #global arrow_radius, arrow_x, arrow_y, arrow_velocity_y, arrow_velocity_x, arrow_angle, arrow_touch_ground
    # arrom variables
    arrow_radius = 10
    # arrow_size_x = 40
    # arrow_size_y = 10
    arrow_x = 0
    arrow_y = 0
    arrow_velocity_y = 0
    arrow_velocity_x = 0
    arrow_angle = 0
    arrow_touch_ground = True
    throw_angle = 0
    throw_power = 0

    def __init__(self,radius,x,y,velox,veloy,angle,touch):
        self.arrow_radius = radius
        self.arrow_x = x
        self.arrow_y = y
        self.arrow_velocity_x = velox
        self.arrow_velocity_y = veloy
        self.arrow_angle = angle
        self.arrow_touch_ground = touch

    def set_position(self,x,y):
        self.arrow_x = x
        self.arrow_y = y
    def throwset(self,power,angle):
        self.throw_power += power
        self.throw_angle += angle

    def throw(self):
        self.arrow_velocity_x += self.throw_power * math.cos(math.radians(self.throw_angle))
        self.arrow_velocity_y -= self.throw_power * math.sin(math.radians(self.throw_angle))
        if p2.TURN:
            self.arrow_velocity_x = 0 - self.arrow_velocity_x

        print(f'x = {self.arrow_velocity_x} , y = {self.arrow_velocity_y}')
        self.throw_angle = 0
        self.throw_power = 0
        self.arrow_touch_ground = False

        if p1.TURN:
            p1.TURN = False
            p2.TURN = True
        else:
            p1.TURN = True
            p2.TURN = False

    def arrow_gravity(self):
        if not self.arrow_touch_ground:
            self.arrow_y += self.arrow_velocity_y
            self.arrow_velocity_y += gravity
            self.arrow_x += self.arrow_velocity_x

    def arrow_display(self):
        pygame.draw.circle(screen, BLUE, [self.arrow_x, self.arrow_y], self.arrow_radius, 0)

    def keepin(self):
        if self.arrow_y > HEIGHT - self.arrow_radius:
            self.arrow_y = HEIGHT - self.arrow_radius
            self.arrow_velocity_y = 0
            self.arrow_velocity_x = 0
            self.arrow_touch_ground = True

    def check_collision(self):
        circle_x = self.arrow_x
        circle_y = self.arrow_y
        circle_radius = self.arrow_radius
        if p1.TURN:
            rect_x = p1.player_x
            rect_y = p1.player_y
            rect_width = p1.player_size_x
            rect_height = p1.player_size_y
        if p2.TURN:
            rect_x = p2.player_x
            rect_y = p2.player_y
            rect_width = p2.player_size_x
            rect_height = p2.player_size_y

        # Closest point on the rectangle to the center of the circle
        closest_x = max(rect_x, min(circle_x, rect_x + rect_width))
        closest_y = max(rect_y, min(circle_y, rect_y + rect_height))

        # Calculate distance between the closest point and the center of the circle
        distance = math.sqrt((circle_x - closest_x) ** 2 + (circle_y - closest_y) ** 2)

        # Check if the distance is less than the radius of the circle
        #print(distance)
        return distance < circle_radius

def char_setting():
    global p1,p2,a
    p1 = Player(50,80,100,-1,0,True,RED)
    p2 = Player(50, 80, (WIDTH - 100) , -1, 0, True,BLACK)
    p2.TURN = False

    a = arrow(10,p1.player_x+p1.player_size_x+10,HEIGHT - (p1.player_size_y * 0.8),0,0,0,True)



char_setting()

# Pygame setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Throwing Game")
clock = pygame.time.Clock()


font = pygame.font.Font('freesansbold.ttf', 32)


def text():
    global p_turn
    p_turn = 0
    if p1.TURN:
        p_turn = 1
    if p2.TURN:
        p_turn = 2
    text = font.render(f'Player : {p_turn} / POW : {a.throw_power} / AN : {a.throw_angle}', True, GREEN, BLUE)
    textRect = text.get_rect()
    textRect.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(text, textRect)



def button():
    if keys[pygame.K_w]:
        a.throwset(1,0)
    if keys[pygame.K_s]:
        a.throwset(-1,0)
    if keys[pygame.K_a]:
        a.throwset(0,-1)
    if keys[pygame.K_d]:
        a.throwset(0,1)

    if keys[pygame.K_r]:
        char_setting()

    if keys[pygame.K_b]:
        p1.player_x += 20

# Main game loop
while True:
    global keys
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_q]:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                a.throw()

    button()

    # Update player position and velocity with gravity
    p1.player_gravity()
    p2.player_gravity()
    a.arrow_gravity()

    # Keep player within screen boundaries
    p1.keepin()
    p2.keepin()
    a.keepin()

    #Check Turn
    if p1.TURN and a.arrow_touch_ground:
        a.set_position(p1.player_x+p1.player_size_x+10,HEIGHT - (p1.player_size_y * 0.8))

    elif p2.TURN and a.arrow_touch_ground:
        a.set_position(p2.player_x - 10, HEIGHT - (p1.player_size_y * 0.8))


    if a.check_collision():
        print(f'hit player{p_turn}')
        a.arrow_touch_ground = True

    # Clear the screen
    screen.fill(WHITE)

    # Draw the player
    p1.display()
    p2.display()
    a.arrow_display()

    text()
    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
