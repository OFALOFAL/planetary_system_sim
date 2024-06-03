from body import Body
import math
from debug import debug_print
from slider import Slider


class Simulation:
    def __init__(self, config):
        self.config = config
        self.old_simulation_speed = self.config.simulation_speed
        self.bodies = []
        self.init_bodies()

        self.speed_slider = Slider(
            config.screen_width - 440, 45,
            200, 15,
            0, 1_000_000,
            config.simulation_speed,
            "Simulation Speed",
        )

        self.sliders_m = []
        self.sliders_r = []

        for i, body in enumerate(self.bodies):
            self.sliders_m.append(Slider(
                20,
                45 * i + 45,
                200,
                15,
                0,
                1_000_000,
                body.mass,
                f"Body {i} mass",
                nonlinear=True
            ))

        for i, body in enumerate(self.bodies):
            self.sliders_r.append(Slider(
                20,
                len(self.bodies) * 45 + 45 * i + 90,
                200,
                15,
                0,
                500_000,
                body.radius,
                f"Body {i} radius"
            ))

        self.all_sliders = [*self.sliders_m, *self.sliders_r, self.speed_slider]

    def init_bodies(self):
        for body_conf in self.config.bodies:
            debug_print(f"Initializing body with: {body_conf}", self.config)
            body = Body(
                body_conf['x'],
                body_conf['y'],
                body_conf['radius'],
                body_conf['mass'],
                body_conf['color'],
                body_conf['vx'],
                body_conf['vy'],
                self.config,
                self.bodies[0] if self.bodies else None
            )
            self.bodies.append(body)

    def update(self):
        dt = self.config.time_step

        for body in self.bodies:
            if body.mass == 0:
                continue
            total_fx = total_fy = 0
            for other_body in self.bodies:
                if body == other_body or body.mass == 0:
                    continue

                dx = other_body.x - body.x
                dy = other_body.y - body.y
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance == 0:
                    continue
                force = self.config.G * body.mass * other_body.mass / distance ** 2
                fx = force * dx / distance
                fy = force * dy / distance

                total_fx += fx
                total_fy += fy

            body.apply_force(total_fx, total_fy)

        central_body = self.bodies[0]  # Assuming the first body is the central body (e.g., the Sun)
        for body in self.bodies:
            if body.mass != 0:
                body.update_position(dt, self.config.screen_offset)
                body.set_orbit_length(central_body)  # Update orbit length based on distance to central body

        self.handle_collisions()

    def handle_collisions(self):
        for i in range(len(self.bodies)):
            if self.bodies[i].mass == 0:
                continue
            for j in range(i + 1, len(self.bodies)):
                if self.bodies[j].mass == 0:
                    continue
                body1 = self.bodies[i]
                body2 = self.bodies[j]
                dx = body2.x - body1.x
                dy = body2.y - body1.y
                distance = math.sqrt(dx ** 2 + dy ** 2)
                min_distance = body1.radius + body2.radius
                if distance < min_distance:
                    # Calculate overlap
                    overlap = min_distance - distance
                    # Move the bodies apart
                    dx_unit = dx / distance
                    dy_unit = dy / distance
                    move_x = overlap * dx_unit / 2
                    move_y = overlap * dy_unit / 2
                    body1.x -= move_x
                    body1.y -= move_y
                    body2.x += move_x
                    body2.y += move_y

    def resolve_collision(self, body1, body2):
        # Simple elastic collision resolution
        # Conservation of momentum and kinetic energy
        total_mass = body1.mass + body2.mass
        vx1 = (body1.mass * body1.vx + body2.mass * body2.vx) / total_mass
        vy1 = (body1.mass * body1.vy + body2.mass * body2.vy) / total_mass
        vx2 = (2 * body1.mass * body1.vx - body2.mass * body2.vx) / total_mass
        vy2 = (2 * body1.mass * body1.vy - body2.mass * body2.vy) / total_mass
        body1.vx, body1.vy = vx1, vy1
        body2.vx, body2.vy = vx2, vy2

    def draw(self, screen, scale):
        for body in self.bodies:
            if body.mass != 0:
                body.draw(screen, scale, self.config.screen_offset)

        for slider in self.all_sliders:
            slider.draw(screen)
