import pygame
from dataclasses import dataclass
from edit_me import take_turn, Direction

MOVE_TIME = 1.0

def lerp(a, b, t):
    return a + (b - a) * t

GRID_SIZE = 80

class Drawable(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, texture):
        super().__init__()
        self.__x = x_pos - 1
        self.__y = y_pos - 1
        self.__next_x = self.__x
        self.__next_y = self.__y
        self.__timer = 0
        img = pygame.image.load(texture).convert_alpha()
        self.__img = pygame.transform.scale(img, (GRID_SIZE, GRID_SIZE))

    def move_to(self, x_pos, y_pos):
        next_x = x_pos - 1
        next_y = y_pos - 1

        updated = False
        if next_x != self.__next_x:
            self.__x = self.__next_x
            self.__next_x = next_x
            updated = True

        if next_y != self.__next_y:
            self.__y = self.__next_y
            self.__next_y = next_y
            updated = True

        if updated:
            self.__timer = MOVE_TIME

    def get_position(self):
        return lerp(self.__next_x, self.__x, self.__timer / MOVE_TIME), lerp(self.__next_y, self.__y, self.__timer / MOVE_TIME)

    def advance_timer(self, delta_time):
        self.__timer = self.__timer - delta_time
        if self.__timer < 0:
            self.__timer = 0
            self.__x = self.__next_x
            self.__y = self.__next_y

    def render(self, delta_time):
        pass

class Santa(Drawable):
    def __init__(self, x_pos, y_pos):
        super().__init__(x_pos, y_pos, "santa.png")

class Gift(Drawable):
    def __init__(self, x_pos, y_pos):
        super().__init__(x_pos, y_pos, "gift.png")

@dataclass
class GameState:
    santas: list[Santa]
    gifts: list[Gift]

class Game:
    def __init__(self, grid_width, grid_height):
        window_width = grid_width * GRID_SIZE
        window_height = grid_height * GRID_SIZE

        self.__game_state = GameState(list(), list())
        pygame.display.init()
        pygame.display.set_mode((window_width, window_height))

        self.__clock = pygame.time.Clock()
        self.__running = False

        background_tile_img = pygame.image.load("../res/snow.png").convert()
        background_tile = pygame.transform.scale(background_tile_img, (GRID_SIZE, GRID_SIZE))
        self.__background = pygame.surface.Surface((window_width, window_height))
        for y in range(grid_height):
            for x in range(grid_width):
                self.__background.blit(background_tile, (x * GRID_SIZE, y * GRID_SIZE))

    def run(self):
        self.__running = True
        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False

            delta_time = self.__clock.tick(60) / 1000.0

            self.update()
            self.render(delta_time)

    def update(self):
        pass

    def render(self, delta_time):
        pygame.display.get_surface().blit(self.__background, (0, 0))