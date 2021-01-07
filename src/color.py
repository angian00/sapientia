from __future__ import annotations
from typing import Tuple


white = (0xFF, 0xFF, 0xFF)
black = (0x0, 0x0, 0x0)
red = (0xFF, 0x0, 0x0)

player_atk = (0xE0, 0xE0, 0xE0)
enemy_atk = (0xFF, 0xC0, 0xC0)
needs_target = (0x3F, 0xFF, 0xFF)
status_effect_applied = (0x3F, 0xFF, 0x3F)
descend = (0x9F, 0x3F, 0xFF)

player_die = (0xFF, 0x30, 0x30)
enemy_die = (0xFF, 0xA0, 0x30)

invalid = (0xFF, 0xFF, 0x00)
impossible = (0x80, 0x80, 0x80)
error = (0xFF, 0x40, 0x40)

welcome_text = (0x20, 0xA0, 0xFF)
health_recovered = (0x0, 0xFF, 0x0)

bar_text = white
bar_filled = (0x0, 0x60, 0x0)
bar_empty = (0x40, 0x10, 0x10)

menu_title = (255, 255, 63)
menu_text = white



terrain_plains_1  = (165,165,141)
terrain_plains_2  = (183,183,164)
terrain_hills_1   = (107,112,92)
terrain_hills_2   = (203,153,126)
terrain_mountains = (221,190,169)

floor_dark  = (144, 144, 144)
floor_light = (200, 200, 200)
wall_dark  = (64, 64, 64)
wall_light = (0, 0, 0)
site_light = (0, 0, 200)
site_dark  = (0, 0, 150)


def darken(color: Tuple[int, int, int]) -> Tuple[int, int, int]:
	darken_factor = 0.75

	return (
		int(color[0]*darken_factor),
		int(color[1]*darken_factor),
		int(color[2]*darken_factor),
	)
