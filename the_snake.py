"""Компьютерная игра 'Змейка'.

Написана на языке Python
"""
from random import choice
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
ALL_FIELD = set(
    (x * GRID_SIZE, y * GRID_SIZE)
    for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)
)

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


class GameObject:
    """Родительский класс.

    Отвечает за атрибуты всех объектов
    """

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR) -> None:
        """Инициализатор родительского класса."""
        self.position = (0, 0)
        self.body_color = body_color

    def draw(self):
        """Метод для переопределения в дочерних классах."""


class Apple(GameObject):
    """Класс, описывающий поведение яблока в коде."""

    def __init__(self, color=APPLE_COLOR, occupied_cells=None) -> None:
        super().__init__(color)
        """Инициализатор класса яблоко."""
        if occupied_cells is None:
            occupied_cells = []
        self.randomize_position(occupied_cells)

    def randomize_position(self, occupied_cells):
        """Функция, которая устанавливает начальную позицию яблока."""
        self.position = choice(tuple(ALL_FIELD - set(occupied_cells)))

    def draw(self):
        """Функция, которая отрисовывает яблоко на игровой поверхности."""
        rect = (pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейка, описывает поведение змейки и её вид."""

    def __init__(self, color=SNAKE_COLOR):
        super().__init__(color)
        """Инициализатор класса змейка."""
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [start_pos]
        self.direction = UP
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Функция, которая обновляет направление движения змейки."""
        if self.next_direction:
            direction_x, direction_y = self.direction
            if ((direction_x * -1, direction_y * -1)
               != self.next_direction):
                self.direction = self.next_direction
                self.next_direction = None

    def move(self):
        """Функция, отвечающая за движение змейки."""
        dx, dy = self.get_head_position()
        direction_x, direction_y = self.direction
        new_x = (dx + direction_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (dy + direction_y * GRID_SIZE) % SCREEN_HEIGHT
        self.positions.insert(0, (new_x, new_y))
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Функция, которая отрисовывает змейку на экране.

        Отрисовываем голову и затираем хвост
        """
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = (pygame.Rect(self.get_head_position(),
                     (GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Функция, которая возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Функция, сбрасывающая текущее значение змейки."""
        self.length = 1
        self.positions = [start_pos]
        self.direction = choice([UP, DOWN, RIGHT, LEFT])
        self.last = None


def handle_keys(snake):
    """Обработка действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif (event.key == pygame.K_LEFT
                    and snake.direction != RIGHT):
                snake.next_direction = LEFT
            elif (event.key == pygame.K_RIGHT
                    and snake.direction != LEFT):
                snake.next_direction = RIGHT


def main():
    """Функция, описывающая основное взаимодействие кода между собой."""
    # Инициализация PyGame:
    pygame.init()
    # Тут создаём экземпляры классов.
    screen.fill(BOARD_BACKGROUND_COLOR)
    snake = Snake()
    apple = Apple(occupied_cells=snake.positions)
    running = True

    while running:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.update_direction()

        # Проверка на поедание яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()
        pygame.display.update()
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
