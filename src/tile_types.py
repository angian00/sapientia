from typing import Tuple

import numpy as np  # type: ignore


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
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

floor = new_tile(
	walkable=True,
	transparent=True,
	dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
	light=(ord(" "), (255, 255, 255), (200, 180, 50)),
)

wall = new_tile(
	walkable=False,
	transparent=False,
	dark=(ord(" "), (255, 255, 255), (0, 0, 100)),
	light=(ord(" "), (255, 255, 255), (130, 110, 50)),
)

down_stairs = new_tile(
   walkable=True,
   transparent=True,
   dark=(ord(">"), (0, 0, 100), (50, 50, 150)),
   light=(ord(">"), (255, 255, 255), (200, 180, 50)),
)




def darken(color):
	darken_factor = 0.75

	return (
		int(color[0]*darken_factor),
		int(color[1]*darken_factor),
		int(color[2]*darken_factor),
	)


terrain_info = [
	(" ", (165,165,141)),
	(" ", (183,183,164)),
	("\u2229", (107,112,92)),
	("\u2229", (203,153,126)),
	("\u25B2", (221,190,169)),
]

terrain_tiles = []
for t in terrain_info:
	t_char = t[0]
	t_color = t[1]
	t_color_dark = darken(t_color)

	terrain_tiles.append(new_tile(
		walkable=True,
		transparent=True,
		dark=(ord(t_char), darken(t_color_dark), t_color_dark),
		light=(ord(t_char), t_color_dark, t_color),
	)
)

terrain_plains_1  = terrain_tiles[0]
terrain_plains_2  = terrain_tiles[1]
terrain_hills_1   = terrain_tiles[2]
terrain_hills_2   = terrain_tiles[3]
terrain_mountains = terrain_tiles[4]
