import pygame
from pygame.sprite import Sprite

class Blok(Sprite):
    """
    Класс, Блок или в частности метиорит.
    """
    def __init__(self, ai_settings, screen, ship):
        """
        Иницилизируем пришельца и задает его начальную позицию.
        """
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Загрусска изображения пришельца и назначения атрибута rect.
        self.image = pygame.image.load('images/blok.bmp')
        self.rect = self.image.get_rect()
        
    def blitme(self):
        """
        Показываем стену
        """
        self.screen.blit(self.image, self.rect)
