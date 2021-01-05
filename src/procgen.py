from __future__ import annotations

import random
from typing import Iterator, List, Tuple, Dict, TYPE_CHECKING

import numpy as np
import tcod

import entity_factories
from game_map import GameMap
import tile_types


if TYPE_CHECKING:
	from engine import Engine
	from entity import Entity




max_n_sites = 8


def place_sites(map: GameMap, max_n_sites: int) -> None:
	n_sites = random.randint(int(max_n_sites/2), max_n_sites)

	for i in range(n_sites):
		x = random.randint(0, map.width - 1)
		y = random.randint(0, map.height - 1)

		if not any(entity.x == x and entity.y == y for entity in map.entities):
			#TODO: guarantee minimal distance
			new_site = entity_factories.monastery.spawn(map, x, y)
			if map.tiles[x, y] == tile_types.terrain_mountains:
				s_size = "small"
			elif map.tiles[x, y] == tile_types.terrain_hills_1 or map.tiles[x, y] == tile_types.terrain_hills_2:
				s_size = "medium"
			else:
				s_size = "large"

			new_site.size = s_size
			if s_size == "small":
				new_site.char = "+"
			elif s_size == "medium":
				new_site.char = "\u00B1"
			else:
				new_site.char = "\u263C"


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
	ogrid[0] *= 0.04
	ogrid[1] *= 0.04

	# Return the sampled noise from this grid of points
	samples = noise.sample_ogrid(ogrid)

	terrain_levels = ( 0, 0.4, 0.65, 0.85, .99, 1 )
	for x in range(map_width):
		for y in range(map_height):
			for i in range(len(terrain_levels)):
				if samples[x, y] < terrain_levels[i]:
					break

			new_map.tiles[x, y] = tile_types.terrain_tiles[i-1]

	place_sites(new_map, max_n_sites)
	player.place(int(new_map.width/2), int(new_map.height/2), new_map)

	return new_map

