import math as m
import pygame
from pygame import event
from pygame import draw

# Setup window
running = True
pygame.init()
size_x = 800
size_y = 600
screen = pygame.display.set_mode([size_x, size_y])

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Parameters
CART_WIDTH = 100
CART_HEIGHT = 20
X_ORIGIN = size_x / 2
Y_ORIGIN = size_y - 100
ROD_LENGTH = 100
GRAV = 9.81
M_CART = 5
M_BALL = 0.5


# Object definitions
def draw_cart(x, theta=0, surface=screen):
    # Clear screen
    surface.fill(BLACK)
    # Draw cart itself
    x_cart = X_ORIGIN + x - 0.5 * CART_WIDTH
    y_cart = Y_ORIGIN - 0.5 * CART_HEIGHT
    pygame.draw.rect(surface, WHITE, (x_cart, y_cart, CART_WIDTH, CART_HEIGHT))
    # Draw rod and ball mass
    x_ball = X_ORIGIN + x - ROD_LENGTH * m.sin(theta)
    y_ball = Y_ORIGIN - ROD_LENGTH * m.cos(theta)
    pygame.draw.line(surface, BLUE, (X_ORIGIN + x, Y_ORIGIN), (x_ball, y_ball), 5)
    pygame.display.update()


# Main loop
F = 0
x = 0
d_x = 0
dd_x = 0
theta = 0
d_theta = 0
dd_theta = 0
dt = 0.1
t = 0
while running:
    draw_cart(x, theta)
    pygame.display.update()
    
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT or (
            e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE
        ):
            running = False
    
    # Update time for next iteration
    t += dt
    
    # Calculate x equation of motion
    dd_theta = 1/(M_CART+M_BALL) * (F + M_BALL*ROD_LENGTH*dd_theta*m.cos(theta) - M_BALL*ROD_LENGTH*d_theta**2*m.sin(theta))
    d_theta = d_theta + dd_theta * dt
    theta = theta + d_theta * dt

    # Calculate Theta equation of motion
    dd_x = (ROD_LENGTH*dd_theta - GRAV*m.sin(theta)) / m.cos(theta)
    d_x = d_x + dd_x * dt
    x = x + d_x * dt

    pygame.time.wait(5)

# cleanup
pygame.quit()
