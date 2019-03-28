# monster location for interaction with World
# TODO: better way of handling collision detection, look into https://www.pygame.org/docs/ref/rect.html#pygame.Rect.colliderect
#       speed should be influenced by carrying weight (add max carry_weight, based on str)
# TODO: not really sure about some of the functions here, specifically those relating to food,
#       might make more sense to make a separate behaviour class for food related behaviours?

import random
import pygame
import pyganim
import math
from monsters.miscellaneous.Activity_Level import Activity_Level


class World_Movement:

    def __init__(self, body, container):

        self.container = container
        self.body = body

        self.width = 48     # may keep this hardcoded
        self.height = 42    # may keep this hardcoded

        self.closest_food = None

        # creatures (x, y) hitbox coords
        # theres definitely a better way to do this but im keeping it like this for reasons ¯\_(ツ)_/¯
        self.x = (self.container.width - self.width) / 2
        self.y = (self.container.height - self.height) / 2

        self.x2 = self.x + self.width
        self.y2 = self.y

        self.x3 = self.x
        self.y3 = self.y + self.height

        self.x4 = self.x2
        self.y4 = self.y3

        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

        self.movement_speed_x = 10
        self.movement_speed_y = 10

        # randomize wandering x direction
        if random.random() > .5:
            self.movement_speed_x *= -1

        # randomize wandering x direction
        if random.random() > .5:
            self.movement_speed_y *= -1

        self.sleep_animation = pyganim.PygAnimation([('assets/slime/blue/sleep/0.png', 25),('assets/slime/blue/sleep/1.png', 25)])
        self.rest_animation = pyganim.PygAnimation([('assets/slime/blue/rest/0.png', 25),('assets/slime/blue/rest/1.png', 25)])
        self.idle_animation = pyganim.PygAnimation([('assets/slime/blue/idle/0.png', 25),('assets/slime/blue/idle/1.png', 25)])

# ----------------------------------------------------------------------------------------------------------------------
#   Movement Functions

    def move_to_food(self):

        x2 = self.closest_food.x
        y2 = self.closest_food.y

        if self.x is not x2:
            if self.x < x2:
                if self.movement_speed_x < 0:
                    self.movement_speed_x *= -1
            elif self.x > x2:
                if self.movement_speed_x > 0:
                    self.movement_speed_x *= -1
            self.x = self.x + self.movement_speed_x

        if self.y is not y2:
            if self.y < y2:
                if self.movement_speed_y < 0:
                    self.movement_speed_y *= -1
            elif self.y > y2:
                if self.movement_speed_y > 0:
                    self.movement_speed_y *= -1
            self.y = self.y + self.movement_speed_y

        self.update_hitbox()
        # self.display_hitbox()
        self.idle_animation.play()
        self.idle_animation.blit(self.container.surface, (self.x, self.y))

        if self.hitbox.colliderect(self.closest_food.hitbox):
            self.body.stomach.eat(self.closest_food)
            self.body.stomach.digest_food()

    def sleep_movement(self):
        # self.display_hitbox()
        self.sleep_animation.play()
        self.sleep_animation.blit(self.container.surface, (self.x, self.y))

    def rest_movement(self):
        # self.display_hitbox()
        self.rest_animation.play()
        self.rest_animation.blit(self.container.surface, (self.x, self.y))

    # slime idle movement behaviour
    def idle_movement(self):
        # chance used for movement chance
        x_chance_to_move = random.uniform(0, 1)
        y_chance_to_move = random.uniform(0, 1)

        # makes chance of creature's x changing on wander random
        if x_chance_to_move > 0.5:
            # reverse direction when close to Container x border
            if self.x2 >= self.container.width and self.movement_speed_x > 0:
                self.movement_speed_x = -self.movement_speed_x
            elif self.x <= 0 and self.movement_speed_x < 0:
                self.movement_speed_x = -self.movement_speed_x

            # change x in opposite direction 20% of the time
            if x_chance_to_move > .9:
                self.movement_speed_x = -self.movement_speed_x
            self.x = self.x + (self.movement_speed_x * random.uniform(0.5, 1))

        # makes chance of creature's y changing on wander random
        if y_chance_to_move > 0.5:
            # reverse direction when close to Container y border
            if self.y4 >= self.container.height and self.movement_speed_y > 0:
                self.movement_speed_y = -self.movement_speed_y
            elif self.y <= 0 and self.movement_speed_y < 0:
                self.movement_speed_y = -self.movement_speed_y

            # change y in opposite direction 20% of the time
            if y_chance_to_move > .9:
                self.movement_speed_y = -self.movement_speed_y
            self.y = self.y + (self.movement_speed_y * random.uniform(0.5, 1))

        self.update_hitbox()
        # self.display_hitbox()
        self.idle_animation.play()
        self.idle_animation.blit(self.container.surface, (self.x, self.y))

# ----------------------------------------------------------------------------------------------------------------------
#   Calculation Functions

    def get_closest_food(self):

        if len(self.container.food_container) > 0:
            self.closest_food = self.container.food_container[0]
            for food in self.container.food_container:
                if self.get_distance(self.closest_food) > self.get_distance(food):
                    self.closest_food = food
        else:
            self.closest_food = None

    # calculate and return distance between self and another object based on x,y coords (top left corner)
    def get_distance(self, other):

        x2 = other.x
        y2 = other.y
        return math.sqrt(math.pow((x2 - self.x), 2) + math.pow((y2 - self.y), 2))

    def search_for_food(self):

        self.get_closest_food()

        # return distance between two points

# ----------------------------------------------------------------------------------------------------------------------
#   Display Functions

    def display_closest_food(self):

        print("Closest Food: " + str(self.closest_food))
        if self.closest_food is not None:
            print("Distance: " + str(self.get_distance(self.closest_food)))

    def display_coordinates(self):
        print("W O R L D - M O V E M E N T")
        print("X-Coord: " + str(self.x))
        print("Y-Coord: " + str(self.y))

    def display_wandering_values(self):

        print("X-Wandering: " + str(self.movement_speed_x))
        print("Y-Wandering: " + str(self.movement_speed_y))

    def display_values(self):

        self.display_coordinates()
        self.display_wandering_values()

    def display_hitbox(self):

        pygame.draw.rect(self.container.surface, (25, 25, 25), self.hitbox, 1)
        # display_hitbox_corners()

    def display_hitbox_corners(self):

        pygame.draw.rect(self.container.surface, (255, 0, 0), [self.x, self.y, 2, 2], 4)
        pygame.draw.rect(self.container.surface, (0, 255, 0), [self.x2, self.y2, 2, 2], 4)
        pygame.draw.rect(self.container.surface, (0, 0, 255), [self.x3, self.y3, 2, 2], 4)
        pygame.draw.rect(self.container.surface, (50, 50, 50), [self.x4, self.y4, 2, 2], 4)

# ----------------------------------------------------------------------------------------------------------------------
#   Update Functions

    def update_hitbox(self):

        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def update_movement(self):

        if self.body.stomach.is_hungry:
            self.search_for_food()
            if self.closest_food is not None:
                self.body.stamina.activity_level = Activity_Level['Light']
                self.move_to_food()
        else:
            self.body.stamina.activity_level = Activity_Level['Idle']

        if self.body.stamina.activity_level.name == 'Sleep':
            self.sleep_movement()

        elif self.body.stamina.activity_level.name == 'Rest':
            self.rest_movement()

        elif self.body.stamina.activity_level.name == 'Idle':
            self.idle_movement()

        elif self.body.stamina.activity_level.name == 'Light':
            self.idle_animation.blit(self.container.surface, (self.x, self.y))

        elif self.body.stamina.activity_level.name == 'Moderate':
            self.idle_animation.blit(self.container.surface, (self.x, self.y))

        elif self.body.stamina.activity_level.name == 'Heavy':
            self.idle_animation.blit(self.container.surface, (self.x, self.y))

    # update 4 corners of hitbox, useful for collision detection later on
    def update_coords(self):

        self.x2 = self.x + self.width
        self.y2 = self.y

        self.x3 = self.x
        self.y3 = self.y + self.height

        self.x4 = self.x2
        self.y4 = self.y3

    def update(self):

        self.update_movement()
        self.update_coords()

