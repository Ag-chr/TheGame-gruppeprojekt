import pygame
import math
import time

from entityCollider import EntityCollider


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
                self.startTime = time.time()
                if time.time() > self.startTime + 1:
                    self.main.bullets.append(Bullet(self.main, self.player, self.angleFromPlayerToMouse, 3, self.distance, 1, self, 2, 2, "Levels/MainLevel_Collision enemy.csv", (2,2), 0, 0, 0, 0))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("Ikk smid med skrald, det kan blive din sidste fejl")

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
        self.image_rect = image_copy.get_rect()
        self.image_rect.x, self.image_rect.y = self.x - self.image_rect.w / 2, self.y - self.image_rect.h / 2
        canvas.blit(image_copy, self.image_rect)

    def getDegrees(self, num):
        num = math.degrees(num)
        if num < 0:
            num += 360
        return num


class Bullet(EntityCollider):
    def __init__(self, main, player, angle, speed, firingDistance, decay, gun, width, height, collisionMap, scanArea, x, y, xOffset, yOffset):
        EntityCollider.__init__(self, main, x, y, xOffset, yOffset, speed, width, height, collisionMap, scanArea)
        self.main = main
        self.player = player
        self.gun = gun
        self.angle = angle
        self.speed = speed * self.main.scale
        self.firingDistance = firingDistance
        self.decay = decay
        self.x = (self.gun.x)
        #+ self.gun.image_rect.w)
        self.y = (self.gun.y)
        #+ self.gun.image_rect.h)
        self.width = width * self.main.scale
        self.height = height * self.main.scale
        self.startTime = time.time()
        self.decayed = False



    def update(self):
        xScreen, yScreen = self.main.screen_region[0]
        wScreen, hScreen = self.main.screen_region[1]

        if xScreen > self.x or yScreen > self.y or wScreen + xScreen < self.x or hScreen + yScreen < self.y:
            self.decayed = True
            return
        self.xVel = math.cos(self.angle) * self.speed
        self.yVel = math.sin(self.angle) * self.speed
        xObstructed, yObstructed = self.checkCollision()
        if xObstructed or yObstructed:
            self.decayed = True




        self.x += self.xVel
        self.y += self.yVel


    def draw(self, canvas):
        if self.decayed == True:
            return
        pygame.draw.rect(canvas,(0, 0, 0),pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height))


    def skud(self, enemy):
        # tjek om bullet rammer fjenden
        bullet_rect = pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)
        enemy_rect = pygame.Rect(enemy.x + enemy.xOffset, enemy.y + enemy.yOffset, enemy.width, enemy.height)
        return bullet_rect.colliderect(enemy_rect)