'''
Change log:
  - 0.0.1: Initial version
'''
__VERSION__ = '0.0.1'

import arcade, math, random
from cisc108_game import Cisc108Game

################################################################################
## Game Constants

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
BACKGROUND_COLOR = arcade.color.BLACK
GAME_TITLE = "Top Down Adventure!"

# Sizes of the enemy, sprite, and items

ENEMY_SIZE = 50
ENEMY_SPEED = 5

TRAINER_SIZE = 40
BACKGROUND_SIZE = 1000
POKEBALL_SIZE = 30

MOVE_SPEED = 6

# Load images
POKEMON_TRAINER = arcade.load_texture('pokemon_boy.png')
CHARIZARD = arcade.load_texture('charizard.png')
POKEBALL = arcade.load_texture('pokeball.png')
BACKGROUND = arcade.load_texture('woods.png')

################################################################################
## Record definitions

# A position is an X/Y coordinate pair.
Position = { 'x': float, 'y': float }

Item = {'position': Position}

Enemy = {
    # The Enemy's current drawn position
    'current': Position,
    # Where the Enemy is going towards
    'goal': Position,
    # The Enemy's current speed
    'speed': float
}
################################################################################
# Helper Functions

def get_random_position() -> Position:
    '''
    Produce a new random position (random X/Y coordinate) within the
    bounds of the window.
    
    Returns:
        Position: The new random position.
    '''
    return {
        'x': random.randint(0, WINDOW_WIDTH),
        'y': random.randint(0, WINDOW_HEIGHT)
    }

def make_item() -> Item:
    '''
    Produces a new Item with a random position
    
    Returns:
        Item: The new randomly generated item.
    '''
    return {
        'position': get_random_position(),
        }

def make_enemy() -> Enemy:
    '''
    Produces a new Enemy with a random current position and random
    goal position.
    
    Returns:
        Enemy: The new randomly generated Enemy.
    '''
    return {
        'current': get_random_position(),
        'goal': get_random_position(),
        'speed': ENEMY_SPEED
        }

def angle_between(p1: Position, p2: Position) -> float:
    '''
    Uses trigonometry to determine the angle (in radians) between
    two points. The result ranges from pi to -pi radians (which would be
    180 degrees and negative 180 degrees).
    
    Args:
        p1 (Position): The origin position
        p2 (Position): The target position
    Returns:
        float: The angle in radians between the origin and the target.
    '''
    return math.atan2(p2['y']-p1['y'], p2['x']-p1['x'])

def distance_between(p1: Position, p2: Position) -> float:
    '''
    Uses algebra to determine the distance between two points.
    
    Args:
        p1 (Position): The origin position
        p2 (Position): The target position
    Returns:
        float: The distance in pixels between the two points.
    '''
    return math.sqrt((p2['y']-p1['y'])**2+(p2['x']-p1['x'])**2)

def x_from_angle_speed(angle: float, speed: float) -> float:
    """
    Determines the new X-coordinate when you move `speed` pixels
    in the `angle` direction. The angle is in radians.
    
    Args:
        angle (float): The angle to move in radians.
        speed (float): The number of pixels to move in that direction.
    Returns:
        float: The horizontal distance traveled
    """
    return math.cos(angle) * speed

def y_from_angle_speed(angle: float, speed: float) -> float:
    """
    Determines the new Y-coordinate when you move `speed` pixels
    in the `angle` direction. The angle is in radians.
    
    Args:
        angle (float): The angle to move in radians.
        speed (float): The number of pixels to move in that direction.
    Returns:
        float: The vertical distance traveled
    """
    return math.sin(angle) * speed

def is_enemy_hitting_position(enemy: Position, position: Position) -> bool:
    '''
    Determine if the enemy's position is colliding with the given point.
    The enemy has a size (ENEMY_SIZE) that allows for some tolerance, so
    that the points don't have to be exactly on top of each other.
    
    Args:
        enemy (Position): The dog's position to be checking.
        position (Position): The position to be checking.
    Returns:
        bool: Whether the dog is hitting that position
    '''
    return distance_between(enemy, position) < ENEMY_SIZE

################################################################################
# World Definitions
World = {
    # Remember to explain each field!
    'x': int,
    'y': int,
    # Pokemon trainer's position
    'pokemontrainer x': int,
    'pokemontrainer y': int,
    # The score is how many items the player has collected.
    'score': int,
    # Items that the player needs to collect
    'items': [Item],
    # List of enemies
    'enemies': [Enemy],
    # whether or not the sprite is moving
    'moving?': bool,
    # direction that the sprite is moving
    'direction': str,
    # whether you win or not
    'win': bool,
    # if the game is running
    'running?': bool
}

INITIAL_WORLD = {
    # And update your INITIAL_WORLD accordingly!
    'x': int(WINDOW_WIDTH/2),
    'y': int(WINDOW_HEIGHT/2),
    # Start Mario in the middle of the screen
    'pokemontrainer x': int(WINDOW_WIDTH/2),
    'pokemontrainer y': int(WINDOW_HEIGHT/2),
    # start the score at zero because the player hasn't collected anything
    'score': 0,
    # five items that are needed to collect
    'items': [make_item(), make_item(), make_item(), make_item(), make_item()],
    # there are 5 enemies
    'enemies':[make_enemy(),make_enemy(),make_enemy(),make_enemy(),make_enemy()],
    # the character is not moving
    'moving?': False,
    # there is no direction since the character is not moving
    'direction': None,
    # currently you have not won or lost.
    'win': None,
    # the game is running
    'running?': True
}
################################################################################

def check_contact_with_items(world: World, item: Item):
    """
    Checks to see if the sprite comes into contact with items.
    Removes the item if the sprite is in contact. 
    Args:
        world (World): The current state of the world.
        item (Item): The item who's position we need to check.
    """
    if world['pokemontrainer x'] - item['position']['x'] < 15 and world['pokemontrainer x'] - item['position']['x'] > -15:
        if world['pokemontrainer y'] - item['position']['y'] < 22 and world['pokemontrainer y'] - item['position']['y'] > -22:
            world['score'] = world['score'] + 1
            # removes item
            world['items'].remove(item)
            # adds another randomly placed item
            world['items'].append(make_item())
    
def check_contact_with_enemies(world: World, enemy: Enemy) -> bool:
    """
    Checks to see if the sprite comes into contact with enemies.
    The game ends if the player comes into contact with an enemy
    Args:
        world (World): The current state of the world.
        enemy (Enemy): The item who's position we need to check.
    """
    if world['pokemontrainer x'] - enemy['current']['x'] < 15 and world['pokemontrainer x'] - enemy['current']['x'] > -15:
        if world['pokemontrainer y'] - enemy['current']['y'] < 22 and world['pokemontrainer y'] - enemy['current']['y'] > -22:
            # you lose the game
            world['win'] = False
            # the game stops running
            world['running?'] = False
            
################################################################################
# Drawing functions

def draw_items(item: Item):
    '''
    Draw the given item on screen.
    
    Args:
        item (Item): The item to draw
    '''
    arcade.draw_texture_rectangle(item['position']['x'], item['position']['y'],
                                  POKEBALL_SIZE, POKEBALL_SIZE, POKEBALL)

def draw_enemies(enemy: Enemy):
    '''
    Draw the given enemy on screen.
    
    Args:
        enemy(Enemy): The enemy to draw
    '''
    arcade.draw_texture_rectangle(enemy['current']['x'], enemy['current']['y'],
                                  ENEMY_SIZE, ENEMY_SIZE,
                                  CHARIZARD)
    
def draw_score(score: int):
    '''
    Draw the given score in the bottom-left corner.
    
    Args:
        score (int): The score to draw.
    '''
    arcade.draw_text('score: ' + str(score), 0, 0, arcade.color.WHITE, 50)

def draw_game_over(world: World):
    '''
    Draw the end screen
    
    Args:
        world (World): The current world to draw
    '''
    arcade.draw_text('GAME OVER!', world['x'] - 330, world['y'], arcade.color.WHITE, 100)
    arcade.draw_text('Your score was ' + str(world['score']), world['x'] - 215, world['y'] - 150, arcade.color.WHITE, 50)

def draw_world(world: World):
    """
    <Describe what is drawn in your world each time.>
    
    Args:
        world (World): The current world to draw
    """
    # draws the background
    arcade.draw_texture_rectangle(world['x'], world['y'],
                                 BACKGROUND_SIZE, BACKGROUND_SIZE,
                                 BACKGROUND)
    # draws the player's character
    arcade.draw_texture_rectangle(world['pokemontrainer x'], world['pokemontrainer y'],
                                  TRAINER_SIZE, TRAINER_SIZE,
                                  POKEMON_TRAINER)
    # draws items
    for item in world['items']:
        draw_items(item)
    # draws enemies  
    for enemy in world['enemies']:
        draw_enemies(enemy)
    # draws the score  
    draw_score(world['score'])
    # draw game over screen if enemy hits
    if world['win'] == False:
        draw_game_over(world)

################################################################################
# enemy manipulating functions

def check_enemy_goal_reached(enemy: Enemy):
    '''
    Tests whether the enemy has reached its goal; if so, it resets to a new
    goal position.
    
    Args:
        enemy (Enemy): The enemy to be testing and potentially updating.
    '''
    if is_enemy_hitting_position(enemy['current'], enemy['goal']):
        enemy['goal'] = get_random_position()

def move_enemy(world: World, enemy: Enemy):
    '''
    Moves the enemy towards its goal.
    
    Args:
        enemy (Enemy): The red dog to be moving.
        world (World): The current status of the world.
    '''
    if world['running?']:
        angle = angle_between(enemy['current'], enemy['goal'])
        enemy['current']['x'] += x_from_angle_speed(angle, enemy['speed'])
        enemy['current']['y'] += y_from_angle_speed(angle, enemy['speed'])
    
#################################################################################
# World manipulating functions

def update_world(world: World):
    """
    <Describe what happens every update.>
    
    Args:
        world (World): The current world to update.
    """
    # continuously moves while keyboard key is held down
    if world['moving?']:
        if world['direction'] == 'up':
            world['pokemontrainer y'] += MOVE_SPEED
        elif world['direction'] == 'down':
            world['pokemontrainer y'] -= MOVE_SPEED
        elif world['direction'] == 'right':
            world['pokemontrainer x'] += MOVE_SPEED
        elif world['direction'] == 'left':
            world['pokemontrainer x'] -= MOVE_SPEED
     
    # checks contact with items and enemies
    for item in world['items']:
        check_contact_with_items(world, item)
     # moves the enemy 
    for enemy in world['enemies']:
        move_enemy(world, enemy)
        check_enemy_goal_reached(enemy)
        check_contact_with_enemies(world, enemy)

def handle_key(world: World, key: int):
    """
    <Describe how your game responds to keyboard input.>
    
    Args:
        world (World): Current state of the world.
        key (int): The ASCII value of the pressed keyboard key (use ord and chr).
    """
    # controls movement
    # while key is held down, sets a direction and starts moving
    
    if world['running?']:
        if key == arcade.key.UP:
            world['moving?'] = True
            world['direction'] = "up"
        elif key == arcade.key.LEFT:
            world['moving?'] = True
            world['direction'] = "left"
        elif key == arcade.key.DOWN:
            world['moving?'] = True
            world['direction'] = "down"
        elif key == arcade.key.RIGHT:
            world['moving?'] = True
            world['direction'] = "right"

def handle_release(world: World, key: int):
    """
    <Describe how your game responds to releasing a keyboard key.>
    
    Args:
        world (World): Current state of the world.
        key (int): The ASCII value of the released keyboard key (use ord and chr).
    """
    # when a key is released, moving is set to false and the sprite stops moving.
    if key == arcade.key.UP:
        world['moving?'] = False
    elif key == arcade.key.LEFT:
        world['moving?'] = False
    elif key == arcade.key.DOWN:
        world['moving?'] = False
    elif key == arcade.key.RIGHT:
        world['moving?'] = False
        
def handle_mouse(world: World, x: int, y: int, button: str):
    """
    <Describe how your game responds to mouse clicks.>
    
    Args:
        world (World): Current state of the world.
        x (int): The x-coordinate of the mouse when the button was clicked.
        y (int): The y-coordinate of the mouse when the button was clicked.
        button (str): The button that was clicked ('left', 'right', 'middle')
    """

def handle_motion(world: World, x: int, y: int):
    """
    <Describe how your game responds to the mouse being moved.>
    
    Args:
        world (World): Current state of the world.
        x (int): The x-coordinate of where the mouse was moved to.
        y (int): The x-coordinate of where the mouse was moved to.
    """
    
############################################################################
# Set up the game
# Don't need to change any of this

if __name__ == '__main__':
    Cisc108Game(World, WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE, INITIAL_WORLD,
                draw_world, update_world, handle_key, handle_mouse,
                handle_motion, handle_release)
    arcade.set_background_color(BACKGROUND_COLOR)
    arcade.run()

