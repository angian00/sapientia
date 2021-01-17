from __future__ import annotations
from typing import Sequence, Dict, Tuple, List, Any


import random
import os.path

from procgen.name_gen import gen_name
import util


church_schemes = [
	("just_a_saint", 20),
	("two_saints", 2),
	("a_saint_decorated", 7),
	("mary_attribute", 4),
	("mary_decorated", 4),
	("jesus_other", 3),
]

c_scheme_names: Sequence[str]
c_scheme_freqs: Sequence[float]

decoration_schemes = [
	("in", 20),
	("sopra", 20),
	("mura", 1),
	("geo", 3),
]

dec_scheme_names: Sequence[str]
dec_scheme_freqs: Sequence[float]

geo_schemes = [
	("monte", 10),
	("monti", 5),
	("colle", 10),
	("colli", 5),
	("fontane", 3),
]

geo_scheme_names: Sequence[str]
geo_scheme_freqs: Sequence[float]

saint_data: List[Dict[str, Any]] = []
saint_freqs: Sequence[float]

mary_data: List[Tuple[str, float]] = []
mary_attrs: Sequence[str]
mary_freqs: Sequence[float]

jesus_other_data: List[Tuple[str, float]] = []
jesus_other_names: Sequence[str]
jesus_other_freqs: Sequence[float]


def load_all_church() -> None:
	global c_scheme_names, c_scheme_freqs
	global dec_scheme_names, dec_scheme_freqs
	global geo_scheme_names, geo_scheme_freqs
	global saint_freqs
	global mary_attrs, mary_freqs
	global jesus_other_names, jesus_other_freqs


	c_scheme_names = [ cs[0] for cs in church_schemes ]
	c_scheme_freqs = [ cs[1] for cs in church_schemes ]

	dec_scheme_names = [ ds[0] for ds in decoration_schemes ]
	dec_scheme_freqs = [ ds[1] for ds in decoration_schemes ]

	geo_scheme_names = [ gs[0] for gs in geo_schemes ]
	geo_scheme_freqs = [ gs[1] for gs in geo_schemes ]

	load_saint_data()
	saint_freqs = [ s["freq"] for s in saint_data ]

	mary_data = load_name_freqs("mary_attributes")
	mary_attrs = [ md[0] for md in mary_data ]
	mary_freqs = [ md[1] for md in mary_data ]

	jesus_other_data = load_name_freqs("jesus_other")
	jesus_other_names = [ jo[0] for jo in jesus_other_data ]
	jesus_other_freqs = [ jo[1] for jo in jesus_other_data ]



def load_saint_data() -> None:
	saint_file = util.get_data_dir() + "/saints.txt"
	with open(saint_file) as f:
		for line in f.readlines():
			if line[0] == "#" or line.strip() == "":
				#skip comments and empty lines
				continue

			tokens = line.strip().split("|")
			
			saint_data.append({
				"prefix": tokens[0], 
				"name": tokens[1],
				"attribute": tokens[2],
				"freq": float(tokens[3]),
				"sex": tokens[4],
			})

def load_name_freqs(filename: str) -> List[Tuple[str, float]]:
	res: List[Tuple[str, float]] = []

	full_path = util.get_data_dir() + "/" + filename + ".txt"

	with open(full_path) as f:
		for line in f.readlines():
			if line[0] == "#" or line.strip() == "":
				#skip comments and empty lines
				continue

			tokens = line.strip().split("|")
			
			res.append(( tokens[0], float(tokens[1]) ))

	return res


def decorate(name: str) -> str:
	res = name

	dec_scheme = random.choices(dec_scheme_names, dec_scheme_freqs)[0]
	
	if dec_scheme == "in":
		res += " in " + gen_name("sites")
	elif dec_scheme == "sopra":
		res += " sopra " + gen_name("sites")
	elif dec_scheme == "mura":
		res += " fuori le mura"

	else: #geo
		geo_scheme = random.choices(geo_scheme_names, geo_scheme_freqs)[0]
		n_geo = random.choice(["", "tre ", "quattro ", "sette "])
		
		if geo_scheme == "monte":
			res += " al monte"
		elif geo_scheme == "monti":
			res += " ai " + n_geo + "monti"
		elif geo_scheme == "colle":
			res += " al colle"
		elif geo_scheme == "colli":
			res += " ai " + n_geo + "colli"
		else: #fontane
			res += " alle " + n_geo + "fontane"

	return res


def gen_church_name() -> str:
	chosen_scheme = random.choices(c_scheme_names, c_scheme_freqs)[0]

	if chosen_scheme == "just_a_saint":
		saint = random.choices(saint_data, saint_freqs)[0]
		if saint["attribute"] == "":
			return saint["prefix"] + saint["name"]
		else:
			return saint["prefix"] + saint["name"] + " " + saint["attribute"]

	elif chosen_scheme == "two_saints":
		[saint1, saint2] = random.choices(saint_data, saint_freqs, k=2)
		return "santi " + saint1["name"] + " e " + saint2["name"]
	
	elif chosen_scheme == "a_saint_decorated":
		saint = random.choices(saint_data, saint_freqs)[0]

		return decorate(saint["prefix"] + saint["name"])

	elif chosen_scheme == "mary_attribute":
		mary_attr = random.choices(mary_attrs, mary_freqs)[0]
		return "santa Maria " + mary_attr

	elif chosen_scheme == "mary_decorated":
		return decorate("santa Maria")

	else: #"jesus_other"
		return random.choices(jesus_other_names, jesus_other_freqs)[0]


load_all_church()

