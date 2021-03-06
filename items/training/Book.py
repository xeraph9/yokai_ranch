from random import randint
import pygame


class Book:

    def __init__(self, Container, x, y):

        self._container = Container

        self.width = 34
        self.height = 28

        self.name = "Book"
        self.type = "Training Item"
        self.nutrition = 8
        self.weight = 2
        self.x = x
        self.y = y

        self.x_center = self.x + self.width / 2
        self.y_center = self.y + self.height / 2

        self.body = pygame.image.load("assets/items/book.png")
        self._container.surface.blit(self.body, (self.x,  self.y))

        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        # self.display_hitbox()

        self.is_edible = False
        self.is_destroyed = False

    def destroy(self):

        self.is_destroyed = True

    # ----------------------------------------------------------------------------------------------------------------------
    #   Display Functions

    def display_location(self):

        print("Location: (" + str(self.x_center) + ", " + str(self.y_center) + ")")

    def display_values(self):

        print("Name: " + str(self.name))
        print("Type: " + str(self.type))
        print("Nutrition: " + str(self.nutrition))
        self.display_location()
        print("Is Destroyed: " + str(self.is_destroyed))
        print("")

    def display_hitbox(self):

        pygame.draw.rect(self._container.surface, (25, 25, 25), self.hitbox, 1)

    # ----------------------------------------------------------------------------------------------------------------------
    #   Update Functions

    def update_position(self):

        self._container.surface.blit(self.body, (self.x, self.y))
        #self.display_hitbox

    def update(self):

        self.update_position()

