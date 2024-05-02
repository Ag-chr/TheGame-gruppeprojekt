import pygame


class Button:

    def __init__(self, x, y, width, height, text, enabled, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.enabled = enabled
        self.color = color
        self.font = pygame.font.Font('freesansbold.ttf', 40)
    def draw(self, canvas):
        button_text = self.font.render(self.text, True, (0, 0, 0))
        button_rect = pygame.rect.Rect((self.x, self.y), (self.width, self.height))
        pygame.draw.rect(canvas, self.color, button_rect, 0, 0)
        canvas.blit(button_text, (self.width // 2 + self.x - 35, self.height // 2 + self.y - 20))

    def update(self):
        xMouse, yMouse = pygame.mouse.get_pos()
        mouse = pygame.Rect(xMouse, yMouse, 0, 0)  # bruges til når man skal tjekke om hvis mus er inde i button

    def checkInput(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame. BUTTON_LEFT:
                print("Click click")