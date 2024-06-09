import pygame, csv, os
from getSpritesheets import playerSpritesheet
from collider import Collider
import math
from hjælpeFunktioner import read_csv, rectCollisionChecker, checkNearbyTiles
from entityCollider import EntityCollider


class Player(EntityCollider):
    def __init__(self, main, x, y, speed, collisionMap, scanArea):
        super().__init__(main=main, x=x, y=y, xOffset=3, yOffset=2, width=10, height=12, speed=speed, collisionMap=collisionMap, scanArea=scanArea)
        self.max_health = 100
        self.health = self.max_health
        self.respawning = False

        self.lastMove = "DOWN"
        self.vector_direction = [0, 0]

        self.player_img = playerSpritesheet.parse_sprite("character0.png")  # giver udsnit af sprite0 fra json fil
        self.player_img = pygame.transform.scale_by(self.player_img, self.main.scale)
        self.player_rect = self.player_img.get_rect()  # giver bredde og højde af sprite/player

    def checkInput(self, event):
        if self.respawning:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.yVel = -self.speed
            if event.key == pygame.K_s:
                self.yVel = self.speed
            if event.key == pygame.K_a:
                self.xVel = -self.speed
            if event.key == pygame.K_d:
                self.xVel = self.speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w and self.yVel == -self.speed:
                self.yVel = 0
            if event.key == pygame.K_s and self.yVel == self.speed:
                self.yVel = 0
            if event.key == pygame.K_a and self.xVel == -self.speed:
                self.xVel = 0
            if event.key == pygame.K_d and self.xVel == self.speed:
                self.xVel = 0

    def update(self):
        if self.respawning:
            return


        # bruger checkCollision fra fil entitycollider.py, som tjekker hvis
        xObstructed, yObstructed = self.checkCollision()

        # Tjekker hvis player bevæger sig mere end speed, som den gør når den går skråt. Derefter rettes det
        distanceMoved = math.sqrt(self.xVel ** 2 + self.yVel ** 2)
        amountToCorrect = 1
        if distanceMoved > self.speed:
            amountToCorrect = self.speed / distanceMoved

        # stopper player hvis collider er i vejen
        if not xObstructed:
            self.x += self.xVel * amountToCorrect
        if not yObstructed:
            self.y += self.yVel * amountToCorrect


    def getDirection(self):
        if self.xVel == 0 and self.yVel == 0:
            return tuple(self.vector_direction)
        self.vector_direction = [0, 0]
        if self.yVel < 0:
            self.lastMove = "UP"
            self.vector_direction[1] = -1
        elif self.yVel > 0:
            self.lastMove = "DOWN"
            self.vector_direction[1] = 1
        elif self.xVel < 0:
            self.lastMove = "LEFT"
            self.vector_direction[0] = -1
        elif self.xVel > 0:
            self.lastMove = "RIGHT"
            self.vector_direction[0] = 1
        return tuple(self.vector_direction)

    def draw_player(self, canvas):
        self.player_rect.x = self.x
        self.player_rect.y = self.y
        canvas.blit(self.player_img, self.player_rect)

        healthbar_width = 50
        healthbar_height = 10

        player_center_x = self.x + self.xOffset + self.width / 2

        healthbar_x = player_center_x - healthbar_width / 2

        # Beregner healthbaren
        health_width = (self.health / self.max_health) * healthbar_width

        # Tegner den grønne, røde og sorte outline
        pygame.draw.rect(canvas, (255, 0, 0), (healthbar_x, self.y - 20, healthbar_width, healthbar_height))
        pygame.draw.rect(canvas, (0, 128, 0), (healthbar_x, self.y - 20, health_width, healthbar_height))
        pygame.draw.rect(canvas, (0, 0, 0), (healthbar_x, self.y - 20, healthbar_width, healthbar_height), 1)

        self.hitbox = (self.x + 17, self.y + 4, self.width, self.height)

    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()

    def die(self):
        self.respawning = True
        pygame.time.set_timer(self.main.respawn_event, 3000)  # Sætter en timer til 3 sekunder for respawn

    def respawn(self):
        self.health = self.max_health
        self.x = (self.main.maps[0].map_w - self.width) / 2
        self.y = (self.main.maps[0].map_h - self.height) / 2
        self.respawning = False
        pygame.time.set_timer(self.main.respawn_event, 0)  # Slukker timeren (så den ikke kører et uendelig loop)
