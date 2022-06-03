import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """
        Инициализирует корабль и задает его начальную позицию.
        """
        super().__init__()
        self.screen = screen
        # Инициализируем корабль и задаём начальную позицию.
        self.ai_settings = ai_settings
        # Загруска изображения коробля и получение прямоугольника.
        self.image = pygame.image.load('images/kosmo_korablic.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # Каждый новый корабль появляется у нижнего края экрана.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # Сохраняем вещественной кординаты центра коробля
        self.center = float(self.rect.centerx)
        # Флаг перемещения
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """
        Обновляет пзицию коробля с учётом флага.
        """
        if self.moving_right and self.rect.right < self.screen_rect.right:
            #self.rect.centerx += 1
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            #self.rect.centerx -= 1
            self.center -= self.ai_settings.ship_speed_factor
        # Обновление атрибута rect на основании self.center.
        self.rect.centerx = self.center


    def blitme(self):
        """
        Рисуем корабль в текущей позиции.
        """
        self.screen.blit(self.image, self.rect)


    def center_ship(self):
        """ Размещает корабль в центре нижней стороны. """
        self.center = self.screen_rect.centerx
