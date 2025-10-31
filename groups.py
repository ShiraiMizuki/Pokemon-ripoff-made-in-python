import pygame.sprite
from settings import *

class Allsprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()
    def draw(self , player):
        self.offset.x = -(player.rect.centerx - (self.display_surface.get_width() // 2))
        self.offset.y = -(player.rect.centery - (self.display_surface.get_height() // 2))
        grass_sprites = [sprite for sprite in self if sprite.z < world_layers['main']]
        main_sprites = sorted([sprite for sprite in self if sprite.z == world_layers['main']] , key = lambda sprite: sprite.y_sort)
        top_sprites = [sprite for sprite in self if sprite.z > world_layers['main']]
        for layer in (grass_sprites , main_sprites , top_sprites):
          for sprite in layer:
              self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
              if sprite == player and player.noticed:
                  rect = self.notice_surf.get_frect(midbottom=sprite.rect.midtop)
                  self.display_surface.blit(self.notice_surf, rect.topleft + self.offset)