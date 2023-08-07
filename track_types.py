import pygame

# track images
GRASS = pygame.image.load('./resources/images/grass.png')
HORIZONTAL_PATH = pygame.image.load('./resources/images/horizontal_path.png')
VERTICAL_PATH = pygame.image.load('./resources/images/vertical_path.png')
TOP_LEFT_CORNER = pygame.image.load('./resources/images/top_left_corner.png')
TOP_RIGHT_CORNER = pygame.image.load('./resources/images/top_right_corner.png')
BOTTOM_LEFT_CORNER = pygame.image.load('./resources/images/bottom_left_corner.png')
BOTTOM_RIGHT_CORNER = pygame.image.load('./resources/images/bottom_right_corner.png')
TRACK_TYPES = {
    0: GRASS,
    1: HORIZONTAL_PATH,
    2: VERTICAL_PATH,
    3: TOP_LEFT_CORNER,
    4: TOP_RIGHT_CORNER,
    5: BOTTOM_LEFT_CORNER,
    6: BOTTOM_RIGHT_CORNER
}

# track masks
GRASS_MASK = pygame.image.load('./resources/masks/grass_mask.png')
HORIZONTAL_PATH_MASK = pygame.image.load('./resources/masks/horizontal_path_mask.png')
VERTICAL_PATH_MASK = pygame.image.load('./resources/masks/vertical_path_mask.png')
TOP_LEFT_CORNER_MASK = pygame.image.load('./resources/masks/top_left_corner_mask.png')
TOP_RIGHT_CORNER_MASK = pygame.image.load('./resources/masks/top_right_corner_mask.png')
BOTTOM_LEFT_CORNER_MASK = pygame.image.load('./resources/masks/bottom_left_corner_mask.png')
BOTTOM_RIGHT_CORNER_MASK = pygame.image.load('./resources/masks/bottom_right_corner_mask.png')
TRACK_MASK_TYPES = {
    0: GRASS_MASK,
    1: HORIZONTAL_PATH_MASK,
    2: VERTICAL_PATH_MASK,
    3: TOP_LEFT_CORNER_MASK,
    4: TOP_RIGHT_CORNER_MASK,
    5: BOTTOM_LEFT_CORNER_MASK,
    6: BOTTOM_RIGHT_CORNER_MASK
}

# initialize track to given specs
def create_track(track, width, height, grid_size, mask=False):
    track_surface = pygame.Surface((width, height))
    for i in range(height // grid_size):
        for j in range(width // grid_size):
            if mask:
                track_surface.blit(TRACK_MASK_TYPES[track[i, j]], (j * grid_size, i * grid_size))
            else:
                track_surface.blit(TRACK_TYPES[track[i, j]], (j * grid_size, i * grid_size))
    return track_surface

# get checkpoints from around the track
def get_track_checkpoints(track, start, end):
    checkpoints = []
    next = start

    direction = None
    if start[0] - end[0] == 1:
        direction = 'right'
    elif start[0] - end[0] == -1:
        direction = 'left'
    elif start[1] - end[1] == 1:
        direction = 'down'
    elif start[1] - end[1] == -1:
        direction = 'up'

    started = False
    while next != start or not started:
        #print(next, start, started)
        started = True

        cp_type = track[next[1], next[0]]
        if cp_type == 0: # grass
            print('Error in track, found non track tile')
            return None
        elif cp_type == 1: # horizontal
            checkpoints.append(pygame.Rect(
                30 + 100 * next[0],
                10 + 100 * next[1],
                40,
                80
            ))
            if direction == 'right':
                direction = 'right'
                next = (next[0] + 1, next[1])
            elif direction == 'left':
                direction = 'left'
                next = (next[0] - 1, next[1])
        elif cp_type == 2: # vertical
            checkpoints.append(pygame.Rect(
                10 + 100 * next[0],
                30 + 100 * next[1],
                80,
                40
            ))
            if direction == 'down':
                direction = 'down'
                next = (next[0], next[1] + 1)
            elif direction == 'up':
                direction = 'up'
                next = (next[0], next[1] - 1)
        elif cp_type == 3: # top left corner
            checkpoints.append(pygame.Rect(
                10 + 100 * next[0],
                10 + 100 * next[1],
                54,
                54
            ))
            if direction == 'right':
                direction = 'up'
                next = (next[0], next[1] - 1)
            elif direction == 'down':
                direction = 'left'
                next = (next[0] - 1, next[1])
        elif cp_type == 4: # top right corner
            checkpoints.append(pygame.Rect(
                36 + 100 * next[0],
                10 + 100 * next[1],
                54,
                54
            ))
            if direction == 'left':
                direction = 'up'
                next = (next[0], next[1] - 1)
            elif direction == 'down':
                direction = 'right'
                next = (next[0] + 1, next[1])
        elif cp_type == 5: # bottom left corner
            checkpoints.append(pygame.Rect(
                10 + 100 * next[0],
                36 + 100 * next[1],
                54,
                54
            ))
            if direction == 'right':
                direction = 'down'
                next = (next[0], next[1] + 1)
            elif direction == 'up':
                direction = 'left'
                next = (next[0] - 1, next[1])
        elif cp_type == 6: # bottom right corner
            checkpoints.append(pygame.Rect(
                36 + 100 * next[0],
                36 + 100 * next[1],
                54,
                54
            ))
            if direction == 'left':
                direction = 'down'
                next = (next[0], next[1] + 1)
            elif direction == 'up':
                direction = 'right'
                next = (next[0] + 1, next[1])
    print(len(checkpoints))
    return checkpoints
