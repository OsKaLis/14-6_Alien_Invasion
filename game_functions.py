import sys
import pygame
from time import sleep

from bullet import Bullet
from alien import Alien

def sours_fon(name_file):
    """
    Проигррование фоновой музыки для игры
    """
    pygame.mixer.music.load(name_file)
    pygame.mixer.music.play(-1)


def fire_bullet(ai_settings, screen, ship, bullets):
    """
    Выпускает пулю, если максимум ещё не достигнут.
    """
    # СозданиеНовой пули и включении её в группу bullet
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """
    Рефгирет на нажатие клавишь.
    """
    if event.key == pygame.K_q:
        sys.exit()
    # Нажата Правая стрелка (Двигаемся в права)
    elif event.key == pygame.K_RIGHT:
        ship.moving_right = True
    # Нажата левая стрелка (Двигаемся в лево)
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # СозданиеНовой пули и включении её в группу bullet
        fire_bullet(ai_settings, screen, ship, bullets)

def check_keyup_events(event, ship):
    """
    Реагирует на отпускание клавишь.
    """
    # Отжата правая клавиша (Перестаём двигаться в права)
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    # Отжата левая клавиша (Перестаём двигаться в лево)
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb,
    play_button, ship, bullets, aliens):
    """
    Отслеживаем события клавиатуры и мыши
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        # Проверяем нажатие мышки на область кнопки (Для запуска игры)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
        aliens, bullets, mouse_x, mouse_y):
    """ Запускаем новую игру при нажатии кнопри (Играть) """
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Сброс игровых настроек.
        ai_settings.initialize_dynamic_settings()
        if play_button.rect.collidepoint(mouse_x, mouse_y):
            # Указатель мыши скрывается
            pygame.mouse.set_visible(False)
            # Сброс игровой статистики.
            stats.reset_stats()
            stats.game_active = True
            # Сброс изображений счетов и уровня.
            sb.prep_score()
            sb.prep_high_score()
            sb.prep_level()
            sb.prep_ships()

            # Очистка списка пришельцев и пуль
            aliens.empty()
            bullets.empty()

            # Создание нового флота и размещение корабля в центре.
            create_fleet(ai_settings, screen, ship, aliens)
            ship.center_ship()

def update_screen(ai_settings, screen,
        stats, sb, ship, aliens, bullets, play_button):
    """
    Обновляет изображения на экране и отображает новый экран.
    """
    # При каждом проходе цикла перерисовывается экрана.
    screen.fill(ai_settings.bg_color)
    # Все пули выводятся позади изображения коробля и прищельцев.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # рисуем корабль
    ship.blitme()

    # Рисуем пришельца.
    #alien.blitme()
    aliens.draw(screen)

    # Вывод счета.
    sb.show_score()

    # Кнопка Play отображается в том случае, если игра неактивна.
    if not stats.game_active:
        play_button.draw_button()

    # Отображение последнего прорисованного экранна.
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens,
        bullets):
    """
    Обновляет позиции пули и уничтожает старые пули.
    """
    bullets.update()
    # Удаление пуль, вышедших за край экрана.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #print(len(bullets))

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    Обработка коллизий пуль с пришельцами.
    """
    # Проверка попадания в пришельца
    # При обнаружении попадания удалить пулю и пришельца.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
        sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Если весь флот уничтожен, начинается следующий уровень.
        bullets.empty()
        ai_settings.increase_speed()
        # Увеличение уровня.
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
    """
    Вычисляем количество пришельцев в ряду.
    """
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """
    Определяет количество рядов, помещающихся на экране.
    """
    available_space_y = (ai_settings.screen_height -
                                    (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """
    Создание пришельца и размещение его в ряду.
    """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """
    Создание флота пришельца.
    """
    # Создание пришельца и вычисление количества пришельцев в ряду.
    # Интервал между соседними пришельцами равен одной ширине пришельца.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Создание флота пришельцев
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # Создание пришельца и разместить его в ряду
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    Проверяет, достиг ли флот края экранна,
    после чего обновляет позиции всех пришельцев во флоте.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Проверка коллизий "пришелец-корабль"
    if pygame.sprite.spritecollideany(ship, aliens):
        # print('Ship hit !!!')
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # Проверка пришельцев, добравшихся до нижнего края экрана.
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)


def check_fleet_edges(ai_settings, aliens):
    """
    Реагирует на достижение пришельцем края экрана.
    """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """
    Отпускает весь флот и меняет направление флота.
    """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    Обрабатывает столковение коробля с пришельцем.
    """
    if stats.ships_left > 0:
        # Уменьшение ships_left.
        stats.ships_left -= 1

        # Обновление игровой информации.
        sb.prep_ships()

        # Очистка списка пришельцев и пуль.
        aliens.empty()
        bullets.empty()

        # Создание нового флота и рзмещение коробля в центре.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Пауза.
        sleep(0.7)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """ Проверяет, добрались ли пришельцы до нижнго края экрана. """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Происходит то же, чо при столкновении с кароблём.
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break

def check_high_score(stats, sb):
    """
    Проверяет, появился ли новый рекорд.
    """
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
