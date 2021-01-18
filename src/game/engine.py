from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING
if TYPE_CHECKING:
	from game.entity import Actor
	from ui.screen import GameScreen


from tcod.map import compute_fov
from tcod import FOV_BASIC

from game.map import GameMap
from game.world import GameWorld
from game.message_log import MessageLog
import ui.color

import exceptions


# DEBUG
#fov_full = True
fov_full = False
#


class Engine:
	game_map: GameMap
	game_world: GameWorld


	@classmethod
	def new_game(cls, player: Actor) -> Engine:
		"""Return a brand new game session as an Engine instance"""
		#TODO: move
		map_width = 78
		map_height = 28

		#player = copy.deepcopy(entity_factories.player)

		engine = Engine(player=player)

		engine.game_world = GameWorld(
			engine=engine,
			map_width=map_width,
			map_height=map_height,
		)

		engine.game_world.generate_world_map()
		engine.update_fov()

		engine.message_log.add_message("Welcome, adventurer, to yet another dungeon!", ui.color.welcome_text)

		return engine



	def __init__(self, player: Actor):
		self.message_log = MessageLog()
		self.mouse_location = (0, 0)
		self.player = player
		self.game_screen: Optional[GameScreen] = None


	def handle_enemy_turns(self) -> None:
		for entity in set(self.game_map.actors) - {self.player}:
			if entity.ai:
				try:
					entity.ai.perform()
				except exceptions.Impossible:
					# Ignore impossible action exceptions from AI
					pass


	def update_fov(self) -> None:
		if fov_full:
			import numpy as np # type: ignore
			self.game_map.visible[:] = np.full((self.game_map.width, self.game_map.height), fill_value=True, order="F")
		else:
			transparents: List[List[bool]] = []

			for x in range(self.game_map.width):
				transparents.append([])
				for y in range(self.game_map.height):
					transparents[x].append(self.game_map.tiles[x][y].transparent)

			self.game_map.visible[:] = compute_fov(
				transparents,
				(self.player.x, self.player.y),
				radius=8,
				algorithm=FOV_BASIC
			)

		for x in range(self.game_map.width):
			for y in range(self.game_map.height):
				self.game_map.explored[x][y] |= self.game_map.visible[x][y]


	def update_view(self) -> None:
		if not self.game_screen:
			return

		self.game_screen.update_map(self.game_map)
		self.game_screen.update_messages(self.message_log)

		self.game_screen.update_stats([{
			"name": "hp",
			"curr_value": self.player.fighter.hp,
			"max_value": self.player.fighter.max_hp,
		}])

		self.game_screen.update_mouse_info(self.get_mouse_info())
		self.game_screen.refresh()


	def get_mouse_info(self) -> str:
		mouse_x, mouse_y = self.mouse_location
		if not self.game_map.in_bounds(mouse_x, mouse_y) or not self.game_map.visible[mouse_x][mouse_y]:
			return ""

		names = ", ".join(entity.display_name for entity in self.game_map.entities \
			if entity.x == mouse_x and entity.y == mouse_y)

		return names
