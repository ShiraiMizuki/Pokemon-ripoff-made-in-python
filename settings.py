import pygame
from pygame.math import Vector2 as vector
from sys import exit
window_height , window_width = 160 , 240

tile_size = 16
ANIMATION_SPEED = 13
world_layers = {
'grass' : 0,
'main':1,
'top':2
}