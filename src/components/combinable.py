from __future__ import annotations

from typing import Optional


import copy

from components.base_component import BaseComponent
import components.inventory
import ingredients
import entity_factories
from entity import Item

from exceptions import Impossible



class Combinable(BaseComponent):
	parent: Item

	def combine(self, ingr2_comb: Combinable) -> None:
		ingr1 = self.parent
		ingr2 = ingr2_comb.parent

		inventory = ingr1.parent
		assert isinstance(inventory, components.inventory.Inventory), "ingr1 is in inventory"
		assert ingr2.parent == inventory, "ingr2 is in inventory"

		prod_id = ingredients.get_combination(ingr1.name, ingr2.name)
		if not prod_id:
			raise Impossible("You cannot combine those two ingredients")

		inventory.items.remove(ingr1)
		inventory.items.remove(ingr2)

		#TODO: make more typesafe
		prod = copy.deepcopy(entity_factories.get_entity_by_id(prod_id))
		assert isinstance(prod, Item)
		self.engine.message_log.add_message(f"You produced a {prod.name}!")

		prod.parent = inventory
		inventory.items.append(prod)
