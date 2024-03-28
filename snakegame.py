import pygame
import random

# Screen sizes
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Snake and food classes
class Snake:
    def __init__(self):
        self.size = 10
        self.length = 1
        self.positions = [(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = BLACK
    
    def get_head_position(self):
        return self.positions[0]
    
    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point
    
    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x*self.size)) % SCREEN_WIDTH), (cur[1] + (y*self.size)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            return True
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
    
    def reset(self):
        self.__init__()

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (self.size, self.size))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, WHITE, r, 1)

class Food:
    def __init__(self):
        self.size = 10
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()
    
    def randomize_position(self):
        self.position = (random.randint(0, (SCREEN_WIDTH-self.size )//self.size ) * self.size ,
                         random.randint(0, (SCREEN_HEIGHT-self.size )//self.size ) * self.size )
    
    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (self.size, self.size))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, WHITE, r, 1)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")
    
    snake = Snake()
    food = Food()
    
    score = 0
    game_over = False
    
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.turn(UP)
                elif event.key == pygame.K_DOWN:
                    snake.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.turn(RIGHT)
        
        collision = snake.move()
        if collision:
            game_over = True
        
        if snake.get_head_position() == food.position:
            snake.length += 1
            score += 1
            food.randomize_position()
        
        screen.fill(WHITE)
        snake.draw(screen)
        food.draw(screen)
        pygame.display.update()
        clock.tick(10)

    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Game over! Score: {score}", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()

if __name__ == "__main__":
    main()