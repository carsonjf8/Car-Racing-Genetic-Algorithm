import math
import numpy as np
import pygame
import numpy as np

class Car:
    ACTIONS = {
        0: [1, 0], # FORWARD
        1: [1, -1], # LEFT
        2: [1, 1] # RIGHT
    }
    N_ACTIONS = len(ACTIONS)

    def __init__(self, x, y, width=10, height=20, color='blue', heading=0, speed=3, turning_speed=0.07):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.heading = heading
        self.speed = speed
        self.turning_speed = turning_speed
        self.image = pygame.image.load('./resources/images/car.png')
        self.mask = pygame.image.load('./resources/masks/car_mask.png')
        self.mask.set_colorkey((0, 0, 0))

    # analyze environment and take an action (move)
    def take_action(self, action_index):
        action_params = Car.ACTIONS[action_index]
        self.move(forward=action_params[0], turning=action_params[1])

    # draw itself to screen
    def draw(self, screen, draw_car=True, draw_outline=False):
        # rotate and draw car
        rotated_car = pygame.transform.rotate(self.image, -self.heading * 180 / math.pi)
        new_rect = rotated_car.get_rect(center=self.image.get_rect(topleft=(self.x, self.y)).center)
        if draw_car:
            screen.blit(rotated_car, new_rect)

        # draw outline
        if draw_outline:
            rotated_car_mask = pygame.transform.rotate(self.mask, -self.heading * 180 / math.pi)
            car_mask = pygame.mask.from_surface(rotated_car_mask)
            mask_rect = car_mask.get_rect(center=self.mask.get_rect(topleft=(self.x, self.y)).center)
            # bounding box of mask
            pygame.draw.rect(screen, 'green', mask_rect, width=1)
            car_outline = car_mask.outline()
            # outline of mask
            for pt in car_outline:
                pygame.draw.ellipse(screen, 'red', pygame.Rect(mask_rect.x + pt[0], mask_rect.y + pt[1], 1, 1))

    # move
    def move(self, forward=0, turning=0):
        self.heading += forward * (turning * self.turning_speed)
        if self.heading > 2 * math.pi:
            self.heading -= 2 * math.pi
        elif self.heading < -2 * math.pi:
            self.heading += 2 * math.pi
        self.x += forward * (math.cos(self.heading) * self.speed)
        self.y += forward * (math.sin(self.heading) * self.speed)

    # check for collision with track boundaries
    def collide(self, track_mask):
        rotated_car_mask = pygame.transform.rotate(self.mask, -self.heading * 180 / math.pi)
        car_mask = pygame.mask.from_surface(rotated_car_mask)
        car_mask_rect = car_mask.get_rect(center=self.mask.get_rect(topleft=(self.x, self.y)).center)
        offset = (int(car_mask_rect.x), int(car_mask_rect.y))
        poi = track_mask.overlap(car_mask, offset)
        return poi

    # check for collision with checkpoint
    def checkpoint_collision(self, checkpoint_rect):
        return checkpoint_rect.collidepoint(self.x + self.width / 2, self.y + self.height / 2)

    # obtain data from surroundings
    def sensor(self, track_mask, left_angle=-90, right_angle=90, step=15, max_depth=200, threshold=2, draw_rays=False, screen=None):
        observation = []

        # find dist of each ray to border
        for i in range(left_angle, right_angle + 1, step):
            angle = i * math.pi / 180
            low = 0
            high = max_depth
            dist = None
            # find distance in a binary search manner
            while dist == None:
                test_dist = (high + low) / 2
                # draw ray onto surface
                ray_surface = pygame.Surface((max_depth * 2, max_depth * 2))
                ray_surface.fill('black')
                ray_surface.set_colorkey((0, 0, 0))
                pygame.draw.line(
                    ray_surface, 'white',
                    (max_depth, max_depth),
                    (
                        max_depth + test_dist * math.cos(self.heading + angle),
                        max_depth + test_dist * math.sin(self.heading + angle)
                    )
                )
                # convert surface to mask
                ray_mask = pygame.mask.from_surface(ray_surface)
                offset = (int(self.x - max_depth), int(self.y - max_depth))
                # test if ray mask overlaps with track mask
                poi = track_mask.overlap(ray_mask, offset)
                # update high, low, and dist
                if poi:
                    high = test_dist
                else:
                    low = test_dist
                if high - low < threshold:
                    dist = test_dist
            # draw rays
            if draw_rays and screen:
                pt = (
                    self.x + dist * math.cos(self.heading + angle),
                    self.y + dist * math.sin(self.heading + angle)
                )
                pygame.draw.line(screen, 'white', (self.x, self.y), pt)

            # add observed distance to observation list
            observation.append(dist)
        
        return np.array(observation)
