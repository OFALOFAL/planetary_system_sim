import pygame
from debug import debug_print
import math


class Body:
    orbit_max_length = 1000

    def __init__(self, x, y, radius, mass, color, vx, vy, config, central_body=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.color = color
        self.vx = vx
        self.vy = vy
        self.ax = 0
        self.ay = 0
        self.config = config
        self.orbit = []
        self.orbit_max_length = 50  # Maximum number of points in the orbit
        if central_body is None:
            self.distance = 0
        else:
            self.distance = math.sqrt((self.x - central_body.x) ** 2 + (self.y - central_body.y) ** 2)
        self.max_distance = self.distance

    def update_position(self, dt, screen_offset):
        self.vx += self.ax * dt
        self.vy += self.ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.update_orbit()
        debug_print(f"Updated position to: ({self.x}, {self.y}) with velocity ({self.vx}, {self.vy})", self.config)

    def update_orbit(self):
        self.orbit.append((self.x, self.y))
        while len(self.orbit) > self.orbit_max_length or len(self.orbit) > Body.orbit_max_length:
            self.orbit.pop(0)

    def apply_force(self, fx, fy):
        if self.mass == 0:
            self.ax = 0
            self.ay = 0
        else:
            self.ax = fx / self.mass
            self.ay = fy / self.mass
        debug_print(f"Applied force: ({fx}, {fy}) resulting in acceleration ({self.ax}, {self.ay})", self.config)

    def draw(self, screen, scale, screen_offset):
        screen_x = self.x + screen_offset[0]
        screen_y = self.y + screen_offset[1]
        center = (int(screen_x * scale + self.config.screen_width // 2), int(screen_y * scale + self.config.screen_height // 2))
        radius = int(self.radius * scale)
        pygame.draw.circle(screen, self.color, center, radius)

        # Draw orbit
        if len(self.orbit) > 1:
            orbit_points = [(int((x + screen_offset[0]) * scale + self.config.screen_width // 2),
                             int((y + screen_offset[1]) * scale + self.config.screen_height // 2)) for x, y in self.orbit]
            pygame.draw.lines(screen, self.color, False, orbit_points)

    def update_distance(self, central_body):
        self.distance = math.sqrt((self.x - central_body.x) ** 2 + (self.y - central_body.y) ** 2)
        self.max_distance = max(self.distance, self.max_distance)

    def set_orbit_length(self, central_body):
        self.update_distance(central_body)

        self.orbit_max_length = self.max_distance ** 2 / (self.config.simulation_speed * self.max_distance + 1) * self.max_distance / 25_000
        if self.orbit_max_length < 0:  # Ustaw minimalną wartość na 0
            self.orbit_max_length = 0
