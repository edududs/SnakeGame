import random

import pygame

pygame.init()

# Definindo constantes
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SQUARE_SIZE = 15
VEL_GAME = 15
SNAKE_HEAD_RADIUS = SQUARE_SIZE // 1.45
FOOD_SIZE = SQUARE_SIZE
SCORE_PER_FOOD = 1

# Definindo cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class SnakeGame:
    def __init__(self):
        pygame.display.set_caption("Snake Game")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.end_game = False
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.vel_x = 0
        self.vel_y = 0

        self.direction = pygame.K_RIGHT

        self.snake_size = 1
        self.pixels = []

        self.food_x, self.food_y = self.generate_food()

    def generate_food(self):
        food_x = round(
            random.randrange(SQUARE_SIZE, SCREEN_WIDTH - SQUARE_SIZE, SQUARE_SIZE)
        )
        food_y = round(
            random.randrange(SQUARE_SIZE, SCREEN_HEIGHT - SQUARE_SIZE, SQUARE_SIZE)
        )
        return food_x, food_y

    def draw_food(self):
        pygame.draw.rect(
            self.screen,
            GREEN,
            [self.food_x, self.food_y, FOOD_SIZE, FOOD_SIZE],
        )

    def draw_snake(self):
        for pixel in self.pixels:
            pygame.draw.circle(
                self.screen,
                BLACK,
                (pixel[0] + SQUARE_SIZE // 2, pixel[1] + SQUARE_SIZE // 2),
                SQUARE_SIZE // 2,
            )

        # Desenhar a cabeça da cobra (o último pixel) com um tamanho maior para melhorar a aparência
        pygame.draw.circle(
            self.screen,
            BLACK,
            (
                self.pixels[-1][0] + SQUARE_SIZE // 2,
                self.pixels[-1][1] + SQUARE_SIZE // 2,
            ),
            SNAKE_HEAD_RADIUS,
        )

    def draw_score(self):
        font = pygame.font.SysFont("monospace", 20)
        text = font.render("Score: " + str(self.snake_size), True, RED)
        self.screen.blit(text, (1, 1))

    def select_vel(self, key):
        opposites = {
            pygame.K_UP: pygame.K_DOWN,
            pygame.K_DOWN: pygame.K_UP,
            pygame.K_LEFT: pygame.K_RIGHT,
            pygame.K_RIGHT: pygame.K_LEFT,
        }

        if key != opposites.get(self.direction):
            self.direction = key

        return {
            pygame.K_UP: (0, -SQUARE_SIZE),
            pygame.K_DOWN: (0, SQUARE_SIZE),
            pygame.K_LEFT: (-SQUARE_SIZE, 0),
            pygame.K_RIGHT: (SQUARE_SIZE, 0),
        }.get(self.direction, (0, 0))

    def game_over(self):
        font = pygame.font.SysFont("monospace", 50)
        text = font.render("Game Over", True, RED)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2))
        pygame.display.update()
        pygame.time.wait(2000)  # Aguarda 2 segundos
        self.end_game = True

    def run(self):
        while not self.end_game:
            self.screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end_game = True
                elif event.type == pygame.KEYDOWN:
                    self.vel_x, self.vel_y = self.select_vel(event.key)

            self.x += self.vel_x
            self.y += self.vel_y

            # Atualizar a posição da cobra
            if (
                self.x < 0
                or self.x >= SCREEN_WIDTH
                or self.y < 0
                or self.y >= SCREEN_HEIGHT
            ):
                self.game_over()

            # Desenhar comida
            self.draw_food()

            # Desenhar cobra
            self.pixels.append([self.x, self.y])
            if len(self.pixels) > self.snake_size:
                self.pixels.pop(0)

            # Condição se a cobrinha bateu no próprio corpo
            for pixel in self.pixels[:-1]:
                if pixel == [self.x, self.y]:
                    self.game_over()

            self.draw_snake()

            # Desenhar pontos
            self.draw_score()

            # Atualização da tela
            pygame.display.update()

            # Criar uma nova comida
            head_center = (self.x + SQUARE_SIZE // 2, self.y + SQUARE_SIZE // 2)
            food_center = (self.food_x + FOOD_SIZE // 2, self.food_y + FOOD_SIZE // 2)
            distance = (
                (head_center[0] - food_center[0]) ** 2
                + (head_center[1] - food_center[1]) ** 2
            ) ** 0.5
            if distance <= SNAKE_HEAD_RADIUS + FOOD_SIZE / 2:
                self.snake_size += SCORE_PER_FOOD
                self.food_x, self.food_y = self.generate_food()

            self.clock.tick(VEL_GAME)

        pygame.quit()


if __name__ == "__main__":
    game = SnakeGame()
    game.run()
