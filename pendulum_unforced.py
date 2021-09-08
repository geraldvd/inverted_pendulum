import numpy as np
from numpy.linalg import inv
from math import sin, pi, cos
import matplotlib.pyplot as plt
import pygame


def G(y, t):
    """Runga Kutta: G(y, t) is vector function for accelaration, where
    y = [theta_dot, theta] and t is time"""
    theta1_dot, theta1 = y[0], y[1]
    return np.array([-g / l1 * sin(theta1), theta1_dot])


def RK4_step(y, t, dt):
    """Runga Kutta 4th order solution of EOM; returns delta_y"""
    k1 = G(y, t)
    k2 = G(y + 0.5 * k1 * dt, t + 0.5 * dt)
    k3 = G(y + 0.5 * k2 * dt, t + 0.5 * dt)
    k4 = G(y + k3 * dt, t + dt)

    return dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6


def update(theta1):
    SCALE = 100

    x = l1 * sin(theta1)
    y = -l1 * cos(theta1)

    return (x * SCALE + ORIGIN[0], -y * SCALE + ORIGIN[1])


def render(point1):
    # Clear screen
    screen.fill(BLACK)
    # Draw cart, rod and mass
    pygame.draw.line(screen, RED, ORIGIN, point1, 5)
    pygame.draw.rect(
        screen,
        WHITE,
        (
            ORIGIN[0] - CART_WIDTH / 2,
            ORIGIN[1] - CART_HEIGHT / 2,
            CART_WIDTH,
            CART_HEIGHT,
        ),
    )
    pygame.draw.circle(screen, RED, ORIGIN, 3)
    pygame.draw.circle(screen, BLUE, point1, m1 * 10)


# Pygame paramters
running = True
w = 800
h = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LT_BLUE = (230, 230, 255)
CART_WIDTH = 100
CART_HEIGHT = 20
ORIGIN = (w / 2, h / 2)
TEXT_POSITION = (10, 10)

pygame.init()
screen = pygame.display.set_mode([w, h])
pygame.display.update()
clock = pygame.time.Clock()

# System parameters
m1 = 2.0
l1 = 1.0
g = 9.81
delta_t = 0.02

# Initial state
t = 0.0
y = np.array(
    [0, pi - 0.00001]
)  # [velocities, displacements] => [v1, v2, ..., d1, d2, ...] => [dtheta1, theta1]

# Timer
pygame.font.init()
myfont = pygame.font.SysFont("Halvetica", 24)

# Simulate/animate
while running:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT or (
            e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE
        ):
            running = False

    point1 = update(y[1])
    render(point1)

    nl = "\n"
    time_text = myfont.render(f"Time: {round(t, 1)} seconds", False, WHITE)
    angle_text = myfont.render(f"Angle: {y[1]*180/pi:.2f} deg", False, WHITE)
    screen.blit(time_text, (10, 10))
    screen.blit(angle_text, (10, 35))

    t += delta_t
    y = y + RK4_step(y, t, delta_t)

    clock.tick(60)
    pygame.display.update()
