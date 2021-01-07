from __future__ import annotations

import random
from typing import Iterator, List, Tuple, Dict, TYPE_CHECKING

import numpy as np

import tcod

import entity_factories
from game_map import GameMap
from entity import Site

import tile_types
import name_gen


if TYPE_CHECKING:
	from engine import Engine
	from entity import Entity


max_n_buildings = 8
building_min_size = 4
building_max_size = 8

max_n_sites = 10
min_site_distance = 5


class Rectangle:
	def __init__(self, x: int, y: int, width: int, height: int):
		self.x1 = x
		self.y1 = y
		self.x2 = x + width
		self.y2 = y + height

	@property
	def center(self) -> Tuple[int, int]:
		center_x = int((self.x1 + self.x2) / 2)
		center_y = int((self.y1 + self.y2) / 2)

		return center_x, center_y

	@property
	def inner(self) -> Tuple[slice, slice]:
		"""Return the inner area of this room as a 2D array index"""
		return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

	def intersects(self, other: Rectangle) -> bool:
		"""Return True if this room overlaps with another RecOutdoorBuilding"""
		return (
				self.x1 <= other.x2
				and self.x2 >= other.x1
				and self.y1 <= other.y2
				and self.y2 >= other.y1
		)



def place_sites(map: GameMap, max_n_sites: int) -> None:
	n_sites = random.randint(int(max_n_sites/2), max_n_sites)

	for i in range(n_sites):
		x = random.randint(0, map.width - 2)
		y = random.randint(0, map.height - 2)

		#if not any(entity.x == x and entity.y == y for entity in map.entities):

		#guarantee minimal distance between sites
		tile_is_ok = True
		for entity in map.entities:
			if (entity.x == x and entity.y == y) or \
				(isinstance(entity, Site) and \
				abs(entity.x - x) < min_site_distance and \
				abs(entity.y - y) < min_site_distance ):

				tile_is_ok = False
				break
		
		if not tile_is_ok:
			continue

		new_site = entity_factories.monastery.spawn(map, x, y)
		if map.tiles[x, y] == tile_types.terrain_mountains:
			s_size = "small"
		elif map.tiles[x, y] == tile_types.terrain_hills_1 or map.tiles[x, y] == tile_types.terrain_hills_2:
			s_size = "medium"
		else:
			s_size = "large"

		new_site.size = s_size
		new_site.name = "Monastery of " + name_gen.gen_name("sites")

		if s_size == "small":
			new_site.char = "+"
		elif s_size == "medium":
			new_site.char = "\u00B1"
		else:
			new_site.char = "\u263C"


def generate_wilderness_map(
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

	return new_map



def generate_local_map(
	map_width: int,
	map_height: int,
	engine: Engine,
) -> GameMap:
	"""Generate a new local outdoor map"""

	player = engine.player

	new_map = GameMap(engine, map_width, map_height, entities=[player])

	buildings: List[Rectangle] = []
	for b in range(max_n_buildings):
		b_width = random.randint(building_min_size, building_max_size)
		b_height = random.randint(building_min_size, building_max_size)

		x = random.randint(0, new_map.width - b_width - 1)
		y = random.randint(0, new_map.height - b_height - 1)

		new_b = Rectangle(x, y, b_width, b_height)

		if any(new_b.intersects(other_b) for other_b in buildings):
			# This building intersects, so go to the next attempt
			continue

		new_map.tiles[new_b.inner] = tile_types.wall

		buildings.append(new_b)

	return new_map
