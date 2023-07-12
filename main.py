import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 640, 480
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Define colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Size of the snake and the food
SIZE = 20

# Snake speed
SPEED = 10


# Create the Snake class
class Snake:
    def __init__(self):
        self.body = []
        self.direction = "RIGHT"
        self.body.append([WIDTH / 2, HEIGHT / 2])
        self.grow_flag = False

    def move(self):
        new_segment = self.body[0].copy()
        if self.direction == "RIGHT":
            new_segment[0] += SIZE
        elif self.direction == "LEFT":
            new_segment[0] -= SIZE
        elif self.direction == "UP":
            new_segment[1] -= SIZE
        elif self.direction == "DOWN":
            new_segment[1] += SIZE
        self.body.insert(0, new_segment)
        if not self.grow_flag:
            self.body.pop()  # Remove the last segment to simulate movement
        else:
            self.grow_flag = False

    def change_direction(self, new_direction):
        if new_direction == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"
        elif new_direction == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
        elif new_direction == "UP" and self.direction != "DOWN":
            self.direction = "UP"
        elif new_direction == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"

    def grow(self):
        self.grow_flag = True

    def draw(self):
        for segment_s in self.body:
            pygame.draw.rect(window, GREEN, (segment_s[0], segment_s[1], SIZE, SIZE))
            pygame.draw.rect(window, BLACK, (segment_s[0], segment_s[1], SIZE, SIZE), 1)


# Create the Food class
class Food:
    def __init__(self):
        self.x = random.randint(0, (WIDTH - SIZE) // SIZE) * SIZE
        self.y = random.randint(0, (HEIGHT - SIZE) // SIZE) * SIZE

    def draw(self):
        pygame.draw.rect(window, RED, (self.x, self.y, SIZE, SIZE))
        pygame.draw.rect(window, BLACK, (self.x, self.y, SIZE, SIZE), 1)


snake = Snake()
food = Food()

clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.change_direction("RIGHT")
            elif event.key == pygame.K_LEFT:
                snake.change_direction("LEFT")
            elif event.key == pygame.K_UP:
                snake.change_direction("UP")
            elif event.key == pygame.K_DOWN:
                snake.change_direction("DOWN")

    window.fill(BLACK)

    snake.move()

    # Check collision with the food
    if snake.body[0][0] == food.x and snake.body[0][1] == food.y:
        snake.grow()
        food = Food()

    # Check collision with the wall
    if (snake.body[0][0] < 0 or snake.body[0][0] >= WIDTH or
            snake.body[0][1] < 0 or snake.body[0][1] >= HEIGHT):
        running = False

    # Check collision with its own body
    for segment in snake.body[1:]:
        if snake.body[0][0] == segment[0] and snake.body[0][1] == segment[1]:
            running = False

    snake.draw()
    food.draw()

    pygame.display.update()
    clock.tick(SPEED)

# Quit the game
pygame.quit()
