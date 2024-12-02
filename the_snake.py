from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


start_pos = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (150, 150, 255)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (150, 0, 150)

# Цвет змейки
SNAKE_COLOR = (204, 255, 255)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.

class GameObject:
    """Описываем родительский класс GameObject, который отвечает
    за атрибуты всех объектов
    """

    def __init__(self) -> None:
        self.position = (0, 0)
        self.body_color = None

    def draw(self):
        """Метод, который предназначен для переопределения
        в дочерних классах
        """
        pass


class Apple(GameObject):
    """Класс, описывающий поведение яблока в коде"""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Функция, которая устанавливает начальную позицию яблока"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Функция, которая отрисовывает яблоко на игровой поверхности"""
        rect = (pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейка, описывает поведение змейки и её вид"""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [start_pos]
        self.direction = (1, 0)
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Функция, которая обновляет направление движения змейки"""
        if self.next_direction:
            if ((self.direction[0] * -1, self.direction[1] * -1)
               != self.next_direction):
                self.direction = self.next_direction
                self.next_direction = None

    def move(self):
        """Функция, отвечающая за движение змейки"""
        x, y = self.get_head_position()
        new_x = (x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_y = (y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        if len(self.positions) > self.length:
            self.positions.pop()
        elif (new_x, new_y) in self.positions:
            return self.reset()
        elif x >= GRID_WIDTH or x < 0 or y >= GRID_HEIGHT or y < 0:
            x, y = abs(x), abs(y)
        self.positions.insert(0, (new_x, new_y))

    def draw(self):
        """Функция, которая отрисовывает змейку на экране"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        """Отрисовка головы змейки"""
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        """Затирание последнего сегмента"""
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Функция, которая возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """Функция, сбрасывающая текущее значение змейки"""
        self.length = 1
        self.positions = [start_pos]
        self.direction = choice((0, -1), (0, 1), (-1, 0), (1, 0))


def main():
    """Функция, описывающая основное взаимодействие кода между собой"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    running = True

    while running:
        screen.fill(BOARD_BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.next_direction = UP
                elif event.key == pygame.K_DOWN:
                    snake.next_direction = DOWN
                elif event.key == pygame.K_LEFT:
                    snake.next_direction = LEFT
                elif event.key == pygame.K_RIGHT:
                    snake.next_direction = RIGHT

        snake.update_direction()

        snake.move()

        # Проверка на поедание яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        clock.tick(SPEED)
        apple.draw()
        # for position in snake.positions:
        snake.draw()
        pygame.display.update()
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# 
# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
