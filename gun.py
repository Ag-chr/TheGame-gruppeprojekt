import pygame
import math

class Gun:
    def __init__(self, main, player, camera, image, distance):
        self.main = main
        self.player = player
        self.camera = camera
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale_by(self.image, self.main.scale)
        self.distance = distance * self.main.scale
        self.x = None
        self.y = None
        self.angleFromPlayerToMouse = None
        self.xPlayer = None
        self.yPlayer = None


    def checkInput(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                print("BANG")

    def update(self):
        # få musets koordinater
        xCamera, yCamera = self.camera.getCameraPos()
        xMouse, yMouse = pygame.mouse.get_pos()
        xMouse += xCamera
        yMouse += yCamera

        # find vinklen fra player til musets koordinater
        self.xPlayer = self.player.x + self.main.tile_size * self.main.scale / 2
        self.yPlayer = self.player.y + self.main.tile_size * self.main.scale / 2
        self.angleFromPlayerToMouse = math.atan2(yMouse - self.yPlayer, xMouse - self.xPlayer)

        # regn koordinater ud for hvor gun image skal tegnes
        self.x = math.cos(self.angleFromPlayerToMouse) * self.distance + self.xPlayer
        self.y = math.sin(self.angleFromPlayerToMouse) * self.distance + self.yPlayer

    def draw_gun(self, canvas):
        # ud fra koordinater og vinkel tegn gun image
        angle = abs(self.getDegrees(self.angleFromPlayerToMouse) - 360)
        image_copy = self.image.copy()

        if angle > 90 and angle < 270:
            angle += 180
            image_copy = pygame.transform.flip(image_copy, True, False)

        image_copy = pygame.transform.rotate(image_copy, angle)
        image_rect = image_copy.get_rect()
        image_rect.x, image_rect.y = self.x - image_rect.w / 2, self.y - image_rect.h / 2
        canvas.blit(image_copy, image_rect)

    def getDegrees(self, num):
        num = math.degrees(num)
        if num < 0:
            num += 360
        return num


