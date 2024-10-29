import pygame
import random
import sys

# Ustawienia
WIDTH, HEIGHT = 800, 600  # Zwiększona mapa
GRID_SIZE = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)  # Kolor jedzenia
RED = (255, 0, 0)    # Kolor miny
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)  # Kolor głowy węża
BLUE = (0, 0, 255)      # Kolor ogona węża

# Klasa Węża
class Snake:
    def __init__(self):
        self.body = [(100, 100)]  # Zmniejszona początkowa długość węża
        self.direction = (GRID_SIZE, 0)
        self.grow = False

    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, direction):
        self.direction = direction

    def eat(self):
        self.grow = True

    def collides_with_self(self):
        return self.body[0] in self.body[1:]

    def collides_with_bounds(self):
        head_x, head_y = self.body[0]
        return head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT

    def draw(self, surface):
        # Rysowanie głowy węża
        head_x, head_y = self.body[0]
        pygame.draw.polygon(surface, YELLOW, [
            (head_x + GRID_SIZE // 2, head_y),  # Wierzchołek góry
            (head_x, head_y + GRID_SIZE),  # Lewy dolny wierzchołek
            (head_x + GRID_SIZE, head_y + GRID_SIZE)  # Prawy dolny wierzchołek
        ])
        # Rysowanie ogona
        for segment in self.body[1:]:
            pygame.draw.rect(surface, BLUE, (*segment, GRID_SIZE, GRID_SIZE))

# Klasa Jedzenia
class Food:
    def __init__(self):
        self.spawn()

    def spawn(self):
        self.position = (random.randint(0, (WIDTH // GRID_SIZE - 1)) * GRID_SIZE,
                         random.randint(0, (HEIGHT // GRID_SIZE - 1)) * GRID_SIZE)

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, (*self.position, GRID_SIZE, GRID_SIZE))

# Klasa Miny
class Mine:
    def __init__(self, position=None):
        self.position = position if position else self.spawn()

    def spawn(self):
        return (random.randint(0, (WIDTH // GRID_SIZE - 1)) * GRID_SIZE,
                random.randint(0, (HEIGHT // GRID_SIZE - 1)) * GRID_SIZE)

    def draw(self, surface):
        # Rysowanie trójkąta
        pygame.draw.polygon(surface, RED, [
            (self.position[0] + GRID_SIZE // 2, self.position[1]),  # Wierzchołek góry
            (self.position[0], self.position[1] + GRID_SIZE),  # Lewy dolny wierzchołek
            (self.position[0] + GRID_SIZE, self.position[1] + GRID_SIZE)  # Prawy dolny wierzchołek
        ])

# Funkcja generująca miny
def generate_mines(snake_body, num_mines=6):
    mines = []
    while len(mines) < num_mines:
        position = (random.randint(0, (WIDTH // GRID_SIZE - 1)) * GRID_SIZE,
                    random.randint(0, (HEIGHT // GRID_SIZE - 1)) * GRID_SIZE)
        while position in snake_body or position in [mine.position for mine in mines]:  # Upewnij się, że mina nie pojawi się na wężu ani w miejscu innej miny
            position = (random.randint(0, (WIDTH // GRID_SIZE - 1)) * GRID_SIZE,
                        random.randint(0, (HEIGHT // GRID_SIZE - 1)) * GRID_SIZE)
        mines.append(Mine(position))
    return mines

# Klasa Komputerowego Węża
class ComputerSnake(Snake):
    def __init__(self):
        super().__init__()
        self.direction = (GRID_SIZE, 0)  # Domyślny kierunek

    def auto_move(self, food_position):
        head_x, head_y = self.body[0]

        # Prosta logika sterowania komputerem
        if head_x < food_position[0]:
            self.change_direction((GRID_SIZE, 0))
        elif head_x > food_position[0]:
            self.change_direction((-GRID_SIZE, 0))
        elif head_y < food_position[1]:
            self.change_direction((0, GRID_SIZE))
        elif head_y > food_position[1]:
            self.change_direction((0, -GRID_SIZE))

# Funkcja menu
def menu(screen):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "play"  # Zagraj
                elif event.key == pygame.K_2:
                    return "difficulty"  # Ustaw poziom trudności
                elif event.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()  # Wyjdź

        # Wyświetl menu
        screen.fill(BLACK)
        font = pygame.font.Font(None, 36)
        text = font.render("Snake Game", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4))

        # Opcje
        options = ["1. Zagraj (domyślnie poziom łatwy)", "2. Ustaw poziom trudności", "3. Wyjdź"]
        for i, option in enumerate(options):
            text = font.render(option, True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4 + 50 + i * 40))

        pygame.display.flip()

# Funkcja ustawiania poziomu trudności
def set_difficulty(screen):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 5  # Łatwy poziom
                elif event.key == pygame.K_2:
                    return 10  # Średni poziom
                elif event.key == pygame.K_3:
                    return 15  # Trudny poziom
                elif event.key == pygame.K_ESCAPE:
                    return None  # Powrót do menu

        # Wyświetl menu z poziomami trudności
        screen.fill(BLACK)
        font = pygame.font.Font(None, 36)
        text = font.render("Wybierz poziom trudności", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4))

        options = ["1. Łatwy", "2. Średni", "3. Trudny", "ESC. Powrót do menu"]
        for i, option in enumerate(options):
            text = font.render(option, True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4 + 50 + i * 40))

        pygame.display.flip()

# Funkcja końca gry
def game_over(screen):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render("GAME OVER", True, RED)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(6000)  # Zmiana z 6 na 3 sekundy
    return

# Funkcja główna
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    mines = generate_mines(snake.body)  # Przeniesiono na górę
    difficulty_level = 5  # Domyślnie łatwy poziom
    level_speed = difficulty_level

    while True:
        choice = menu(screen)

        if choice == "play":
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP and snake.direction != (0, GRID_SIZE):
                            snake.change_direction((0, -GRID_SIZE))
                        elif event.key == pygame.K_DOWN and snake.direction != (0, -GRID_SIZE):
                            snake.change_direction((0, GRID_SIZE))
                        elif event.key == pygame.K_LEFT and snake.direction != (GRID_SIZE, 0):
                            snake.change_direction((-GRID_SIZE, 0))
                        elif event.key == pygame.K_RIGHT and snake.direction != (-GRID_SIZE, 0):
                            snake.change_direction((GRID_SIZE, 0))

                # Ruch węża
                snake.move()

                # Sprawdzanie kolizji
                if snake.collides_with_self() or snake.collides_with_bounds():
                    game_over(screen)
                    break  # Wraca do menu po śmierci

                # Sprawdzanie zjedzenia jedzenia
                if snake.body[0] == food.position:
                    snake.eat()
                    food.spawn()
                    if len(mines) < 6:  # Dodaj nową minę, jeśli jest mniej niż 6
                        mines.append(Mine())

                # Rysowanie na ekranie
                screen.fill(BLACK)
                snake.draw(screen)
                food.draw(screen)
                for mine in mines:
                    mine.draw(screen)

                pygame.display.flip()
                clock.tick(level_speed)

        elif choice == "difficulty":
            difficulty_level = set_difficulty(screen)
            if difficulty_level:
                level_speed = difficulty_level
                if difficulty_level == 15:  # Tylko w trybie trudnym
                    computer_snake = ComputerSnake()  # Dodanie komputera
                else:
                    computer_snake = None  # Brak komputera w innych trybach

if __name__ == "__main__":
    main()
