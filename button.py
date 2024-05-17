import pygame
from hjælpeFunktioner import rectCollisionChecker

class Button:

    def __init__(self, x, y, width, height, text, enabled, color, function):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.enabled = enabled
        self.color = color
        self.font = pygame.font.Font('freesansbold.ttf', 40)
        self.function = function

    def draw(self, canvas):
        button_text = self.font.render(self.text, True, (0, 0, 0))
        button_rect = pygame.rect.Rect((self.x, self.y), (self.width, self.height))
        pygame.draw.rect(canvas, self.color, button_rect, 0, 10)
        pygame.draw.rect(canvas, (0, 0, 0), button_rect, 3, 10)
        canvas.blit(button_text, (self.width // 2 + self.x - 35, self.height // 2 + self.y - 20))

    def update(self, event):
        xMouse, yMouse = pygame.mouse.get_pos()
        mouse = pygame.Rect(xMouse, yMouse, 0, 0)  # bruges til når man skal tjekke om hvis mus er inde i button

        self.buttonClickZone = pygame.Rect(self.x, self.y, self.width, self.height)

        isXInButtonZone, isYInButtonZone = rectCollisionChecker(mouse, self.buttonClickZone)
        if isXInButtonZone and isYInButtonZone:
            self.checkInput(event)
    def checkInput(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame. BUTTON_LEFT:
                self.function()