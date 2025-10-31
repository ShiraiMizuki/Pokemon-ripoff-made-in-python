import random
import pygame
from settings import *
from sprites import Sprite, BorderSpritre, transition_sprites, grass_sprites
from characters import Player
from groups import Allsprites
from support import *
from pokemons import *
class wylew:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((window_width, window_height)    )
        pygame.display.set_caption('nintendo please dont sue me :3')
        self.clock = pygame.time.Clock()
        self.all_sprites = Allsprites()
        self.collision_spirtes = pygame.sprite.Group()
        self.transition_sprites = pygame.sprite.Group()
        self.player_pokemon_manager = PlayerPokemonManager()
        self.player_pokemon = self.player_pokemon_manager.load_player_pokemon()[0]
        self.grass_sprites = pygame.sprite.Group()
        self.pokemon_checking = False
        self.previous_position = None
        self.import_assets()
        self.setup(self.tmx_maps['gaymon'], 'start')
        self.transition_target = None
        self.tint_surf = pygame.Surface((self.display_surface.get_width(), self.display_surface.get_height()))
        self.tint_mode = 'untint'
        self.tint_progress = 0
        self.tint_direction = -1
        self.tint_speed = 400
        self.show_background = False

    def import_assets(self):
        self.tmx_maps = {
            'gaymon': load_pygame('graphics/maps/gaymon.tmx'),
            'hospital': load_pygame('graphics/maps/hospital.tmx'),
            'shop': load_pygame('graphics/maps/shop.tmx')
        }
        self.overworld = {
            'characters': all_character_import('graphics/Characters')
        }

    def setup(self, tmx_map, player_start_pos):
        for group in (self.all_sprites, self.collision_spirtes, self.transition_sprites):
            group.empty()
        # terrain
        for x, y, surf in tmx_map.get_layer_by_name('grass').tiles():
            Sprite((x * tile_size, y * tile_size), surf, self.all_sprites, world_layers['grass'])
        # objects
        for obj in tmx_map.get_layer_by_name('obj'):
            Sprite((obj.x, obj.y), obj.image, self.all_sprites, world_layers['grass'])
        # transitions
        for obj in tmx_map.get_layer_by_name('trans'):
            transition_sprites((obj.x, obj.y), (obj.width, obj.height), (obj.properties['target'], obj.properties['pos']), self.transition_sprites)
        for obj in tmx_map.get_layer_by_name('pokegrass'):
            grass_sprites((obj.x, obj.y), (obj.width, obj.height), (obj.properties['pokemon']), self.grass_sprites)
        # collisions
        for obj in tmx_map.get_layer_by_name('collisons'):
            BorderSpritre((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_spirtes)
        for obj in tmx_map.get_layer_by_name('characters'):
            if obj.name == 'player' and obj.properties['pos'] == player_start_pos:
                self.player = Player(
                    pos=(obj.x, obj.y),
                    frames=self.overworld['characters']['player'],
                    groups=self.all_sprites,
                    facing_direction=obj.properties['direction'],
                    collision_spirtes=self.collision_spirtes)
        # terrain top
        for x, y, surf in tmx_map.get_layer_by_name('top').tiles():
            Sprite((x * tile_size, y * tile_size), surf, self.all_sprites, world_layers['top'])

    def draw_text_animated(self, texts, color=(255, 255, 255), delay=30, base_font_size=12, text_xx=12, text_yy=120):
        screen_width = self.display_surface.get_width()
        screen_height = self.display_surface.get_height()
        width_scale = screen_width / 240
        height_scale = screen_height / 160
        font = pygame.font.Font("graphics/font/pokemon_fire_red.ttf", int(base_font_size * height_scale))
        text_x = int(text_xx * width_scale)
        text_y = int(text_yy * height_scale)
        clock = pygame.time.Clock()
        for text in texts:
            skip_requested = False
            current_text = ""
            char_surfaces = []
            for char in text:
                char_surface = font.render(char, True, color)
                char_surfaces.append(char_surface)
            for i, char_surface in enumerate(char_surfaces):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        skip_requested = True
                text_area = pygame.Rect(text_x, text_y, int(216 * width_scale), int(48 * height_scale))
                self.display_surface.blit(self.current_battle_bg, text_area, text_area)
                current_text += text[i]
                text_surface = font.render(current_text, True, color)
                self.display_surface.blit(text_surface, (text_x, text_y))
                pygame.display.flip()
                if skip_requested:
                    full_text = text
                    self.display_surface.blit(self.current_battle_bg, text_area, text_area)
                    text_surface = font.render(full_text, True, color)
                    self.display_surface.blit(text_surface, (text_x, text_y))
                    pygame.display.flip()
                    break
                clock.tick(1000 / delay)
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        waiting = False
            self.display_surface.blit(self.current_battle_bg, text_area, text_area)
            pygame.display.flip()
        return True

    def draw_text(self, text, color=(255, 255, 255), base_font_size=12, text_xx=12, text_yy=120):
        screen_width = self.display_surface.get_width()
        screen_height = self.display_surface.get_height()
        width_scale = screen_width / 240
        height_scale = screen_height / 160
        font = pygame.font.Font("graphics/font/pokemon_fire_red.ttf", int(base_font_size * height_scale))
        text_x = int(text_xx * width_scale)
        text_y = int(text_yy * height_scale)
        if not isinstance(text, str):
            text = str(text)
        text_surface = font.render(text, True, color)
        self.display_surface.blit(text_surface, (text_x, text_y))
        pygame.display.flip()

    def transition_check(self):
        sprites = [sprite for sprite in self.transition_sprites if sprite.rect.colliderect(self.player.hitbox)]
        if sprites:
            self.player.block()
            self.transition_target = sprites[0].target
            self.tint_mode = 'tint'

    def tint_screen(self, dt):
        if self.tint_mode == 'untint':
            self.tint_progress -= self.tint_speed * dt
        if self.tint_mode == 'tint':
            self.tint_progress += self.tint_speed * dt
            if self.tint_progress >= 255:
                self.tint_mode = 'untint'
                self.setup(self.tmx_maps[self.transition_target[0]], self.transition_target[1])
                self.transition_target = None
        self.tint_progress = max(0, min(self.tint_progress, 255))
        self.tint_surf.set_alpha(self.tint_progress)
        self.display_surface.blit(self.tint_surf, (0, 0))

    def show_pokemon_info(self, pokemon):
        pokemon.display_info()

    def pokemon_check(self):
        sprites = [sprite for sprite in self.grass_sprites if sprite.rect.colliderect(self.player.hitbox)]
        if sprites:
            current_tile = (self.player.hitbox.x // tile_size, self.player.hitbox.y // tile_size)
            if not self.pokemon_checking or current_tile != self.previous_tile:
                random1 = random.randint(0, 7)
                random2 = random.randint(0, 6)
                randompok = random.randint(0, 1)
                self.pokemon_list = sprites[0].target.split(',')
                self.pokemon_checking = True
                self.previous_tile = current_tile
                if random1 == random2:
                    selected_pokemon_name = self.pokemon_list[randompok]
                    wild_pokemon = create_pokemon(selected_pokemon_name)
                    self.all_sprites.empty()
                    self.collision_spirtes.empty()
                    self.transition_sprites.empty()
                    self.grass_sprites.empty()
                    screen_width = self.display_surface.get_width()
                    screen_height = self.display_surface.get_height()
                    scale_factor = min(screen_width // 240, screen_height // 160)
                    scale_factor = max(1, scale_factor)
                    battle_bg = pygame.Surface((240 * scale_factor, 160 * scale_factor))
                    battle_image = pygame.image.load('graphics/battle/background_grass.png').convert()
                    battle_image = pygame.transform.scale(battle_image, (240 * scale_factor, 160 * scale_factor))
                    battle_bg.blit(battle_image, (0, 0))
                    enemy_image = pygame.image.load(f'graphics/pokemons/{selected_pokemon_name}_enemy.png').convert_alpha()
                    enemy_image = pygame.transform.scale(enemy_image, (64 * scale_factor, 64 * scale_factor))
                    battle_bg.blit(enemy_image, (144 * scale_factor, 18 * scale_factor))
                    player_image = pygame.image.load(f'graphics/pokemons/{self.player_pokemon.name}_player.png').convert_alpha()
                    player_image = pygame.transform.scale(player_image, (64 * scale_factor, 64 * scale_factor))
                    battle_bg.blit(player_image, (32 * scale_factor, 56 * scale_factor))
                    final_surface = pygame.transform.scale(battle_bg, (screen_width, screen_height))
                    self.display_surface.blit(final_surface, (0, 0))
                    self.current_battle_bg = final_surface.copy()
                    self.draw_text_animated([f"A Wild {selected_pokemon_name.capitalize()} has appeared!"], color=(255, 255, 255), delay=35)
                    self.draw_text_animated([f"Go! {self.player_pokemon.name.capitalize()}!"], color=(255, 255, 255), delay=35)
                    action_menu = pygame.image.load('graphics/battle/actionmenu.png').convert_alpha()
                    action_menu = pygame.transform.scale(action_menu, (120 * scale_factor, 48 * scale_factor))
                    battle_bg.blit(action_menu, (120 * scale_factor, 112 * scale_factor))
                    health_bar_img = pygame.image.load('graphics/battle/playerbar.png').convert_alpha()
                    health_bar_img = pygame.transform.scale(health_bar_img, (104 * scale_factor, 37 * scale_factor))
                    battle_bg.blit(health_bar_img, (126 * scale_factor, 74 * scale_factor))
                    health_bar_enemy_img = pygame.image.load('graphics/battle/enemybar.png').convert_alpha()
                    health_bar_enemy_img = pygame.transform.scale(health_bar_enemy_img, (100 * scale_factor, 29 * scale_factor))
                    battle_bg.blit(health_bar_enemy_img, (14 * scale_factor, 15 * scale_factor))
                    final_surface = pygame.transform.scale(battle_bg, (screen_width, screen_height))
                    self.display_surface.blit(final_surface, (0, 0))
                    self.current_battle_bg = final_surface.copy()
                    self.draw_text(f"{selected_pokemon_name.upper()}", color=(64, 64, 64), base_font_size=13, text_xx=22, text_yy=17)
                    self.draw_text(f"{self.player_pokemon.name.upper()}", color=(64, 64, 64), base_font_size=13, text_xx=143, text_yy=76)
                    pygame.display.flip()
                    print("\nWild Pokémon Info:")
                    self.show_pokemon_info(wild_pokemon)
                    print("\nPlayer Pokémon Info:")
                    self.show_pokemon_info(self.player_pokemon)

                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    waiting = False
                        self.clock.tick(30)
                    self.setup(self.tmx_maps['gaymon'], 'start')
        else:
            self.pokemon_checking = False
            self.previous_tile = None

    def run(self):
        while True:
            dt = self.clock.tick(30) / 1000
            self.display_surface.fill('black')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.transition_check()
            self.pokemon_check()
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.player)
            self.tint_screen(dt)
            pygame.display.update()

if __name__ == '__main__':
    game = wylew()
    game.run()