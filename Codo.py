import pygame
import random
import sys

# Ініціалізація Pygame
pygame.init()

# Налаштування екрану та кольорів
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Кодонавт: Космічна Пригода")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Шрифти
font = pygame.font.SysFont("Arial", 30)

# Клас для корабля
class SpaceShip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

# Клас для ворогів
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 50)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(2, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, WIDTH - 50)

# Клас для проектилів
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 7

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

# Функція для відображення тексту на екрані
def draw_text(text, x, y, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Головна функція гри
def game():
    clock = pygame.time.Clock()

    # Групи спрайтів
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    # Створення космічного корабля
    player = SpaceShip()
    all_sprites.add(player)

    # Створення ворогів
    for _ in range(5):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    score = 0
    running = True
    while running:
        screen.fill(BLACK)

        # Обробка подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)

        # Оновлення стану спрайтів
        keys = pygame.key.get_pressed()
        all_sprites.update(keys)

        # Перевірка зіткнень між кулями та ворогами
        for bullet in bullets:
            hits = pygame.sprite.spritecollide(bullet, enemies, True)
            for hit in hits:
                score += 1
                bullet.kill()
                # Створення нового ворога після знищення
                new_enemy = Enemy()
                all_sprites.add(new_enemy)
                enemies.add(new_enemy)

        # Виведення тексту на екран
        draw_text(f"Score: {score}", 10, 10, WHITE)

        # Малювання спрайтів на екрані
        all_sprites.draw(screen)

        # Оновлення екрану
        pygame.display.flip()

        # Обмеження кадрів в секунду
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game()
