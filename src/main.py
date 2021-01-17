#!/usr/bin/env python3

from bearlibterminal import terminal # type: ignore

import ui.screen



def main() -> None:
	print("Antiqua Sapientia starting")
	ui.screen.init()


if __name__ == "__main__":
	main()
