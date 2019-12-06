import pygame, sys, os

class Player():
    def __init__(self,pos):
        self.pos = pos

class Star():
    def __init__(self,pos):
        self.pos = pos

class Selector():
    def __init__(self,pos):
        self.pos = pos

dir_path = os.path.dirname(os.path.abspath(__file__))

pygame.init()

game_map = [ [' ',' ',' ',' ',' ',' ',' '],
           ['x','#','#','#','#','x',' '],
           ['#','o','o','o','o','#','x'],
           ['#','o','o','o','o','o','#'],
           ['#','o','o','o','o','o','#'],
           ['#','o','o','o','o','o','#'],
           ['#','o','o','o','o','o','#'],
           ['x','#','#','#','#','o','x']]

game_map2 = [[' ',' ','#','#','#','#','#',' '],
            ['#','#','#','o','o','o','#',' '],
            ['#','o','o','o','o','o','#',' '],
            ['#','#','#','o','o','o','#',' '],
            ['#','o','#','#','o','o','#','#'],
            ['#','o','#','o','o','o','#','#'],
            ['#','o','o','o','o','o','o','#'],
            ['#','o','o','o','o','o','o','#'],
            ['#','#','#','#','#','#','#','#']]

maps = [game_map,game_map2]

TILE_WIDTH = 50
TILE_HEIGHT = 85
TILE_FLOOR_HEIGHT = 40
MAP_WIDTH = len(game_map[0])
MAP_HEIGHT = len(game_map)

IMAGES = {'star': pygame.image.load(dir_path+'/image/Star.png'),
              'selector': pygame.image.load(dir_path+'/image/Selector.png'),
              'corner': pygame.image.load(dir_path+'/image/Wall_Block_Tall.png'),
              'wall': pygame.image.load(dir_path+'/image/Wood_Block_Tall.png'),
              'inside floor': pygame.image.load(dir_path+'/image/Plain_Block.png'),
              'outside floor': pygame.image.load(dir_path+'/image/Grass_Block.png'),
              'boy': pygame.image.load(dir_path+'/image/boy.png'),
              'rock': pygame.image.load(dir_path+'/image/Rock1.png'),
              'solved': pygame.image.load(dir_path+'/image/star_solved.png'),
              'title': pygame.image.load(dir_path+'/image/star_title.png')
          }

TILE_DEFINITION = {'x': IMAGES['corner'],
               '#': IMAGES['wall'],
               'o': IMAGES['inside floor'],
               ' ': IMAGES['outside floor'],
               '1': IMAGES['rock'],
               }

def set_state():
    if level == 0:
        player = Player((5,4))
        selectors = [Selector((2,3)),Selector((2,4))]
        stars = [Star((4,2)),Star((4,4))]
    elif level == 1:
        player = Player((2,2))
        selectors = [Selector((2,1)),Selector((3,5)),Selector((4,1)),Selector((5,4)),Selector((6,3)),Selector((6,6)),Selector((7,4))]
        stars = [Star((2,3)),Star((3,4)),Star((4,4)),Star((6,1)),Star((6,3)),Star((6,4)),Star((6,5))]
    return player, selectors, stars

def draw_map(game_map, player, stars, selectors):
    """Draws the map to a Surface object, including the player's position"""

    # map_surf will be the single Surface object that the tiles are drawn on,
    # by doing so it is easy to position the entire map on the BASE_SURF object

    # First, the width and height must be calculated.    
    map_surf_w = MAP_WIDTH * TILE_WIDTH
    map_surf_h = (MAP_HEIGHT-1) * TILE_FLOOR_HEIGHT + TILE_HEIGHT
    map_surf = pygame.Surface((map_surf_w, map_surf_h))
    map_surf.fill((0, 170, 255)) # start with a blank color on the surface.

    # Draw the tile sprites onto this surface.
    for r in range(len(game_map)):
        for c in range(len(game_map[r])):
            space_rect = pygame.Rect((c * TILE_WIDTH, r * TILE_FLOOR_HEIGHT, TILE_WIDTH, TILE_HEIGHT))

            if game_map[r][c] in TILE_DEFINITION:
                base_tile = TILE_DEFINITION[game_map[r][c]]

            # First draw the base ground/wall tile.
            map_surf.blit(base_tile, space_rect)

            for item in selectors:
                if (r, c) == item.pos:
                    map_surf.blit(IMAGES['selector'], space_rect)

            for item in stars:
                if (r, c) == item.pos:
                    map_surf.blit(IMAGES['star'], space_rect)
                    
            # Last draw the player on the board.
            if (r, c) == player.pos:
                map_surf.blit(IMAGES['boy'], space_rect)

    return map_surf

def make_move(g_map, player, stars, move_to):
    offset = (0,0)

    if move_to == 'UP':
        offset = (-1,0)
    elif move_to == 'DOWN':
        offset = (1,0)
    elif move_to == 'LEFT':
        offset = (0,-1)
    elif move_to == 'RIGHT':
        offset = (0,1)

    # TODO: compute the position that the player want to move
    # TODO: check if that position is on the floor
    tmp_player_pos = (offset[0] + player.pos[0],offset[1] + player.pos[1])
    if tmp_player_pos[0] >= MAP_HEIGHT or tmp_player_pos[1] >= MAP_WIDTH or \
       tmp_player_pos[0] < 0 or tmp_player_pos[1] < 0 or \
       g_map[tmp_player_pos[0]][tmp_player_pos[1]] == '#' or \
       g_map[tmp_player_pos[0]][tmp_player_pos[1]] == 'x':
        return

    # TODO: check if there is a star on that position 
    # TODO: if the star can be pushed, push that star and move player to that position

    star_pos, has_star = move_star(offset, player, stars)
    
    if has_star is not -1:
        tmp_star_pos = (star_pos[0]+offset[0],star_pos[1]+offset[1])
        if tmp_star_pos[0] >= MAP_HEIGHT or tmp_star_pos[1] >= MAP_WIDTH or \
           tmp_star_pos[0] < 0 or tmp_star_pos[1] < 0 or \
           g_map[tmp_star_pos[0]][tmp_star_pos[1]] == '#' or \
           g_map[tmp_star_pos[0]][tmp_star_pos[1]] == 'x' or collide_star(tmp_star_pos, stars):
            return
        stars[has_star].pos = tmp_star_pos
            
    player.pos = tmp_player_pos

def collide_star(future_star_pos, stars) :
    for star in stars :
        if future_star_pos[0] == star.pos[0] and future_star_pos[1] == star.pos[1]:
            return True
        
    return False

def is_solved(selectors, stars):
    # TODO: check if the puzzle is solved
    for star in stars :
        in_selector = False
        for selector in selectors :
            if star.pos == selector.pos :
                in_selector = True

        if not in_selector : return False

    return True


def move_star(offset, player, stars) :
    star_pos = ()
    index, i = -1,0
    while i < len(stars) :
        if offset[0] + player.pos[0] == stars[i].pos[0] and offset[1] + player.pos[1] == stars[i].pos[1]:
            star_pos = (offset[0] + player.pos[0],offset[1] + player.pos[1])
            index = i
            return star_pos, index
        i+=1

    return (),index

level = 0
switch_scene =begin = True
BASE_SURF = pygame.display.set_mode((800, 600))
BASE_SURF.blit(IMAGES['solved'], (175,200))
fontObj = pygame.font.Font('freesansbold.ttf', 35)
player,selectors,stars= set_state()

while True:
    
    move_to = None
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT and not switch_scene:
                move_to = 'LEFT'
            if e.key == pygame.K_RIGHT and not switch_scene:
                move_to = 'RIGHT'
            if e.key == pygame.K_UP and not switch_scene:
                move_to = 'UP'
            if e.key == pygame.K_DOWN and not switch_scene:
                move_to = 'DOWN'
            if e.key == pygame.K_r and not switch_scene:
               player,selectors,stars= set_state()
            if e.key == pygame.K_a and switch_scene:
                if not begin:level +=1
                if level > 1: level = 0
                player,selectors,stars= set_state()
                switch_scene = False
                begin = False
    
    make_move(maps[level], player, stars, move_to)

    BASE_SURF.fill((0, 170, 255))
    
    map_surf = draw_map(maps[level], player, stars, selectors)  
    map_surf_rect = map_surf.get_rect()
    map_surf_rect.center = BASE_SURF.get_rect().center
    BASE_SURF.blit(map_surf, map_surf_rect)
    if begin :
        BASE_SURF.blit(IMAGES['title'], (175,200))

    # TODO: if the puzzle is solved, display a message to indicate user
    if is_solved(selectors, stars) :
        BASE_SURF.blit(IMAGES['solved'], (175,200))
        switch_scene = True
        
    # TODO: render a text to indicate user how to reset the game  
    textSurfaceObj = fontObj.render('R to reset the game', True, (255,255,255))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (800//2, 550)
    BASE_SURF.blit(textSurfaceObj, textRectObj)
    pygame.display.update()
