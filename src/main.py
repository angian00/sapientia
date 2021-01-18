#!/usr/bin/env python3

from bearlibterminal import terminal # type: ignore

from ui.screen import init_terminal



def main() -> None:
	print("Antiqua Sapientia starting")
	init_terminal()


if __name__ == "__main__":
	main()
