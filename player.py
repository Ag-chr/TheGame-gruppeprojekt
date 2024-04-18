import pygame
from spritesheetToJson import SpritesheetToJson
from spritesheet import Spritesheet


class Player:

    def __init__(self, main, drawPosX, drawPosY):
        self.main = main
        self.drawPosX = drawPosX
        self.drawPosY = drawPosY
        self.x = self.main.XOffset
        self.y = self.main.YOffset

        self.moveAmount = 2.5 * self.main.scale
        self.MoveX = 0
        self.MoveY = 0

        SpritesheetToJson("Images/character.png", self.main.tile_size, 16, (16, 16), (16, 16))
        self.player_spritesheet = Spritesheet("Images/character.png")

        self.player_img = self.player_spritesheet.parse_sprite("character0.png")
        self.player_img = pygame.transform.scale_by(self.player_img, self.main.scale)
        self.player_rect = self.player_img.get_rect()

    def checkInput(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.MoveY = -self.moveAmount
            if event.key == pygame.K_s:
                self.MoveY = self.moveAmount
            if event.key == pygame.K_a:
                self.MoveX = -self.moveAmount
            if event.key == pygame.K_d:
                self.MoveX = self.moveAmount

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                self.MoveY = 0
            if event.key == pygame.K_a or event.key == pygame.K_d:
                self.MoveX = 0

    def draw_player(self, canvas):
        self.player_rect.x = self.drawPosX + self.main.XOffset - self.player_rect.width / 2
        self.player_rect.y = self.drawPosY + self.main.YOffset - self.player_rect.width / 2
        canvas.blit(self.player_img, self.player_rect)



