import random
import os
import json
from settings import *

POKEMON_DATA = {
    'pidgey': {
        'types': ['normal', 'flying'],
        'stats': {
            'max_hp': lambda level: (24 + level) * 3,
            'atk': lambda level: (20 + level) * 2,
            'def': lambda level: (17 + level) * 2,
            'spatk': lambda level: (30 + level) * 2,
            'spdef': lambda level: (40 + level) * 2,
            'speed': lambda level: (44 + level) * 2
        },
        'moves': [
            {'name': 'peck', 'type': 'normal', 'power': 25, 'accuracy': 95, 'pp': 15}
        ]
    },
    'rattata': {
        'types': ['normal'],
        'stats': {
            'max_hp': lambda level: (24 + level) * 3,
            'atk': lambda level: (20 + level) * 2,
            'def': lambda level: (12 + level) * 2,
            'spatk': lambda level: (21 + level) * 2,
            'spdef': lambda level: (15 + level) * 2,
            'speed': lambda level: (55 + level) * 2
        },
        'moves': [
            {'name': 'tackle', 'type': 'normal', 'power': 20, 'accuracy': 100, 'pp': 15}
        ]
    },
}

class Pokemon:
    def __init__(self, name, types, base_stats, moves, level):
        self.name = name
        self.types = types
        self.base_stats = base_stats
        self.moves = moves
        self.level = level
        self.xp = 0
        self.current_hp = base_stats['max_hp']  # Initialize current_hp
        self.xp_to_level = lambda level: level * 100

    def display_info(self):
        """Display the Pokémon's information."""
        print(f"Pokémon: {self.name.capitalize()}")
        print(f"Level: {self.level}")
        print(f"Types: {', '.join(self.types).capitalize()}")
        print(f"Stats: {self.base_stats}")
        print(f"Moves: {[move.name for move in self.moves]}")
        print(f"Current HP: {self.current_hp}")

class Move:
    def __init__(self, name, move_type, power, accuracy, pp):
        self.name = name
        self.type = move_type
        self.power = power
        self.accuracy = accuracy
        self.pp = pp

def create_pokemon(pokemon_name):
    if pokemon_name.lower() not in POKEMON_DATA:
        print(f"Pokemon '{pokemon_name}' not found")
        return None

    pokemon_data = POKEMON_DATA[pokemon_name.lower()]
    level = random.randint(3, 6)
    base_stats = {
        stat: calc(level)
        for stat, calc in pokemon_data['stats'].items()
    }
    moves = [
        Move(move['name'], move['type'], move['power'], move['accuracy'], move['pp'])
        for move in pokemon_data['moves']
    ]
    created_pokemon = Pokemon(
        name=pokemon_name.lower(),
        types=pokemon_data['types'],
        base_stats=base_stats,
        moves=moves,
        level=level
    )
    return created_pokemon

class PlayerPokemonManager:
    def __init__(self, save_file='player_pokemon.json'):
        self.save_file = save_file
        if not os.path.exists(self.save_file):
            self.initialize_starter()

    def initialize_starter(self):
        starter_pokemon = create_pokemon('pidgey')
        starter_pokemon.level = 5
        starter_pokemon.xp = 0
        starter_data = {
            'name': starter_pokemon.name,
            'level': starter_pokemon.level,
            'current_hp': starter_pokemon.base_stats['max_hp'],
            'moves': [move.name for move in starter_pokemon.moves],
            'xp': starter_pokemon.xp
        }
        self.save_to_json([starter_data])

    def load_player_pokemon(self):
        with open(self.save_file, 'r') as f:
            saved_data = json.load(f)
        player_pokemon = []
        for pokemon_data in saved_data:
            pokemon = create_pokemon(pokemon_data['name'])
            pokemon.level = pokemon_data['level']
            pokemon.current_hp = pokemon_data.get('current_hp', pokemon.base_stats['max_hp'])
            player_pokemon.append(pokemon)
        return player_pokemon

    def save_to_json(self, pokemon_list):
        save_data = []
        for pokemon in pokemon_list:
            if hasattr(pokemon, 'name'):
                save_data.append({
                    'name': pokemon.name,
                    'level': pokemon.level,
                    'current_hp': getattr(pokemon, 'current_hp', pokemon.base_stats['max_hp']),
                    'moves': [move.name for move in pokemon.moves],
                    'xp': pokemon.xp
                })
            else:
                save_data.append(pokemon)
        with open(self.save_file, 'w') as f:
            json.dump(save_data, f, indent=4)