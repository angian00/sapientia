from components.ai import BaseAI, HostileAI, FriendlyAI
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.equipment import Equipment
from components import consumable, equippable, combinable

from game.entity import Entity, Actor, Item, Site
import ui.color


#----------------------------------------------------

def get_entity_by_id(entity_id: str) -> Entity:
	return poison_potion

#----------------------------------------------------

player = Actor(
	char="@",
	color="white",
	name="player",
	ai_cls=BaseAI,
	equipment=Equipment(),
	fighter=Fighter(hp=30, base_defense=2, base_power=5),
	inventory=Inventory(capacity=26),
	level=Level(level_up_base=200),
)


orc = Actor(
	char="o",
	color="#408040",
	name="orc",
	ai_cls=HostileAI,
	equipment=Equipment(),
	fighter=Fighter(hp=10, base_defense=0, base_power=3),
	inventory=Inventory(capacity=0),
	level=Level(xp_given=35),
	is_hostile=True,
)

troll = Actor(
	char="T",
	color="#008000",
	name="troll",
	ai_cls=HostileAI,
	equipment=Equipment(),
	fighter=Fighter(hp=16, base_defense=1, base_power=4),
	inventory=Inventory(capacity=0),
	level=Level(xp_given=100),
	is_hostile=True,
)

#----------------------------------------------------
friendly_npc = Actor(
	char="p",
	color=ui.color.white,
	name="<no name>",
	ai_cls=FriendlyAI,
	equipment=Equipment(),
	fighter=Fighter(hp=10, base_defense=1, base_power=1),
	inventory=Inventory(capacity=10),
	level=Level(xp_given=0),
	is_hostile=False
)

#----------------------------------------------------

health_potion = Item(
	char="!",
	color="#8000FF",
	name="health potion",
	consumable=consumable.HealingConsumable(amount=4),
)

lightning_scroll = Item(
	char="~",
	color="#FFFF00",
	name="lightning scroll",
	consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)

confusion_scroll = Item(
   char="~",
   color="#cf3fff",
   name="confusion scroll",
   consumable=consumable.ConfusionConsumable(number_of_turns=10),
)

fireball_scroll = Item(
   char="~",
   color="#FF0000",
   name="fireball scroll",
   consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)


poison_potion = Item(
	char="!",
	color="#FF0000",
	name="poison potion",
	consumable=consumable.PoisonConsumable(amount=4),
)


#----------------------------------------------------

dagger = Item(
	char="/", color="#00BFFF", name="dagger", equippable=equippable.Dagger()
)

sword = Item(char="/", color="#00BFFF", name="sword", equippable=equippable.Sword())

leather_armor = Item(
	char="[",
	color="#8B4513",
	name="leather armor",
	equippable=equippable.LeatherArmor(),
)

chain_mail = Item(
	char="[", color="#8B4513", name="chain mail", equippable=equippable.ChainMail()
)

#----------------------------------------------------

herb = Item(
	char=",", color="#28FF33", name="<unknown herb>", combinable=combinable.Combinable()
)


#----------------------------------------------------

monastery = Site(char="?", name="monastery")
village = Site(char="\u25CB", name="village")

