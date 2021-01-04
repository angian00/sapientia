#!/usr/bin/env python3

import os.path
import glob
import json


root_dir = os.path.dirname(os.path.realpath(__file__))
herbs = {}


def main():
	print("Trying out herbalism ideas")
	load_herbs()


def load_herbs():
	herb_dir = root_dir + "/data/herbs"
	for filename in glob.glob(herb_dir + "/*.json"):
		load_herb(filename)


def load_herb(filename):
	with open(filename) as f:
		herb_data = json.load(f)

	print("Found {}".format(herb_data["name"]))
	herbs[herb_data["name"]] = herb_data



if __name__ == '__main__':
	main()
