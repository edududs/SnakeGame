import random

import pygame

pygame.init()


class SnakeGame:
    def __init__(self):
        pygame.display.set_caption("Snake Game")
        self.width, self.height = 1200, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)

        self.square_size = 10
        self.vel_game = 15

        self.end_game = False
        self.x = self.width / 2
        self.y = self.height / 2
        self.vel_x = 0
        self.vel_y = 0

        self.direction = pygame.K_RIGHT

        self.snake_size = 1
        self.pixels = []

        self.food_x, self.food_y = self.generate_food()

    def generate_food(self):
        food_x = round(
            random.randrange(
                self.square_size, self.width - self.square_size, self.square_size
            )
        )
        food_y = round(
            random.randrange(
                self.square_size, self.height - self.square_size, self.square_size
            )
        )
        return food_x, food_y

    def draw_food(self):
        pygame.draw.rect(
            self.screen,
            self.green,
            [self.food_x, self.food_y, self.square_size, self.square_size],
        )

    def draw_snake(self):
        for pixel in self.pixels:
            pygame.draw.circle(
                self.screen,
                self.black,
                (pixel[0] + self.square_size // 2, pixel[1] + self.square_size // 2),
                self.square_size // 2,
            )

        # Desenhar a cabeça da cobra (o último pixel) com um tamanho maior para melhorar a aparência
        pygame.draw.circle(
            self.screen,
            self.black,
            (
                self.pixels[-1][0] + self.square_size // 2,
                self.pixels[-1][1] + self.square_size // 2,
            ),
            self.square_size // 1.45,
        )

    def draw_score(self):
        font = pygame.font.SysFont("monospace", 20)
        text = font.render("Score: " + str(self.snake_size), True, self.red)
        self.screen.blit(text, (1, 1))

    def select_vel(self, key):
        oposites = {
            pygame.K_UP: pygame.K_DOWN,
            pygame.K_DOWN: pygame.K_UP,
            pygame.K_LEFT: pygame.K_RIGHT,
            pygame.K_RIGHT: pygame.K_LEFT,
        }

        if key != oposites.get(self.direction):
            self.direction = key

        return {
            pygame.K_UP: (0, -self.square_size),
            pygame.K_DOWN: (0, self.square_size),
            pygame.K_LEFT: (-self.square_size, 0),
            pygame.K_RIGHT: (self.square_size, 0),
        }.get(self.direction, (0, 0))

    def run(self):
        while not self.end_game:
            self.screen.fill(self.white)

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
                or self.x >= self.width
                or self.y < 0
                or self.y >= self.height
            ):
                self.end_game = True

            # Desenhar comida
            self.draw_food()

            # Desenhar cobra
            self.pixels.append([self.x, self.y])
            if len(self.pixels) > self.snake_size:
                self.pixels.pop(0)

            # Condição se a cobrinha bateu no próprio corpo
            for pixel in self.pixels[:-1]:
                if pixel == [self.x, self.y]:
                    self.end_game = True

            self.draw_snake()

            # Desenhar pontos
            self.draw_score()

            # Atualização da tela
            pygame.display.update()

            # Criar uma nova comida
            if self.x == self.food_x and self.y == self.food_y:
                self.snake_size += 4
                self.food_x, self.food_y = self.generate_food()

            self.clock.tick(self.vel_game)

        pygame.quit()


if __name__ == "__main__":
    game = SnakeGame()
    game.run()
