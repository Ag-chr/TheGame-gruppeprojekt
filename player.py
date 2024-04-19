import pygame
from spritesheetToJson import SpritesheetToJson
from spritesheet import Spritesheet


class Player:

    def __init__(self, main, drawPosX, drawPosY):
        self.main = main

        SpritesheetToJson("Images/character.png", self.main.tile_size, 16, (16, 16), (16, 16))
        self.player_spritesheet = Spritesheet("Images/character.png")

        self.player_img = self.player_spritesheet.parse_sprite("character0.png")
        self.player_img = pygame.transform.scale_by(self.player_img, self.main.scale)
        self.player_rect = self.player_img.get_rect()

        self.drawPosX = drawPosX
        self.drawPosY = drawPosY
        self.x = self.main.maps[0].map_w / 2 - self.player_rect.width / 2
        self.y = self.main.maps[0].map_h / 2 - self.player_rect.height / 2

        self.moveAmount = 2.5 * self.main.scale
        self.moveX = 0
        self.moveY = 0

    def checkInput(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.moveY = -self.moveAmount
            if event.key == pygame.K_s:
                self.moveY = self.moveAmount
            if event.key == pygame.K_a:
                self.moveX = -self.moveAmount
            if event.key == pygame.K_d:
                self.moveX = self.moveAmount

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                self.moveY = 0
            if event.key == pygame.K_a or event.key == pygame.K_d:
                self.moveX = 0

    def update(self):
        self.x += self.moveX
        self.y += self.moveY

    def draw_player(self, canvas):
        self.player_rect.x = self.x - self.player_rect.width / 2
        self.player_rect.y = self.y - self.player_rect.width / 2
        canvas.blit(self.player_img, self.player_rect)



