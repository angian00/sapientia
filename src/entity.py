from __future__ import annotations

import math
import copy

from typing import Optional, Tuple, Union, Type, TypeVar, TYPE_CHECKING

from render_order import RenderOrder
import color
import metadata


if TYPE_CHECKING:
	from components.ai import BaseAI
	from components.consumable import Consumable
	from components.equippable import Equippable
	from components.combinable import Combinable
	from components.fighter import Fighter
	from components.inventory import Inventory
	from components.level import Level
	from components.equipment import Equipment
	from game_map import GameMap

T = TypeVar("T", bound="Entity")


class Entity:
	"""
	A generic object to represent players, enemies, items, etc.
	"""
	parent: Union[GameMap, Inventory]
	
	def __init__(
		self,
		parent: Optional[GameMap] = None,
		x: int = 0,
		y: int = 0,
		char: str = "?",
		color: Tuple[int, int, int] = (255, 255, 255),
		name: str = "<Unnamed>",
		blocks_movement: bool = False,
		render_order: RenderOrder = RenderOrder.CORPSE,
	):
		self.x = x
		self.y = y
		self.char = char
		self.color = color
		self.name = name
		self.blocks_movement = blocks_movement
		self.render_order = render_order

		if parent:
			# If parent isn't provided now then it will be set later.
			self.parent = parent
			parent.entities.add(self)



	@property
	def gamemap(self) -> GameMap:
		return self.parent.gamemap

	@property
	def display_name(self) -> str:
		return self.name


	def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
		"""Spawn a copy of this instance at the given location."""
		clone = copy.deepcopy(self)
		clone.x = x
		clone.y = y
		clone.parent = gamemap
		gamemap.entities.add(clone)
		return clone

	
	def distance(self, x: int, y: int) -> float:
		"""
		Return the distance between the current entity and the given (x, y) coordinate.
		"""
		return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)


	def move(self, dx: int, dy: int) -> None:
		# Move the entity by a given amount
		self.x += dx
		self.y += dy

	def place(self, x: int, y: int, gamemap: Optional[GameMap] = None) -> None:
		"""Place this entity at a new location.  Handles moving across GameMaps."""
		self.x = x
		self.y = y
		if gamemap:
			if hasattr(self, "parent"):  # Possibly uninitialized.
				if self.parent is self.gamemap:
					self.gamemap.entities.remove(self)
			self.parent = gamemap
			gamemap.entities.add(self)



class Actor(Entity):
	def __init__(
		self,
		*,
		x: int = 0,
		y: int = 0,
		char: str = "?",
		color: Tuple[int, int, int] = (255, 255, 255),
		name: str = "<Unnamed>",
		ai_cls: Type[BaseAI],
		equipment: Equipment,
		fighter: Fighter,
		inventory: Inventory,
		level: Level,
		is_hostile: bool = False,
	):
		super().__init__(
			x=x,
			y=y,
			char=char,
			color=color,
			name=name,
			blocks_movement=True,
			render_order=RenderOrder.ACTOR,
		)

		self.ai: Optional[BaseAI] = ai_cls(self)

		self.equipment: Equipment = equipment
		self.equipment.parent = self

		self.fighter = fighter
		self.fighter.parent = self

		self.inventory = inventory
		self.inventory.parent = self

		self.level = level
		self.level.parent = self

		self.is_hostile: bool = is_hostile
		self.role: Optional[str] = None
		

	@property
	def is_alive(self) -> bool:
		"""Returns True as long as this actor can perform actions."""
		return bool(self.ai)

	@property
	def display_name(self) -> str:
		if self.role:
			return self.name + " - " + self.role
		else:
			return self.name


class Item(Entity):
	def __init__(
		self,
		*,
		x: int = 0,
		y: int = 0,
		char: str = "?",
		color: Tuple[int, int, int] = (255, 255, 255),
		name: str = "<Unnamed>",
		consumable: Optional[Consumable] = None,
		equippable: Optional[Equippable] = None,
		combinable: Optional[Combinable] = None,
	):
		super().__init__(
			x=x,
			y=y,
			char=char,
			color=color,
			name=name,
			blocks_movement=False,
			render_order=RenderOrder.ITEM,
		)

		self.consumable = consumable
		if self.consumable:
			self.consumable.parent = self

		self.equippable = equippable
		if self.equippable:
			self.equippable.parent = self

		self.combinable = combinable
		if self.combinable:
			self.combinable.parent = self


class Site(Entity):
	def __init__(
		self,
		*,
		x: int = 0,
		y: int = 0,
		char: str = "?",
		color: Tuple[int, int, int] = color.site_light,
		dark_color: Tuple[int, int, int] = color.site_dark,
		name: str = "<Unnamed>",
		size: str = "small",
	):
		super().__init__(
			x=x,
			y=y,
			char=char,
			color=color,
			name=name,
			blocks_movement=False,
			render_order=RenderOrder.SITE,
		)

		self.size = size
		self.dark_color = dark_color
		self.site_data: Optional[metadata.SiteData] = None 

