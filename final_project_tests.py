'''
Tests for my CISC108 final project.

Change log:
  - 0.0.1: Initial version
'''

__VERSION__ = '0.0.1'

from cisc108 import assert_equal
from cisc108_game import assert_type

################################################################################
# Game import
# Rename this to the name of your project file.
from project_starter import *

################################################################################
## Testing random_value
random.seed(0)

for i in range(4):
    point = get_random_position()
    # Test the function produces values in the expected range
    assert_equal(0 <= point['x'] <= WINDOW_WIDTH, True)
    assert_equal(0 <= point['y'] <= WINDOW_HEIGHT, True)
    
################################################################################
## Testing make_enemy and make_item

for i in range(4):
    enemy = make_enemy()
    # Test the function produces values in the expected range
    assert_equal(0 <= enemy['current']['x'] <= WINDOW_WIDTH, True)
    assert_equal(0 <= enemy['current']['y'] <= WINDOW_HEIGHT, True)
    assert_equal(0 <= enemy['goal']['x'] <= WINDOW_WIDTH, True)
    assert_equal(0 <= enemy['goal']['y'] <= WINDOW_HEIGHT, True)
    # Test the function has different current and goal (unlikely)
    assert_equal(enemy['current'] != enemy['goal'], True)
    
for i in range(4):
    item = make_item()
    # Test the function produces values in the expected range
    assert_equal(0 <= item['position']['x'] <= WINDOW_WIDTH, True)
    assert_equal(0 <= item['position']['y'] <= WINDOW_HEIGHT, True)
    
################################################################################
## Testing angle_between
ORIGIN = {'x': 0, 'y': 0}
TOP_RIGHT = {'x': WINDOW_WIDTH, 'y': WINDOW_HEIGHT}
TOP_LEFT = {'x': 0, 'y': WINDOW_HEIGHT}
BOTTOM_RIGHT = {'x': WINDOW_WIDTH, 'y': 0}
CENTER = {'x': WINDOW_WIDTH/2, 'y': WINDOW_HEIGHT/2}
CENTER_LEFT = {'x': 0, 'y': WINDOW_HEIGHT/2}
CENTER_RIGHT = {'x': WINDOW_WIDTH, 'y': WINDOW_HEIGHT/2}
CENTER_BOTTOM = {'x': WINDOW_WIDTH/2, 'y': 0}
CENTER_TOP = {'x': WINDOW_WIDTH/2, 'y': WINDOW_HEIGHT}
assert_equal(angle_between(CENTER, TOP_RIGHT), math.pi/4)
assert_equal(angle_between(CENTER, CENTER_TOP), math.pi/2)
assert_equal(angle_between(CENTER, TOP_LEFT), 3*math.pi/4)
assert_equal(angle_between(CENTER, CENTER_LEFT), math.pi)
assert_equal(angle_between(CENTER, ORIGIN), -3*math.pi/4)
assert_equal(angle_between(CENTER, CENTER_BOTTOM), -math.pi/2)
assert_equal(angle_between(CENTER, BOTTOM_RIGHT), -math.pi/4)
assert_equal(angle_between(CENTER, CENTER_RIGHT), 0.0)

################################################################################
## Testing distance_between
# Cardinal directions from center
assert_equal(distance_between(CENTER, TOP_RIGHT), math.sqrt(500000))
assert_equal(distance_between(CENTER, CENTER_TOP), 500.0)
assert_equal(distance_between(CENTER, TOP_LEFT), math.sqrt(500000))
assert_equal(distance_between(CENTER, CENTER_LEFT), 500.0)
assert_equal(distance_between(CENTER, ORIGIN), math.sqrt(500000))
assert_equal(distance_between(CENTER, CENTER_BOTTOM), 500.0)
assert_equal(distance_between(CENTER, BOTTOM_RIGHT), math.sqrt(500000))
assert_equal(distance_between(CENTER, CENTER_RIGHT), 500.0)
# And also some weirder angles
assert_equal(distance_between(CENTER_LEFT, BOTTOM_RIGHT), math.sqrt(1250000))
assert_equal(distance_between(ORIGIN, TOP_RIGHT), math.sqrt(2000000))
# And a classic Pythagorean Triple
assert_equal(distance_between(ORIGIN, {'x': 3, 'y': 4}), 5.0)

################################################################################
## Testing x_from_angle_speed
assert_equal(x_from_angle_speed(0, 5), 5.0)
assert_equal(x_from_angle_speed(math.pi/3, 5), 2.5)
assert_equal(x_from_angle_speed(math.pi/2, 5), 0.0)
assert_equal(x_from_angle_speed(2*math.pi/3, 5), -2.5)
assert_equal(x_from_angle_speed(math.pi, 5), -5.0)
assert_equal(x_from_angle_speed(-math.pi/3, 5), 2.5)
assert_equal(x_from_angle_speed(-math.pi/2, 5), 0.0)
assert_equal(x_from_angle_speed(-2*math.pi/3, 5), -2.5)

################################################################################
## Testing y_from_angle_speed
assert_equal(y_from_angle_speed(0, 5), 0.0)
assert_equal(y_from_angle_speed(math.pi/6, 5), 2.5)
assert_equal(y_from_angle_speed(math.pi/2, 5), 5.0)
assert_equal(y_from_angle_speed(5*math.pi/6, 5), 2.5)
assert_equal(y_from_angle_speed(math.pi, 5), 0.0)
assert_equal(y_from_angle_speed(-math.pi/6, 5), -2.5)
assert_equal(y_from_angle_speed(-math.pi/2, 5), -5.0)
assert_equal(y_from_angle_speed(-5*math.pi/6, 5), -2.5)

################################################################################
## Testing is_enemy_hitting_position
FIRST_POSITION = {'x': 50, 'y': 50}
SECOND_POSITION = {'x': 60, 'y': 60}
THIRD_POSITION = {'x': 70, 'y': 70}
assert_equal(is_enemy_hitting_position(FIRST_POSITION, FIRST_POSITION), True)
assert_equal(is_enemy_hitting_position(FIRST_POSITION, SECOND_POSITION), True)
assert_equal(is_enemy_hitting_position(FIRST_POSITION, THIRD_POSITION), True)
assert_equal(is_enemy_hitting_position(SECOND_POSITION, THIRD_POSITION), True)

################################################################################
## Testing check_contact_with_items

# player collides with item
ITEM = {'position': {'x': 500, 'y': 500}}
WORLD = {'pokemontrainer x' : 490, 'pokemontrainer y': 490, 'score': 0, 'items':[ITEM], 'win': None, 'running?': True}
# they are not colliding
ITEM2 = {'position': {'x': 550, 'y': 550}}
WORLD2 = {'pokemontrainer x' : 490, 'pokemontrainer y': 490, 'score': 0, 'items':[ITEM], 'win': None, 'running?': True}

# adds 1 to score
check_contact_with_items(WORLD, ITEM)
assert_equal(WORLD['score'], 1, WORLD['win'], True, WORLD['running?'], False)
# doesn't add to score
check_contact_with_items(WORLD2, ITEM2)
assert_equal(WORLD2['score'], 0)

################################################################################
## Testing check_contact_with_enemies

ENEMY = {'current':{'x': 500, 'y': 500}}
WORLD = {'pokemontrainer x' : 490, 'pokemontrainer y': 490, 'win': None, 'enemies':[ENEMY], 'running?': True}
# they are not colliding
ENEMY2 = {'current':{'x': 550, 'y': 550}}
WORLD2 = {'pokemontrainer x' : 490, 'pokemontrainer y': 490, 'win': None, 'enemies':[ENEMY], 'running?': True}

# sets win to false (you lose) and stops game
check_contact_with_enemies(WORLD, ENEMY)
assert_equal(WORLD['win'], False, WORLD['running?'], False)

# game is still running, and you haven't lost yet
check_contact_with_enemies(WORLD2, ENEMY2)
assert_equal(WORLD2['win'], None, WORLD2['running?'], True)

################################################################################
## Testing check_enemy_goal_reached
ORIGIN = {'x': 0, 'y': 0}
CENTER = {'x': WINDOW_WIDTH/2, 'y': WINDOW_HEIGHT/2}
CENTER_RIGHT = {'x': WINDOW_WIDTH, 'y': WINDOW_HEIGHT/2}
ENEMY_IN_PROGRESS = {'current': ORIGIN, 'goal': CENTER_RIGHT}
check_enemy_goal_reached(ENEMY_IN_PROGRESS)
assert_equal(ENEMY_IN_PROGRESS['current'] != ENEMY_IN_PROGRESS['goal'], True)
assert_equal(ENEMY_IN_PROGRESS['goal'], CENTER_RIGHT)
ENEMY_FINISHED = {'current': CENTER, 'goal': CENTER}
check_enemy_goal_reached(ENEMY_FINISHED)
assert_equal(ENEMY_IN_PROGRESS['current'] != ENEMY_IN_PROGRESS['goal'], True)
assert_equal(CENTER != ENEMY_IN_PROGRESS['goal'], True)

################################################################################
## Testing move_enemy
ORIGIN = {'x': 0, 'y': 0}
CENTER = {'x': WINDOW_WIDTH/2, 'y': WINDOW_HEIGHT/2}
CENTER_RIGHT = {'x': WINDOW_WIDTH, 'y': WINDOW_HEIGHT/2}
GOAL_POSITION = {'x': 3, 'y': 4}
ENEMY_SPEED = 1
ENEMY_IN_PROGRESS = {'current': ORIGIN, 'goal': GOAL_POSITION, 'speed': ENEMY_SPEED}
# game is currently running
WORLD = {'running?': True}
move_enemy(WORLD, ENEMY_IN_PROGRESS)
assert_equal(ENEMY_IN_PROGRESS['current']['x'], .6,1)
assert_equal(ENEMY_IN_PROGRESS['current']['y'], .8,1)
move_enemy(WORLD, ENEMY_IN_PROGRESS)
assert_equal(ENEMY_IN_PROGRESS['current']['x'], 1.2,1)
assert_equal(ENEMY_IN_PROGRESS['current']['y'], 1.6,1)
move_enemy(WORLD, ENEMY_IN_PROGRESS)
assert_equal(ENEMY_IN_PROGRESS['current']['x'], 1.8,1)
assert_equal(ENEMY_IN_PROGRESS['current']['y'], 2.4,1)
# game stops running, enemies stop moving
WORLD = {'running?': False}
move_enemy(WORLD, ENEMY_IN_PROGRESS)
assert_equal(ENEMY_IN_PROGRESS['current']['x'], 1.8,1)
assert_equal(ENEMY_IN_PROGRESS['current']['y'], 2.4,1)
move_enemy(WORLD, ENEMY_IN_PROGRESS)
assert_equal(ENEMY_IN_PROGRESS['current']['x'], 1.8,1)
assert_equal(ENEMY_IN_PROGRESS['current']['y'], 2.4,1)

################################################################################
## Testing update_world

ORIGIN = {'x': 0, 'y': 0}
ONE_STEP = {'x': 0.8944271909999159, 'y':0.4472135954999579}
CENTER = {'x': WINDOW_WIDTH/2, 'y': WINDOW_HEIGHT/2}
CENTER_RIGHT = {'x': WINDOW_WIDTH, 'y': WINDOW_HEIGHT/2}
ENEMY_SPEED = 1
ONE_ENEMY_WORLD = {'enemies': [{'current': ORIGIN, 'goal': CENTER_RIGHT,'speed': ENEMY_SPEED}], 'score': 0, 'moving?': True,
                   'direction': None, 'items': [{'position':{'x': 500, 'y': 500}}],'pokemontrainer x' : 490, 'pokemontrainer y': 490,
                   'running?': True}
update_world(ONE_ENEMY_WORLD)
assert_equal(ONE_ENEMY_WORLD['enemies'], [{'current': {'x': 0, 'y': 0} , 'goal': CENTER_RIGHT, 'speed': 1}])
ONE_ENEMY_WORLD['enemies'][0]['current'] = ONE_ENEMY_WORLD['enemies'][0]['goal']
update_world(ONE_ENEMY_WORLD)
assert_equal(ONE_ENEMY_WORLD['enemies'][0]['current'] != ONE_ENEMY_WORLD['enemies'][0]['goal'], True)

WORLD_UP = {'enemies': [{'current': ORIGIN, 'goal': CENTER_RIGHT,'speed': ENEMY_SPEED}], 'score': 0, 'moving?': True,
                   'direction': 'up', 'items': [{'position':{'x': 500, 'y': 500}}],'pokemontrainer x' : 490, 'pokemontrainer y': 490,
                   'running?': True}
update_world(WORLD_UP)
assert_equal(WORLD_UP, {'enemies': [{'current': ORIGIN, 'goal': CENTER_RIGHT,'speed': ENEMY_SPEED}], 'score': 1, 'moving?': True,
                   'direction': 'up', 'items': [],'pokemontrainer x' : 490, 'pokemontrainer y': 496,
                   'running?': False, 'win': True})
WORLD_DOWN= {'enemies': [{'current': ORIGIN, 'goal': CENTER_RIGHT,'speed': ENEMY_SPEED}], 'score': 0, 'moving?': True,
                   'direction': 'down', 'items': [{'position':{'x': 500, 'y': 500}}],'pokemontrainer x' : 490, 'pokemontrainer y': 490,
                   'running?': True}
update_world(WORLD_DOWN)
assert_equal(WORLD_DOWN, {'enemies': [{'current': ORIGIN, 'goal': CENTER_RIGHT,'speed': ENEMY_SPEED}], 'score': 1, 'moving?': True,
                   'direction': 'down', 'items': [],'pokemontrainer x' : 490, 'pokemontrainer y': 484,
                   'running?': False, 'win': True})
WORLD_RIGHT= {'enemies': [{'current': ORIGIN, 'goal': CENTER_RIGHT,'speed': ENEMY_SPEED}], 'score': 0, 'moving?': True,
                   'direction': 'right', 'items': [{'position':{'x': 500, 'y': 500}}],'pokemontrainer x' : 490, 'pokemontrainer y': 490,
                   'running?': True}
update_world(WORLD_RIGHT)
assert_equal(WORLD_RIGHT, {'enemies': [{'current': ORIGIN, 'goal': CENTER_RIGHT,'speed': ENEMY_SPEED}], 'score': 1, 'moving?': True,
                   'direction': 'right', 'items': [],'pokemontrainer x' : 496, 'pokemontrainer y': 490,
                   'running?': False, 'win': True})
WORLD_LEFT= {'enemies': [{'current': ORIGIN, 'goal': CENTER_RIGHT,'speed': ENEMY_SPEED}], 'score': 0, 'moving?': True,
                   'direction': 'left', 'items': [{'position':{'x': 500, 'y': 500}}],'pokemontrainer x' : 490, 'pokemontrainer y': 490,
                   'running?': True}
update_world(WORLD_LEFT)
assert_equal(WORLD_LEFT, {'enemies': [{'current': ORIGIN, 'goal': CENTER_RIGHT,'speed': ENEMY_SPEED}], 'score': 0, 'moving?': True,
                   'direction': 'left', 'items': [{'position':{'x': 500, 'y': 500}}],'pokemontrainer x' : 484, 'pokemontrainer y': 490,
                   'running?': True})

################################################################################
## Testing handle_key
W0 = {'running?': True,'moving?': False, 'direction': None}
handle_key(W0, arcade.key.UP)
assert_equal(W0, {'running?': True, 'moving?': True, 'direction': 'up'})
handle_key(W0, arcade.key.DOWN)
assert_equal(W0, {'running?': True, 'moving?': True, 'direction': 'down'})
handle_key(W0, arcade.key.LEFT)
assert_equal(W0, {'running?': True, 'moving?': True, 'direction': 'left'})
handle_key(W0, arcade.key.RIGHT)
assert_equal(W0, {'running?': True, 'moving?': True, 'direction': 'right'})
'''
W0['running?'] = False
handle_key(W0, arcade.key.UP)
assert_equal(W0, {'running?': False,'moving?': False, 'direction': None}
'''
################################################################################
## Testing handle_release

WORLD = {'moving?': True}
handle_release(WORLD, arcade.key.UP)
assert_equal(WORLD, {'moving?': False})
handle_release(WORLD, arcade.key.DOWN)
assert_equal(WORLD, {'moving?': False})
handle_release(WORLD, arcade.key.LEFT)
assert_equal(WORLD, {'moving?': False})
handle_release(WORLD, arcade.key.RIGHT)
assert_equal(WORLD, {'moving?': False})

