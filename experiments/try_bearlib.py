#!/usr/bin/env python3


from bearlibterminal import terminal

w = 100
h = 40
w2 = 18
h2 = 10
w1 = w - w2
h1 = h - h2


fg_color = terminal.color_from_argb(255, 240, 214, 195)
bg_color = terminal.color_from_argb(255, 35, 20, 10)


def main():

	terminal.open()

	terminal.set("window.title='Sapientia'")
	terminal.set(f"window.size={w}x{h}")
	terminal.set("font: /Users/angian/Downloads/Menlo-Regular-01.ttf, size=16")
	#terminal.set("ini.settings.tile-size=16")


	terminal.bkcolor(bg_color)
	terminal.color(fg_color)
	terminal.clear()

	print_frame(w1, h1, 0, 0, title="Map")
	print_frame(w2, h1, w1, 0, title="Stats")
	print_frame(w, h2, 0, h1, title="Messages")

	print_map()
	print_stats()

	terminal.refresh()

	while terminal.read() != terminal.TK_CLOSE:
		pass

	terminal.close()



def print_frame(w, h, x=0, y=0, title=None):
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
		terminal.printf(x+2, y, s=f" {title} ");


def print_map():
	curr_bkcolor = terminal.state(terminal.TK_BKCOLOR);

	terminal.bkcolor(terminal.color_from_name("black"))

	for x in range(1, w1-1):
		for y in range(1, h1-1):
			terminal.printf(x, y, " ")

	terminal.bkcolor(curr_bkcolor)


def print_stats():
	x = w1 + 1
	y = 1

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


if __name__ == '__main__':
	main()
