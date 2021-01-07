#!/usr/bin/env python3

import os.path
import copy
import traceback

import tcod

import color
import exceptions
import input_handlers
import setup_game



root_dir = os.path.dirname(os.path.realpath(__file__))


def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None:
	"""If the current event handler has an active Engine then save it"""
	if isinstance(handler, input_handlers.EventHandler):
		handler.engine.save_as(root_dir + "/../savegame/" + filename)
		print("Game saved")



def main() -> None:
	screen_width = 80
	screen_height = 50


	tileset = tcod.tileset.load_tilesheet(root_dir + "/../media/Japa_20x20.png", 16, 16, tcod.tileset.CHARMAP_CP437)

	handler: input_handlers.BaseEventHandler = setup_game.MainMenu()

	with tcod.context.new_terminal(
		screen_width,
		screen_height,
		tileset=tileset,
		title="Antiqua Sapientia",
		vsync=True,
	) as context:

		root_console = tcod.Console(screen_width, screen_height, order="F")

		try:
			while True:
				root_console.clear()
				handler.on_render(console=root_console)
				context.present(root_console)

				try:
					for event in tcod.event.wait():
						context.convert_event(event)
						handler = handler.handle_events(event)
				except Exception:
					# Handle exceptions in game
					traceback.print_exc()  # Print error to stderr
					# Then print the error to the message log
					if isinstance(handler, input_handlers.EventHandler):
						handler.engine.message_log.add_message(
							traceback.format_exc(), color.error
						)
		
		except exceptions.QuitWithoutSaving:
			raise

		except SystemExit:
			# Save and quit
			save_game(handler, "savegame.sav")
			raise

		except BaseException:
			# Save on any other unexpected exception.
			save_game(handler, "savegame.sav")
			raise



if __name__ == "__main__":
	main()
