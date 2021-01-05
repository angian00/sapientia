from __future__ import annotations
from typing import Iterable, Iterator, Optional, TYPE_CHECKING

import numpy as np  # type: ignore
from tcod.console import Console

from entity import Actor, Item, Site
import tile_types

if TYPE_CHECKING:
	from engine import Engine
	from entity import Entity



class GameMap:
	def __init__(
		self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()
	):
		self.engine = engine
		self.width, self.height = width, height
		self.entities = set(entities)
		self.tiles = np.full((width, height), fill_value=tile_types.floor, order="F")

		self.visible = np.full(
			(width, height), fill_value=False, order="F"
		)
		self.explored = np.full(
			(width, height), fill_value=False, order="F"
		)
		
		self.downstairs_location = (0, 0)


	@property
	def gamemap(self) -> GameMap:
		return self

	@property
	def actors(self) -> Iterator[Actor]:
		"""Iterate over this maps living actors."""
		yield from (
			entity
			for entity in self.entities
			if isinstance(entity, Actor) and entity.is_alive
		)

	@property
	def items(self) -> Iterator[Item]:
		yield from (entity for entity in self.entities if isinstance(entity, Item))

	@property
	def sites(self) -> Iterator[Site]:
		yield from (entity for entity in self.entities if isinstance(entity, Site))



	def get_blocking_entity_at_location(
		self, location_x: int, location_y: int
	) -> Optional[Entity]:
		for entity in self.entities:
			if (
				entity.blocks_movement 
				and entity.x == location_x 
				and entity.y == location_y
			):
				return entity

		return None


	def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
		for actor in self.actors:
			if actor.x == x and actor.y == y:
				return actor

		return None

	def get_site_at_location(self, x: int, y: int) -> Optional[Site]:
		for site in self.sites:
			if site.x == x and site.y == y:
				return site

		return None



	def in_bounds(self, x: int, y: int) -> bool:
		"""Return True if x and y are inside of the bounds of this map."""
		return 0 <= x < self.width and 0 <= y < self.height


	def render(self, console: Console) -> None:
		"""
		Renders the map.

		If a tile is in the "visible" array, then draw it with the "light" colors.
		If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
		Otherwise, the default is "SHROUD".
		"""
		console.tiles_rgb[0:self.width, 0:self.height] = np.select(
			condlist=[self.visible, self.explored],
			choicelist=[self.tiles["light"], self.tiles["dark"]],
			default=tile_types.SHROUD,
		)


		entities_sorted_for_rendering = sorted(
			self.entities, key=lambda x: x.render_order.value
		)
		for entity in entities_sorted_for_rendering:
			# Only print entities that are in the FOV
			if self.visible[entity.x, entity.y]:
				console.print(
					x=entity.x, y=entity.y, string=entity.char, fg=entity.color
				)


class GameWorld:
	"""
	Holds the settings for the GameMap, and generates new maps when moving down the stairs.
	"""

	def __init__(
		self,
		*,
		engine: Engine,
		map_width: int,
		map_height: int
	):
		self.engine = engine

		self.map_width = map_width
		self.map_height = map_height
		

	def generate_world_map(self) -> None:
		from procgen import generate_wilderness

		self.world_map = generate_wilderness(
			map_width=self.map_width,
			map_height=self.map_height,
			engine=self.engine,
		)

		self.site_maps = {}
		self.engine.game_map = self.world_map


	def switch_map(self, target) -> None:
		from procgen import generate_wilderness

		#if isinstance(target, Site)
		if target not in self.site_maps:
			self.site_maps[target] = generate_wilderness(
				map_width=self.map_width,
				map_height=self.map_height,
				engine=self.engine,
			)

		self.engine.game_map = self.site_maps[target]


