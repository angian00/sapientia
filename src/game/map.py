from __future__ import annotations

from typing import Dict, Iterable, Iterator, Optional, TYPE_CHECKING

if TYPE_CHECKING:
	from game.entity import Entity, Actor, Item, Site
	from game.engine import Engine

import random

import game.tile_types


class GameMap:
	def __init__(self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()):
		self.engine = engine
		self.width, self.height = width, height
		self.entities = set(entities)

		self.visible = [[False] * height ] * width
		self.explored = [[False] * height ] * width
		self.tiles: List[List[Terrain]] = []

		for x in range(width):
			self.tiles.append([])
			self.visible.append([])
			self.explored.append([])

			for y in range(height):
				self.tiles[x].append(game.tile_types.floor)
				self.visible.append(False)
				self.explored.append(False)


	@property
	def gamemap(self) -> GameMap:
		return self

	@property
	def actors(self) -> Iterator[Actor]:
		"""Iterate over this maps living actors"""
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



	def get_blocking_entity_at_location(self, x: int, y: int) -> Optional[Entity]:
		for entity in self.entities:
			if (entity.blocks_movement and entity.x == x and entity.y == y):
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
		return 0 <= x < self.width and 0 <= y < self.height



	def place_random(self, entity: Entity) -> None:
		while True:
			x = random.randint(0, self.width-1)
			y = random.randint(0, self.height-1)
			
			if self.tiles[x][y] != game.tile_types.wall and not self.get_blocking_entity_at_location(x, y):
				break
		
		entity.place(x, y, self)

