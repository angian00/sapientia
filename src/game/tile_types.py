from __future__ import annotations
from typing import Tuple, List, Dict, Any

import ui.color


class Tile:
	def __init__(self, ch: str, fg_color: str, bg_color: str):
		self.ch = ch
		self.fg_color = fg_color
		self.bg_color = bg_color


class Terrain:
	def __init__(self, walkable: bool, transparent: bool, dark_tile: Tile, light_tile: Tile):
		self.walkable = walkable
		self.transparent = transparent
		self.dark_tile = dark_tile
		self.light_tile = light_tile



# SHROUD represents unexplored, unseen tiles
SHROUD = Tile("\u2591", "#909090", ui.color.black)

floor = Terrain(True, True,
	Tile(".", ui.color.black, ui.color.floor_dark),
	Tile(".", ui.color.black, ui.color.floor_light),
)

wall = Terrain(False, False,
	Tile(" ", ui.color.wall_dark, ui.color.wall_dark),
	Tile(" ", ui.color.wall_light, ui.color.wall_light),
)

down_stairs = Terrain(True, True,
   Tile(">", "#000064", "#323296"),
   Tile(">", ui.color.white, "#c8b432"),
)



terrain_info: List[Tuple[str, str]] = [
	(" ", ui.color.terrain_plains_1),
	(" ", ui.color.terrain_plains_2),
	("\u2229", ui.color.terrain_hills_1),
	("\u2229", ui.color.terrain_hills_2),
	("\u25B2", ui.color.terrain_mountains),
]

terrains: List[Terrain] = []
for t in terrain_info:
	t_char = t[0]
	t_color = t[1]
	t_color_dark = "dark " + t_color
	t_color_darker = "darker " + t_color

	terrains.append(Terrain(True, True,
		Tile(t_char, t_color_darker, t_color_dark),
		Tile(t_char, t_color_dark, t_color),
		#Tile(t_char, "black", "green"),
		#Tile(t_char, "blue", "red"),
	))


terrain_plains_1  = terrains[0]
terrain_plains_2  = terrains[1]
terrain_hills_1   = terrains[2]
terrain_hills_2   = terrains[3]
terrain_mountains = terrains[4]
