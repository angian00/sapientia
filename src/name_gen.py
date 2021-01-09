from __future__ import annotations
from typing import Sequence, Dict, Tuple, List, Any


import random
import os.path



categories: Sequence[str] = ( "people", "sites" )
name_data: Dict[str, Tuple[Sequence[str], Sequence[int]]] = {}


root_dir: str = os.path.dirname(os.path.realpath(__file__))


def load_all_names() -> None:
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



def assign_roles(people: List[Dict[str, Any]], category: str, size: str) -> None:
	""" only 0 or 1 role per person """

	candidates = list(range(len(people)))
	chosen_roles: Dict[int, str] = {}

	roles = load_roles(category, size)

	#TODO: sort roles by prob to be more robust if n_roles > n_people
	for r_name in roles:
		r_prob = float(roles[r_name])
		if random.random() > r_prob:
			#skip role
			continue

		chosen = random.choice(candidates)
		chosen_roles[chosen] = r_name
		candidates.remove(chosen)
		
		if not candidates:
			#no more people available!
			break

	for i in chosen_roles:
		people[i]["role"] = chosen_roles[i]


def load_roles(category: str, size: str) -> Dict[str, float]:
	roles: Dict[str, float] = {}
	
	role_file = root_dir + "/../data/roles_" + category + ".txt"
	with open(role_file) as f:
		for line in f.readlines():
			if line[0] == "#" or line.strip() == "":
				#skip comments and empty lines
				continue

			tokens = line.strip().split("|")
			role = tokens[0]
			if category == "small":
				val = tokens[1]
			elif category == "medium":
				val = tokens[2]
			else:
				val  = tokens[3]
			roles[role] = float(val)

	return roles



load_all_names()


