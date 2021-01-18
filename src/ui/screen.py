from __future__ import annotations

from typing import Iterable, Dict, Tuple, Any, Optional, TYPE_CHECKING
if TYPE_CHECKING:
	from game.map import GameMap
	from game.world import GameWorld
	from game.message_log import MessageLog


from bearlibterminal import terminal # type: ignore
import textwrap
import sys
import copy

import ui.color
from ui.layout import *

from game.entity import Site
from game.engine import Engine
from game.actions import *
import game.entity_factories
import game.tile_types
import util
from exceptions import *


curr_screen: Optional[Screen] = None



MOVE_KEYS = {
	# Arrow keys.
	terminal.TK_UP: (0, -1),
	terminal.TK_DOWN: (0, 1),
	terminal.TK_LEFT: (-1, 0),
	terminal.TK_RIGHT: (1, 0),
	terminal.TK_HOME: (-1, -1),
	terminal.TK_END: (-1, 1),
	terminal.TK_PAGEUP: (1, -1),
	terminal.TK_PAGEDOWN: (1, 1),
	# numpad keys
	terminal.TK_KP_1: (-1, 1),
	terminal.TK_KP_2: (0, 1),
	terminal.TK_KP_3: (1, 1),
	terminal.TK_KP_4: (-1, 0),
	terminal.TK_KP_6: (1, 0),
	terminal.TK_KP_7: (-1, -1),
	terminal.TK_KP_8: (0, -1),
	terminal.TK_KP_9: (1, -1),
	# vi keys
	terminal.TK_H: (-1, 0),
	terminal.TK_J: (0, 1),
	terminal.TK_K: (0, -1),
	terminal.TK_L: (1, 0),
	terminal.TK_Y: (-1, -1),
	terminal.TK_U: (1, -1),
	terminal.TK_B: (-1, 1),
	terminal.TK_N: (1, 1),
}

WAIT_KEYS = {
	terminal.TK_PERIOD,
	terminal.TK_KP_5,
}

CONFIRM_KEYS = {
	terminal.TK_RETURN,
	terminal.TK_KP_ENTER,
}



def init_terminal() -> None:
	global curr_screen

	print("screen.init()")

	media_dir = util.get_media_dir()

	terminal.open()

	terminal.set("window.title='Antiqua Sapientia'")
	terminal.set(f"window.size={screen_width}x{screen_height}")
	terminal.set(f"font: {media_dir}/Menlo-Regular-01.ttf, size=16")
	#terminal.set("ini.settings.tile-size=16")


	terminal.bkcolor(terminal.color_from_name(ui.color.default_bg))
	terminal.color(terminal.color_from_name(ui.color.default_fg))

	terminal.clear()
	print("terminal initialized")

	curr_screen = SplashScreen()
	curr_screen.render()

	ev: int = terminal.read()
	while ev != terminal.TK_CLOSE:
		try:
			action = curr_screen.on_input(ev)
			if action:
				try:
					action.perform()
					if action.engine:
						action.engine.update_fov()

				except Impossible as e:
					action.engine.message_log.add_message(e.args[0], ui.color.impossible)

				action.engine.update_view()

		except SystemExit:
			break

		ev = terminal.read()

	terminal.close()


class Screen():
	def render(self) -> None:
		pass

	def refresh(self) -> None:
		terminal.refresh()

	def on_input(self, ev) -> Optional[Action]:
		return None


class SplashScreen(Screen):
	def __init__(self):
		print("SplashScreen")

	def render(self) -> None:
		terminal.print(x=0, y=int(screen_height/3),
			width=screen_width, height=1,
			align=terminal.TK_ALIGN_CENTER, s="Antiqua Sapientia")
		terminal.print(x=0, y=int(screen_height/2),
			width=screen_width, height=1,
			align=terminal.TK_ALIGN_CENTER, s="a Roguelike/RPG by AnGian")
		terminal.refresh()

	def on_input(self, ev) -> Optional[Action]:
		# any key == "new game"
		global curr_screen

		#TODO: move logic to NewGameAction
		player = copy.deepcopy(game.entity_factories.player)
		curr_screen = GameScreen(Engine.new_game(player))
		curr_screen.render()

		return None



class GameScreen(Screen):
	def __init__(self, engine: Engine):
		print("GameScreen")
		self.engine = engine
		self.engine.game_screen = self


	def render(self) -> None:
		print_frame(map_x, map_y, map_width, map_height, title="Map")
		print_frame(stats_x, stats_y, stats_width, stats_height, title="Stats")
		print_frame(messages_x, messages_y, messages_width, messages_height, title="Messages")
		

		self.engine.update_view()

		print_dumb_stats()

		terminal.refresh()


	def on_input(self, ev) -> Optional[Action]:
		player = self.engine.player
		action: Optional[Action] = None

		# if ev == terminal.TK_BACKSLASH:
		# 	return actions.TakeStairsAction(player)

		if ev in MOVE_KEYS:
			dx, dy = MOVE_KEYS[ev]
			action = BumpAction(player, dx, dy)
		elif ev in WAIT_KEYS:
			action = WaitAction(player)

		elif ev == terminal.TK_ESCAPE:
		 	raise SystemExit()
		
		elif ev == terminal.TK_G:
		 	action = PickupAction(player)
		# elif ev == terminal.TK_I:
		# 	return InventoryActivateHandler(self.engine)
		# elif ev == terminal.TK_D:
		# 	return InventoryDropHandler(self.engine)
		
		# elif ev == terminal.TK_T:
		# 	return NPCEventHandler(self.engine)

		# elif ev == terminal.TK_COMMA:
		# 	return LookHandler(self.engine)

		# elif ev == terminal.TK_C:
		# 	return CharacterScreenEventHandler(self.engine)

		# elif ev == terminal.TK_V:
		# 	return HistoryViewer(self.engine)

		return action


	def update_map(self, game_map: GameMap):
		for x in range(0, game_map.width):
			for y in range(0, game_map.height):
				if game_map.visible[x][y]:
					curr_tile = game_map.tiles[x][y].light_tile
				elif game_map.explored[x][y]:
					curr_tile = game_map.tiles[x][y].dark_tile
				else:
					curr_tile = game.tile_types.SHROUD

				terminal.color(terminal.color_from_name(curr_tile.fg_color))
				terminal.bkcolor(terminal.color_from_name(curr_tile.bg_color))
				terminal.printf(map_x + 1 + x, map_y + 1 + y, curr_tile.ch)


		entities_sorted_for_rendering = sorted(game_map.entities, key=lambda x: x.render_order.value)

		for entity in entities_sorted_for_rendering:
			curr_color = None

			if game_map.visible[entity.x][entity.y]:
				curr_color = entity.color
			elif game_map.explored[entity.x][entity.y] and isinstance(entity, Site):
				curr_color = entity.dark_color

			if curr_color:
				terminal.bkcolor(terminal.color_from_name("transparent"))
				terminal.color(terminal.color_from_name(curr_color))
				terminal.printf(map_x + 1 + entity.x, map_y + 1 + entity.y, entity.char)


	def update_messages(self, message_log: MessageLog) -> None:
		terminal.bkcolor(terminal.color_from_name(ui.color.default_bg))

		#clear old lines
		for x in range(messages_width):
			for y in range(messages_height):
				terminal.printf(x + messages_x + 1, y + messages_y + 1, " ")

		#write new lines bottom-up
		y_offset = messages_height - 2 - 1

		for message in reversed(message_log.messages):
			terminal.color(terminal.color_from_name(message.color))
			for line in reversed(list(wrap_str(message.full_text, messages_width - 2))):
				terminal.print(x=messages_x + 1, y=messages_y + 1 + y_offset, s=line)
				y_offset -= 1
				if y_offset < 0:
					return


	def update_stats(self, stats: Iterable[Dict[str, Any]]) -> None:
		tot_width = stats_width - 2

		for stat in stats:
			s_name = stat["name"]
			s_curr = stat["curr_value"]
			s_max = stat["max_value"]

			bar_width = int(float(s_curr) / s_max * tot_width)

			#TODO: overlapping layers
			#console.draw_rect(x=0, y=45, width=20, height=1, ch=1, bg=color.bar_empty)

			#if bar_width > 0:
			#	console.draw_rect(
			#		x=0, y=45, width=bar_width, height=1, ch=1, bg=color.bar_filled
			#	)

			terminal.color(terminal.color_from_name(ui.color.stats))
			terminal.print(x=stats_x + 1, y=stats_y + 1, s=f"{s_name}: {s_curr}/{s_max}")


	def update_mouse_info(self, mouse_info: str) -> None:
		#TODO: put mouse info somewhere
		#console.print(x=x, y=y, string=names_at_mouse_location)
		pass



def print_frame(x, y, w, h, title=None) -> None:
	terminal.printf(x, y, "\u2552")
	terminal.printf(x+1, y, "\u2550" * (w-2))
	terminal.printf(x+w-1, y, "\u2555")

	for i in range(1, h-1):
		terminal.printf(x, y+i, "\u2502")
		terminal.printf(x+w-1, y+i, "\u2502")

	terminal.printf(x, y+h-1, "\u2514")
	terminal.printf(x+1, y+h-1, "\u2500" * (w-2))
	terminal.printf(x+w-1, y+h-1, "\u2518")

	if title:
		terminal.printf(x+2, y, s=f" {title} ")



def wrap_str(string: str, width: int) -> Iterable[str]:
	"""Return a wrapped text message."""
	for line in string.splitlines():
		yield from textwrap.wrap(line, width, expand_tabs=True,)



def print_dumb_map() -> None:
	curr_bkcolor = terminal.state(terminal.TK_BKCOLOR)

	terminal.bkcolor(terminal.color_from_name("black"))

	for x in range(1, map_width-1):
		for y in range(1, map_height-1):
			terminal.printf(map_x + x, map_y + y, " ")

	terminal.bkcolor(curr_bkcolor)


def print_dumb_stats() -> None:
	x = stats_x + 1
	y = stats_y + 1

	terminal.color(terminal.color_from_name("white"))
	terminal.printf(x, y, "Ulemor")

	y += 1
	
	y += 1
	terminal.color(terminal.color_from_name("dark green"))
	terminal.printf(x, y, "HP: 27")

	y += 1
	terminal.color(terminal.color_from_name("dark yellow"))
	terminal.printf(x, y, "xp: 29270")

	y += 1

	y += 1
	terminal.color(terminal.color_from_name("purple"))
	terminal.printf(x, y, "[[Poisoned]]")

	y += 1
	terminal.color(terminal.color_from_name("grey"))
	terminal.printf(x, y, "[[Sleeping]]")

