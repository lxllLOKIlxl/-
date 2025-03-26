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

        # Оновлення космічного корабля (передаємо keys тільки космічному кораблю)
        keys = pygame.key.get_pressed()
        player.update(keys)

        # Оновлення інших спрайтів (без передачі keys)
        for sprite in all_sprites:
            if isinstance(sprite, Enemy) or isinstance(sprite, Bullet):
                sprite.update()

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
