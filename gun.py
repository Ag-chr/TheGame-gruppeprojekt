import pygame

class Gun:
    def __init__(self, main, player, image, distance):
        self.main = main
        self.player = player
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale_by(self.image, self.main.scale)
        self.distance = distance
        self.x = None
        self.y = None

    def checkInput(self):
        pass
        # tjekker hvis man trykker på venstre musse knap og derefter laver en skud klasse, der gemmes i et array i main

    def update(self):
        pass
        # få musets koordinater
        # find vinklen fra player til musets koordinater

        # regn koordinater ud for hvor gun image skal tegnes



    def draw_gun(self, canvas):
        pass
        # ud fra koordinater og vinkel tegn gun image

