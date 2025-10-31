import pygame.sprite
from settings import *
class entity(pygame.sprite.Sprite):
    def __init__(self , pos, frames , groups , facing_direction):
        super().__init__(groups)
        self.z = world_layers['main']
        self.frame_index , self.frames = 0 , frames
        self.facing_direction = facing_direction
        self.direction = vector(0, 0)
        self.speed = 60
        self.blocked = False
        self.image = self.frames[self.getstate()][self.frame_index]
        self.rect = self.image.get_frect(center = pos)
        self.hitbox = self.rect.inflate(-self.rect.width/2 , -16)
        self.y_sort = self.rect.centery
    def animate(self , dt):
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[self.getstate()][int(self.frame_index % len(self.frames[self.getstate()]))]
    def update(self , dt):
        self.animate(dt)
    def getstate(self):
        moving = bool(self.direction)
        if moving:
            if self.direction.x != 0:
                self.facing_direction = 'right' if self.direction.x > 0 else 'left'
            if self.direction.y != 0:
                self.facing_direction = 'down' if self.direction.y > 0 else 'up'
        return f'{self.facing_direction}{'' if moving else '_idle'}'


    def change_facing_direction(self, target_pos):
        relation = vector(target_pos) - vector(self.rect.center)
        if abs(relation.y) < 30:
            self.facing_direction = 'right' if relation.x > 0 else 'left'
        else:
            self.facing_direction = 'down' if relation.y > 0 else 'up'

    def block(self):
        self.blocked = True
        self.direction = vector(0, 0)
    def unblock(self):
        self.blocked = False
class Player(entity):
    def __init__(self , pos ,frames, groups , collision_spirtes , facing_direction):
        super().__init__(pos , frames , groups , facing_direction)
        self.collison_sprites = collision_spirtes
        self.noticed = False
    def input(self):
        input = pygame.key.get_pressed()
        input_vector = vector(0,0)
        if input[pygame.K_UP]:
            input_vector.y -= 1
        elif input[pygame.K_DOWN]:
            input_vector.y += 1
        elif input[pygame.K_LEFT]:
            input_vector.x -= 1
        elif input[pygame.K_RIGHT]:
            input_vector.x += 1
        self.direction = input_vector
    def move(self , dt):
        self.rect.centerx += self.direction.x * self.speed * dt
        self.hitbox.centerx = self.rect.centerx
        self.collisions('horizontal')
        self.rect.centery += self.direction.y * self.speed * dt
        self.hitbox.centery = self.rect.centery
        self.collisions('vertical')
    def collisions(self , axis):
        for sprite in self.collison_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if axis == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                else:
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    else:
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery
    def update(self , dt):
        self.y_sort = self.rect.centery
        if not self.blocked:
            self.input()
            self.move(dt)
        self.animate(dt)
