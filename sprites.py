import pygame.sprite
from settings import *
class Sprite(pygame.sprite.Sprite):
    def __init__(self , pos, surf, groups, z = world_layers['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.z = z
        self.y_sort = self.rect.centery - 40
        self.hitbox = self.rect.copy()
class BorderSpritre(Sprite):
	def __init__(self , pos , surf , groups):
		super().__init__(pos , surf , groups)
		self.hitbox = self.rect.copy()
class transition_sprites(Sprite):
	def __init__(self , pos , size , target , groups):
		surf = pygame.Surface(size)
		super().__init__(pos , surf , groups)
		self.target = target
class grass_sprites(Sprite):
	def __init__(self , pos , size , target , groups):
		surf = pygame.Surface(size)
		super().__init__(pos , surf , groups)
		self.target = target

class AnimatedSprite(Sprite):
	def __init__(self, pos, frames, groups  , z = world_layers['main']):
		self.frame_index, self.frames = 0, frames
		super().__init__(pos, frames[self.frame_index], groups , z)

	def animate(self, dt):
		self.frame_index += ANIMATION_SPEED * dt
		self.image = self.frames[int(self.frame_index % len(self.frames))]

	def update(self, dt):
		self.animate(dt)