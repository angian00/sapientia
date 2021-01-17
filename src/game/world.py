from __future__ import annotations

from typing import Dict, List, Tuple, Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
	from game.map import GameMap
	from game.entity import Site
	from game.engine import Engine



class GameWorld:
	"""
	Holds the map stack for the GameWorld, and generates new maps when entering sites.
	"""

	def __init__(self, *, engine: Engine, map_width: int, map_height: int):
		self.engine = engine

		self.map_width = map_width
		self.map_height = map_height
		self.map_stack: List[Dict[str, Any]] = []


	@property
	def curr_map(self) -> Optional[GameMap]:
		if not self.map_stack:
			return None

		return self.map_stack[-1]["map"]


	def generate_world_map(self) -> None:
		from procgen.map_gen import generate_wilderness_map

		self.world_map = generate_wilderness_map(
			map_width=self.map_width,
			map_height=self.map_height,
			engine=self.engine,
		)

		self.site_maps: Dict[Site, GameMap] = {}
		self.map_stack.clear()

		self.push_map(self.world_map)


	def push_local_map(self, target: Site) -> None:
		from procgen.map_gen import generate_local_map

		self.map_stack[-1]["pos"] = (self.engine.player.x, self.engine.player.y)

		if target not in self.site_maps:
			self.site_maps[target] = generate_local_map(
				map_width=self.map_width,
				map_height=self.map_height,
				engine=self.engine,
				npcs = target.site_data.staff if target.site_data else None,
			)

		self.push_map(self.site_maps[target])


	def push_map(self, new_map: GameMap) -> None:
		new_map.place_random(self.engine.player)
		self.map_stack.append({"map": new_map, "pos": (self.engine.player.x, self.engine.player.y)})

		self.engine.game_map = new_map


	def pop_map(self) -> None:
		self.map_stack.pop()
		
		assert self.curr_map is not None

		curr_pos: Tuple[int, int] = self.map_stack[-1]["pos"]
		self.engine.player.place(curr_pos[0], curr_pos[1], self.curr_map)
		self.engine.game_map = self.curr_map
