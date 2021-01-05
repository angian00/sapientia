#!/usr/bin/env python3

import random


size = "medium"
name_file = "data/names_people.txt"
role_file = "data/roles_monastery.txt"

name_freq_thr = 10


sizes = {
	"small": (5, 8),	
	"medium": (8, 15),
	"large": (16, 30),
}

names = []
name_freqs = []
roles = {}


def main():
	load_names()
	load_roles()

	n_min = sizes[size][0]
	n_max = sizes[size][1]
	n_people = random.randint(n_min, n_max-1)
	people = {}
	for i in range(n_people):
		new_name = random_name()
		people[new_name] = ({"name": new_name})

	assign_roles(people, roles, size)


	
	print("------------------------------")
	print("Random monastery")
	print("------------------------------")
	print()
	
	print(f"size: {size}")
	print(f"n_people: {n_people}")
	print()

	for p_name in people:
		p = people[p_name]
		p_role = p["role"] if "role" in p else None

		p_str = ""
		if p_role == "abate":
			p_str += "* padre "
		else:
			p_str += "  frate "

		p_str += p_name
		if p_role:
			p_str += ": " + p["role"]

		print(p_str)

	print()
	print("------------------------------")


def load_names():
	with open(name_file) as f:
		for line in f.readlines():
			if line[0] == "#" or line.strip() == "":
				#skip comments and empty lines
				continue

			tokens = line.strip().split("|")
			print(line)
			name = tokens[0]
			freq = int(tokens[1])
			if freq >= name_freq_thr:
				names.append(name)
				name_freqs.append(freq)

def random_name():
	return random.choices(names, weights=name_freqs)[0]


def load_roles():
	with open(role_file) as f:
		for line in f.readlines():
			if line[0] == "#" or line.strip() == "":
				#skip comments and empty lines
				continue

			tokens = line.strip().split("|")
			role = tokens[0]
			p_large  = tokens[1]
			p_medium = tokens[2]
			p_small  = tokens[3]
			roles[role] = {
				"small": p_small,
				"medium": p_medium,
				"large": p_large,
			}

def assign_roles(people, roles, size):
	# only 0 or 1 role per person
	candidates = list(people.keys()).copy()

	#TODO: sort roles by prob
	for r_name in roles:
		r_prob = float(roles[r_name][size])
		if random.random() > r_prob:
			#skip role
			continue

		chosen = random.choice(candidates)
		people[chosen]["role"] = r_name
		candidates.remove(chosen)
		
		if not candidates:
			#no more people available!
			break


if __name__ == '__main__':
	main()
