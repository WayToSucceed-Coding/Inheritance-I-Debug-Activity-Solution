import pygame
import random
import math

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 600, 600
FPS = 60
BLACK = (0, 0, 0)
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
        dist = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        return dist < (self.radius + other.radius)

# Pac-Man class inherits GameObject
class PacMan(GameObject):#Bug 1
    def __init__(self, x, y):
        # Initialize attributes directly without calling the parent class's name or super()
        self.x = x
        self.y = y
        self.color = YELLOW
        self.radius = 20

    def move(self, dx, dy):
        # Add boundary check for Pac-Man to stay within the screen
        if 0 < self.x + dx < WIDTH and 0 < self.y + dy < HEIGHT:
            self.x += dx
            self.y += dy

# Ghost class inherits GameObject
class Ghost(GameObject):#Bug 2
    def __init__(self, x, y, color):
        # Initialize attributes directly without calling the parent class's name or super()
        self.x = x
        self.y = y
        self.color = color
        self.radius = 20

    def move_towards_player(self, player_x, player_y):
        # Calculate the difference in position
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        # Normalize the direction
        if distance != 0:
            dx /= distance
            dy /= distance

        # Introduce randomness in movement while still heading towards Pac-Man
        move_direction = random.choice(["direct", "random"])

        if move_direction == "direct":
            # Move smoothly towards Pac-Man
            self.x += dx * 2  # Adjust speed of movement here
            self.y += dy * 2  # Adjust speed of movement here
        elif move_direction == "random":
            # Move in a random direction (small steps)
            random_move = random.choice([("up", 0), ("down", 0), ("left", 0), ("right", 0)])
            if random_move[0] == "up":
                self.y -= 1
            elif random_move[0] == "down":
                self.y += 1
            elif random_move[0] == "left":
                self.x -= 1
            elif random_move[0] == "right":
                self.x += 1

# Dot class (no inheritance, simple class)
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = GREEN
        self.radius = 5

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def check_collision(self, other):
        dist = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        return dist < (self.radius + other.radius)

# Create Pac-Man and Ghosts
pacman = PacMan(WIDTH // 2, HEIGHT // 2)
ghosts = [
    Ghost(random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100), RED),  # Initializing far from Pac-Man
    Ghost(random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100), BLUE)
]

# Create some dots for Pac-Man to collect
dots = [Dot(random.randint(20, WIDTH - 20), random.randint(20, HEIGHT - 20)) for _ in range(10)]

# Score variable
score = 0

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)  # Set background to black
    
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
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Check if all dots are collected (win condition)
    if not dots:
        print("You Win! All dots collected!")
        running = False

    pygame.display.flip()
    clock.tick(FPS)

# Quit the game
pygame.quit()
