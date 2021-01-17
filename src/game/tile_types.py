from __future__ import annotations
from typing import Tuple, List

import numpy as np  # type: ignore

import ui.color


# Tile graphics structured type compatible with Console.tiles_rgb
graphic_dt = np.dtype(
	[
		("ch", np.int32),  # Unicode codepoint
		("fg", "U"),
		("bg", "U"),
	]
)

# Tile struct used for statically defined tile data
tile_dt = np.dtype(
	[
		("walkable", np.bool),  # True if this tile can be walked over
		("transparent", np.bool),  # True if this tile doesn't block FOV
		("dark", graphic_dt),  # Graphics for when this tile is not in FOV
		("light", graphic_dt),  # Graphics for when the tile is in FOV
	]
)


def new_tile(
	*,  # Enforce the use of keywords, so that parameter order doesn't matter
	walkable: int,
	transparent: int,
	dark: Tuple[int, str, str],
	light: Tuple[int, str, str],
) -> np.ndarray:
	"""Helper function for defining individual tile types """
	return np.array((walkable, transparent, dark, light), dtype=tile_dt)


# SHROUD represents unexplored, unseen tiles
SHROUD = np.array((ord("\u2591"), "#909090", ui.color.black), dtype=graphic_dt)

floor = new_tile(
	walkable=True,
	transparent=True,
	dark =(ord("."), ui.color.black, ui.color.floor_dark),
	light=(ord("."), ui.color.black, ui.color.floor_light),
)

wall = new_tile(
	walkable=False,
	transparent=False,
	dark =(ord(" "), ui.color.wall_dark, ui.color.wall_dark),
	light=(ord(" "), ui.color.wall_light, ui.color.wall_light),
)

down_stairs = new_tile(
   walkable=True,
   transparent=True,
   dark =(ord(">"), "#000064", "#323296"),
   light=(ord(">"), ui.color.white, "#c8b432"),
)




terrain_info: List[Tuple[str, str]] = [
	(" ", ui.color.terrain_plains_1),
	(" ", ui.color.terrain_plains_2),
	("\u2229", ui.color.terrain_hills_1),
	("\u2229", ui.color.terrain_hills_2),
	("\u25B2", ui.color.terrain_mountains),
]

terrain_tiles: List[np.ndarray] = []
for t in terrain_info:
	t_char = t[0]
	t_color = t[1]
	t_color_dark = "dark " + t_color
	t_color_darker = "darker " + t_color

	terrain_tiles.append(new_tile(
		walkable=True,
		transparent=True,
		dark=(ord(t_char), t_color_darker, t_color_dark),
		light=(ord(t_char), t_color_dark, t_color),
	)
)

terrain_plains_1  = terrain_tiles[0]
terrain_plains_2  = terrain_tiles[1]
terrain_hills_1   = terrain_tiles[2]
terrain_hills_2   = terrain_tiles[3]
terrain_mountains = terrain_tiles[4]
