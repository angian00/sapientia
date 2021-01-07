from typing import Tuple

import numpy as np  # type: ignore

import color


# Tile graphics structured type compatible with Console.tiles_rgb
graphic_dt = np.dtype(
	[
		("ch", np.int32),  # Unicode codepoint
		("fg", "3B"),  # 3 unsigned bytes, for RGB colors
		("bg", "3B"),
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
	dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
	light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
	"""Helper function for defining individual tile types """
	return np.array((walkable, transparent, dark, light), dtype=tile_dt)


# SHROUD represents unexplored, unseen tiles
SHROUD = np.array((ord("\u2591"), (144, 144, 144), (0, 0, 0)), dtype=graphic_dt)

floor = new_tile(
	walkable=True,
	transparent=True,
	dark=(ord(" "), (0, 0, 0), color.floor_dark),
	light=(ord(" "), (0, 0, 0), color.floor_light),
)

wall = new_tile(
	walkable=False,
	transparent=False,
	dark=(ord(" "), color.wall_dark, color.wall_dark),
	light=(ord(" "), color.wall_light, color.wall_light),
)

down_stairs = new_tile(
   walkable=True,
   transparent=True,
   dark=(ord(">"), (0, 0, 100), (50, 50, 150)),
   light=(ord(">"), (255, 255, 255), (200, 180, 50)),
)




terrain_info = [
	(" ", color.terrain_plains_1),
	(" ", color.terrain_plains_2),
	("\u2229", color.terrain_hills_1),
	("\u2229", color.terrain_hills_2),
	("\u25B2", color.terrain_mountains),
]

terrain_tiles = []
for t in terrain_info:
	t_char = t[0]
	t_color = t[1]
	t_color_dark = color.darken(t_color)

	terrain_tiles.append(new_tile(
		walkable=True,
		transparent=True,
		dark=(ord(t_char), color.darken(t_color_dark), t_color_dark),
		light=(ord(t_char), t_color_dark, t_color),
	)
)

terrain_plains_1  = terrain_tiles[0]
terrain_plains_2  = terrain_tiles[1]
terrain_hills_1   = terrain_tiles[2]
terrain_hills_2   = terrain_tiles[3]
terrain_mountains = terrain_tiles[4]
