import pygame
import math


class Slider:
    def __init__(self, x, y, width, height, min_value, max_value, default_value, label="", nonlinear=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_value = min_value
        self.max_value = max_value
        self.value = default_value
        self.label = label
        self.clicked = False  # Flag to indicate if the slider is being used
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.nonlinear = nonlinear  # Flag to determine if the slider is non-linear

    def round_to_nearest(self, value):
        if value < 10:
            return round(value)  # Round to the nearest integer
        else:
            exp = math.floor(math.log10(value))
            factor = 10 ** exp
            return round(value / factor) * factor  # Round to the nearest 1, 2, 5, or 10 * factor

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Check if left mouse button is pressed
                if self.rect.collidepoint(event.pos):  # Check if mouse is over the slider
                    self.clicked = True  # Set flag to True when slider is clicked

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.clicked = False  # Set flag to False when mouse button is released

        if self.clicked:  # If slider is clicked, update its value
            if event.type == pygame.MOUSEMOTION:
                mx, my = event.pos
                if self.x <= mx <= self.x + self.width:  # Check if mouse is over the horizontal slider
                    percent = (mx - self.x) / self.width

                    if self.nonlinear:
                        log_min = math.log10(self.min_value) if self.min_value > 0 else 0
                        log_max = math.log10(self.max_value)
                        log_value = log_min + percent * (log_max - log_min)
                        value = 10 ** log_value
                    else:
                        value = self.min_value + percent * (self.max_value - self.min_value)

                    self.value = self.round_to_nearest(value)

    def is_active(self):
        return self.clicked  # Return True if the slider is clicked (being used), False otherwise

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        pygame.draw.line(screen, (255, 255, 255), (self.x, self.y + self.height / 2), (self.x + self.width - 2, self.y + self.height / 2), 2)

        if self.nonlinear:
            log_min = math.log10(self.min_value) if self.min_value > 0 else 0
            log_max = math.log10(self.max_value)
            log_value = math.log10(self.value+1)
            percent = (log_value - log_min) / (log_max - log_min)
        else:
            percent = (self.value - self.min_value) / (self.max_value - self.min_value)

        pygame.draw.circle(screen, (255, 255, 255), (int(self.x + percent * self.width), int(self.y + self.height / 2)), 8)

        font = pygame.font.Font(None, 24)
        label_text = font.render(self.label, True, (255, 255, 255))
        screen.blit(label_text, (self.x, self.y - 20))

        value_text = font.render(str(self.value), True, (255, 255, 255))
        screen.blit(value_text, (self.x + self.width + 10, self.y))
