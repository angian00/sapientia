from __future__ import annotations

from typing import Dict, Sequence, Any, Optional

import os.path
import json
import random


root_dir: str = os.path.dirname(os.path.realpath(__file__))

herb_data: Dict[str, Dict[str, Any]] = {}
herb_names: Sequence[str]

combinations: Dict[str, Dict[str, str]] = {}


def load_herbs() -> None:
	herb_file = root_dir + "/../data/herbs.json"
	with open(herb_file) as f:
		json_data = json.load(f)

	for hd in json_data:
		herb_data[hd["englishName"]] = hd


def load_combinations() -> None:
	comb_file = root_dir + "/../data/ingredient_combinations.txt"
	with open(comb_file) as f:
		for line in f.readlines():
			if line[0] == "#" or line.strip() == "":
				#skip comments and empty lines
				continue

			tokens = line.strip().split("|")
			ingr1 = tokens[0]
			ingr2 = tokens[1]
			prod = tokens[2]

			if ingr1 not in combinations:
				combinations[ingr1] = {}
			combinations[ingr1][ingr2] = prod

			if ingr2 not in combinations:
				combinations[ingr2] = {}
			combinations[ingr2][ingr1] = prod



def gen_herb() -> str:
	herb_names = list(herb_data.keys())
	herb_freqs: List[float] = []

	for h_name in herb_names:
		herb_freqs.append(herb_data[h_name]["frequency"])

	return random.choices(herb_names, herb_freqs)[0]


def get_combination(ingr1: str, ingr2: str) -> Optional[str]:
	if ingr1 not in combinations:
		return None
	
	if ingr2 not in combinations[ingr1]:
		return None
	
	return combinations[ingr1][ingr2]
	

load_herbs()
load_combinations()
