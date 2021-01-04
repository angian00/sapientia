from __future__ import annotations

import random
from typing import Iterator, List, Tuple, Dict, TYPE_CHECKING

import numpy as np
import tcod

from game_map import GameMap
import tile_types


if TYPE_CHECKING:
	from engine import Engine
	from entity import Entity



def generate_wilderness(
	map_width: int,
	map_height: int,
	engine: Engine,
) -> GameMap:
	"""Generate a new outside map"""

	player = engine.player
	new_map = GameMap(engine, map_width, map_height, entities=[player])


	noise = tcod.noise.Noise(
		dimensions=2,
		algorithm=tcod.NOISE_SIMPLEX,
		implementation=tcod.noise.TURBULENCE,
		hurst=0.5,
		lacunarity=2.0,
		octaves=3,
		seed=None,
	)

	# Create an open multi-dimensional mesh-grid
	ogrid = [
		np.arange(map_width, dtype=np.float32),
		np.arange(map_height, dtype=np.float32)
	]

	# Scale the grid
	ogrid[0] *= 0.05
	ogrid[1] *= 0.05

	# Return the sampled noise from this grid of points
	samples = noise.sample_ogrid(ogrid)

	terrain_levels = ( 0, 0.4, 0.65, 0.83, .975, 1 )
	for x in range(map_width):
		for y in range(map_height):
			for i in range(len(terrain_levels)):
				if samples[x, y] < terrain_levels[i]:
					break

			new_map.tiles[x, y] = tile_types.terrain[i-1]

	player.place(int(new_map.width/2), int(new_map.height/2), new_map)

	return new_map

