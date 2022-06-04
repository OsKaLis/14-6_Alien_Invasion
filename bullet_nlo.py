import pygame
from pygame.sprite import Sprite

class BulletNLO(Sprite):
    """
    Класс для управления пулями, выпущенными пришельцем.
    """
    def __init__(self, ai_settings, screen, alien):
        """
        Создаёт обьект пули в текущей позиции корабля.
        """
        super().__init__()
        self.screen = screen

        # Создание пули в позиции (0, 0) и назначить правильной позиции.
        self.rect = pygame.Rect(0, 0, ai_settings.bulletNLO_width,
            ai_settings.bulletNLO_height)
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.top

        # Позиция пули хранения в вещественном форме.
        self.y = float(self.rect.y)

        self.color = ai_settings.bulletNLO_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """
        Перемещает пулю вверх по экрану.
        """
        # Обновление позиции пули в вещественном формате.
        self.y += self.speed_factor
        # Обновление позиции прямоугольника.
        self.rect.y = self.y

    def draw_bullet(self):
        """
        Вывод пули на экран.
        """
        pygame.draw.rect(self.screen, self.color, self.rect)
