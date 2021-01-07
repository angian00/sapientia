from __future__ import annotations
from typing import Sequence, Dict, Tuple, TYPE_CHECKING


import random
import os.path



categories: Sequence[str] = ( "people", "sites" )
name_data: Dict[str, Tuple[Sequence[str], Sequence[int]]] = {}


root_dir: str = os.path.dirname(os.path.realpath(__file__))


def load_all() -> None:
	for c in categories:
		name_data[c] = load_names(root_dir + "/../data/names_" + c + ".txt")


def load_names(filename: str) -> Tuple[Sequence[str], Sequence[int]]:
	names = []
	name_freqs = []

	with open(filename) as f:
		for line in f.readlines():
			if line[0] == "#" or line.strip() == "":
				#skip comments and empty lines
				continue

			tokens = line.strip().split("|")
			name = tokens[0]
			freq = 1 if len(tokens) == 1 else int(tokens[1])

			names.append(name)
			name_freqs.append(freq)

	return names, name_freqs


def gen_name(category: str) -> str:
	names = name_data[category][0]
	freqs = name_data[category][1]

	return random.choices(names, weights=freqs)[0]


load_all()

