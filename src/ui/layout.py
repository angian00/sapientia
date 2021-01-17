
screen_width: int = 100
screen_height: int = 40

# game screen
map_x: int = 0
map_y: int = 0
map_width: int = 80
map_height: int = 30

stats_x: int = map_width
stats_y: int = 0
stats_width: int = 20
stats_height: int = map_height

messages_x: int = 0
messages_y: int = map_height
messages_width: int = screen_width
messages_height: int = 10

assert map_width + stats_width == screen_width
assert map_height + messages_height == screen_height
