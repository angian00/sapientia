from components.ai import BaseAI, HostileAI, FriendlyAI
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.equipment import Equipment
from components import consumable, equippable, combinable

from entity import Entity, Actor, Item, Site
import color


#----------------------------------------------------

def get_entity_by_id(entity_id: str) -> Entity:
	return poison_potion

#----------------------------------------------------

player = Actor(
	char="@",
	color=(255, 255, 255),
	name="player",
	ai_cls=BaseAI,
	equipment=Equipment(),
	fighter=Fighter(hp=30, base_defense=2, base_power=5),
	inventory=Inventory(capacity=26),
	level=Level(level_up_base=200),
)


orc = Actor(
	char="o",
	color=(63, 127, 63),
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
	color=(0, 127, 0),
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
	color=color.white,
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
	color=(127, 0, 255),
	name="health potion",
	consumable=consumable.HealingConsumable(amount=4),
)

lightning_scroll = Item(
	char="~",
	color=(255, 255, 0),
	name="lightning scroll",
	consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)

confusion_scroll = Item(
   char="~",
   color=(207, 63, 255),
   name="confusion scroll",
   consumable=consumable.ConfusionConsumable(number_of_turns=10),
)

fireball_scroll = Item(
   char="~",
   color=(255, 0, 0),
   name="fireball scroll",
   consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)


poison_potion = Item(
	char="!",
	color=(255, 0, 0),
	name="poison potion",
	consumable=consumable.PoisonConsumable(amount=4),
)


#----------------------------------------------------

dagger = Item(
	char="/", color=(0, 191, 255), name="dagger", equippable=equippable.Dagger()
)

sword = Item(char="/", color=(0, 191, 255), name="sword", equippable=equippable.Sword())

leather_armor = Item(
	char="[",
	color=(139, 69, 19),
	name="leather armor",
	equippable=equippable.LeatherArmor(),
)

chain_mail = Item(
	char="[", color=(139, 69, 19), name="chain mail", equippable=equippable.ChainMail()
)

#----------------------------------------------------

herb = Item(
	char=",", color=(40, 255, 50), name="<unknown herb>", combinable=combinable.Combinable()
)


#----------------------------------------------------

monastery = Site(char="?", name="monastery")
village = Site(char="\u25CB", name="village")

