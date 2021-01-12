from __future__ import annotations

import random
from typing import Iterator, List, Tuple, Dict, Optional, TYPE_CHECKING

import numpy as np # type: ignore

import tcod

import entity_factories
from game_map import GameMap
from entity import Site

import color
import tile_types
import name_gen
import church_gen
import ingredients
from metadata import SiteData


if TYPE_CHECKING:
	from engine import Engine
	from entity import Entity


max_n_buildings = 8
building_min_size = 4
building_max_size = 8

max_n_sites = 10
min_site_distance = 5
max_n_herbs = 30


class Rectangle:
	def __init__(self, x: int, y: int, width: int, height: int) -> None:
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
	def area(self) -> Tuple[slice, slice]:
		"""Return the area of this room as a 2D array index"""
		return slice(self.x1, self.x2), slice(self.y1, self.y2)

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



def place_sites(target_map: GameMap, n_sites: int) -> None:
	i = 0
	while i < n_sites:
		#leave a 1 tile padding around the borders
		x = random.randint(1, target_map.width - 2)
		y = random.randint(1, target_map.height - 2)

		#if not any(entity.x == x and entity.y == y for entity in target_map.entities):

		#guarantee minimal distance between sites
		tile_is_ok = True
		for entity in target_map.entities:
			if (entity.x == x and entity.y == y) or \
				(isinstance(entity, Site) and \
				abs(entity.x - x) < min_site_distance and \
				abs(entity.y - y) < min_site_distance ):

				tile_is_ok = False
				break
		
		if not tile_is_ok:
			continue

		site_data = generate_monastery_data(target_map.tiles[x, y])
		new_site = entity_factories.monastery.spawn(target_map, x, y)	
		new_site.name = site_data.name

		if site_data.size == "small":
			new_site.char = "+"
		elif site_data.size == "medium":
			new_site.char = "\u00B1"
		else:
			new_site.char = "\u263C"

		new_site.site_data = site_data

		i += 1


def place_herbs(target_map: GameMap, n_herbs: int) -> None:
	i = 0
	while i < n_herbs:
		x = random.randint(0, target_map.width - 1)
		y = random.randint(0, target_map.height - 1)

		if any(entity.x == x and entity.y == y for entity in target_map.entities):
			continue

		new_herb = entity_factories.herb.spawn(target_map, x, y)	
		new_herb.name = ingredients.gen_herb()

		i += 1


def place_npcs(target_map: GameMap, npcs: List[Dict[str, str]]) -> None:
	i = 0
	for npc in npcs:
		x = random.randint(0, target_map.width - 1)
		y = random.randint(0, target_map.height - 1)

		if  (not target_map.tiles["walkable"][x, y]) or \
			any(entity.x == x and entity.y == y for entity in target_map.entities):
			continue

		new_monk = entity_factories.monk.spawn(target_map, x, y)

		new_monk.name = npc["name"]

		if npc["order"] == "franciscan":
			new_monk.color = color.brown
		elif npc["order"] == "dominican":
			new_monk.color = color.black
		else:
			new_monk.color = color.white

		if "role" in npc:
			new_monk.role = npc["role"]

		i += 1


def generate_wilderness_map(map_width: int, map_height: int, engine: Engine) -> GameMap:
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

	n_sites = random.randint(int(max_n_sites/2), max_n_sites)
	place_sites(new_map, n_sites)

	n_herbs = random.randint(int(max_n_herbs/2), max_n_herbs)
	place_herbs(new_map, n_herbs)


	return new_map



def generate_local_map(map_width: int, map_height: int, engine: Engine, npcs: Optional[List[Dict[str, str]]]) -> GameMap:
	"""Generate a new local outdoor map"""

	player = engine.player

	new_map = GameMap(engine, map_width, map_height, entities=[player])

	n_buildings = random.randint(int(max_n_buildings/2), max_n_buildings)
	buildings: List[Rectangle] = []
	i = 0
	while i < n_buildings:
		b_width = random.randint(building_min_size, building_max_size)
		b_height = random.randint(building_min_size, building_max_size)

		x = random.randint(0, new_map.width - b_width - 1)
		y = random.randint(0, new_map.height - b_height - 1)

		new_b = Rectangle(x, y, b_width, b_height)

		if any(new_b.intersects(other_b) for other_b in buildings):
			# This building intersects, so go to the next attempt
			continue

		new_map.tiles[new_b.area] = tile_types.wall

		buildings.append(new_b)

		i += 1


	if npcs:
		place_npcs(new_map, npcs)

	return new_map


def generate_monastery_data(tile_type: np.ndarray) -> SiteData:
	#s_name = "monastery of " + name_gen.gen_name("sites")
	s_name = "monastery of " + church_gen.gen_church_name()
	
	s_order = random.choice(["dominican", "franciscan", "cistercian"])

	if tile_type == tile_types.terrain_mountains:
		s_size = "small"
	elif tile_type == tile_types.terrain_hills_1 or tile_type == tile_types.terrain_hills_2:
		s_size = "medium"
	else:
		s_size = "large"

	new_site_data = SiteData(s_name, s_size, s_order)

	if s_size == "small":
		max_n_staff = 8

	elif s_size == "medium":
		max_n_staff = 16
	
	else:
		max_n_staff = 32

	n_staff = random.randint(int(max_n_staff/2), max_n_staff)
	for i in range(n_staff):
		new_npc = { "name": name_gen.gen_name("people"), "order": s_order }
		new_site_data.staff.append(new_npc)


	name_gen.assign_roles(new_site_data.staff, "monastery", s_size)
	for new_npc in new_site_data.staff:
		if "role" in new_npc and (new_npc["role"] == "abate" or new_npc["role"] == "priore"):
			new_npc["name"] = "padre " + new_npc["name"] + " da " + name_gen.gen_name("sites_international")
		else:
			new_npc["name"] = "frate " + new_npc["name"]



	return new_site_data

