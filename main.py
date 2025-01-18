import pygame
import random
import math

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 600, 600
FPS = 60
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Setup the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Game")

# Base class for game objects
class GameObject:
    def __init__(self, x, y, color, radius=20):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def check_collision(self, other):
        # Calculate distance between two objects
        dist = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        return dist < (self.radius + other.radius)

# Player class (Pac-Man)
class PacMan(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, YELLOW)

    def move(self, dx, dy):
        # Add boundary check for Pac-Man to stay within the screen
        if 0 < self.x + dx < WIDTH and 0 < self.y + dy < HEIGHT:
            self.x += dx
            self.y += dy

# Ghost class
class Ghost(GameObject):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)

    def move_towards_player(self, player_x, player_y):
        # Move the ghost towards Pac-Man's position (simple AI)
        if self.x < player_x:
            self.x += 1
        elif self.x > player_x:
            self.x -= 1

        if self.y < player_y:
            self.y += 1
        elif self.y > player_y:
            self.y -= 1

# Dot class for points collection
class Dot(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, GREEN, radius=5)

# Create Pac-Man and Ghosts
pacman = PacMan(WIDTH // 2, HEIGHT // 2)
ghosts = [
    Ghost(random.randint(0, WIDTH), random.randint(0, HEIGHT), RED),
    Ghost(random.randint(0, WIDTH), random.randint(0, HEIGHT), BLUE)
]

# Create some dots for Pac-Man to collect
dots = [Dot(random.randint(20, WIDTH - 20), random.randint(20, HEIGHT - 20)) for _ in range(10)]

# Score variable
score = 0

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key presses for Pac-Man's movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pacman.move(-5, 0)
    if keys[pygame.K_RIGHT]:
        pacman.move(5, 0)
    if keys[pygame.K_UP]:
        pacman.move(0, -5)
    if keys[pygame.K_DOWN]:
        pacman.move(0, 5)

    # Move the ghosts towards Pac-Man
    for ghost in ghosts:
        ghost.move_towards_player(pacman.x, pacman.y)

    # Draw Pac-Man and the ghosts
    pacman.draw(screen)
    for ghost in ghosts:
        ghost.draw(screen)

    # Draw and check for collisions with dots
    for dot in dots[:]:
        dot.draw(screen)
        if pacman.check_collision(dot):
            dots.remove(dot)  # Remove the dot if collected
            score += 10  # Increase score for collecting a dot

    # Check for collisions between Pac-Man and ghosts
    for ghost in ghosts:
        if pacman.check_collision(ghost):
            print("Game Over! Pac-Man caught!")
            running = False

    # Display score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Check if all dots are collected (win condition)
    if not dots:
        print("You Win! All dots collected!")
        running = False

    pygame.display.flip()
    clock.tick(FPS)

# Quit the game
pygame.quit()
