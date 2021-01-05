import random
import os.path


categories = ( "people", "sites" )
name_data = {}


root_dir = os.path.dirname(os.path.realpath(__file__))


def load_all():
	for c in categories:
		name_data[c] = load_names(root_dir + "/../data/names_" + c + ".txt")


def load_names(filename):
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


def gen_name(category):
	names = name_data[category][0]
	freqs = name_data[category][1]

	return random.choices(names, weights=freqs)[0]
