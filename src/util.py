
import os.path


root_dir: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/..")


def get_root_dir() -> str:
	return root_dir


def get_data_dir() -> str:
	return root_dir + "/data"

def get_savegame_dir() -> str:
	return root_dir + "/savegame"

def get_media_dir() -> str:
	return root_dir + "/media"
