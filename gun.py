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
        self.counter = 0
        self.ammo = 30
        self.timeStart = time.time()
        self.tick = time.time()

    def checkInput(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                if time.time() > self.tick + 0.06 and self.ammo > 0:
                    self.tick = time.time()
                    self.ammo -= 1
                    self.main.bullets.append(Bullet(self.main, self.angleFromPlayerToMouse, 3, 1, "Levels/MainLevel_Collision enemy.csv", self.xPlayer, self.yPlayer))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.ammo = 30
                self.tick = time.time() + 1

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

    def drawUI(self, canvas):
        font = pygame.font.Font('freesansbold.ttf', 45)
        text_surface = font.render(f"Ammo: {self.ammo}", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(30 * self.main.scale, 10 * self.main.scale))
        canvas.blit(text_surface, text_rect)


class Bullet(EntityCollider):
    def __init__(self, main, angle, speed, decay, collisionMap, x, y):
        super().__init__(main, speed, collisionMap, x, y, xOffset=0, yOffset=0, width=2, height=2, scanArea=(2,2))
        self.angle = angle
        self.decay = decay
        self.startTime = time.time()
        self.decayed = False
        self.show_ammo_text = True

        self.ammo_image = pygame.Surface((self.width, self.height))
        pygame.draw.rect(self.ammo_image, (0, 0, 0),pygame.Rect(0, 0, self.width, self.height))

    def update(self):
        if self.decayed:
            return

        if time.time() > self.startTime + 4:
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
        if self.decayed:
            return
        canvas.blit(self.ammo_image, (self.x - self.width/2, self.y - self.height/2))

    def skud(self, enemy):
        # tjek om bullet rammer fjenden
        bullet_rect = pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)
        enemy_rect = pygame.Rect(enemy.x + enemy.xOffset, enemy.y + enemy.yOffset, enemy.width, enemy.height)
        return bullet_rect.colliderect(enemy_rect)

