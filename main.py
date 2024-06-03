import pygame
from simulation import Simulation
from config import Config
from slider import Slider
from button import Button


def main():
    pygame.init()

    config = Config()
    screen = pygame.display.set_mode((config.screen_width, config.screen_height))
    pygame.display.set_caption("Planetary Simulation")

    clock = pygame.time.Clock()
    simulation = Simulation(config)

    dragging = False
    prev_mouse_pos = pygame.mouse.get_pos()

    font = pygame.font.Font(None, 36)
    reset_button = Button(
        config.screen_width - 140, 32,
        120, 40,
        "Reset", font,
        (70, 70, 70),
        (100, 100, 100)
    )

    running = True
    while running:
        for i, slider in enumerate(simulation.sliders_m):
            slider.value = int(simulation.bodies[i].mass)

        for i, slider in enumerate(simulation.sliders_r):
            slider.value = int(simulation.bodies[i].radius)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    config.scale *= 1.1  # Increase scale
                elif event.button == 5:  # Scroll down
                    config.scale /= 1.1  # Decrease scale
                elif event.button == 1:  # Left mouse button
                    dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    dragging = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    dragging = True

            if reset_button.is_clicked(event):
                config = Config()
                simulation = Simulation(config)
                simulation.speed_slider.value = config.simulation_speed

            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos != prev_mouse_pos and dragging and not any([x.is_active() for x in simulation.all_sliders]):
                config.screen_offset[0] += (mouse_pos[0] - prev_mouse_pos[0]) * (1/config.scale)
                config.screen_offset[1] += (mouse_pos[1] - prev_mouse_pos[1]) * (1/config.scale)

            prev_mouse_pos = mouse_pos

            for slider in simulation.all_sliders:
                slider.update(event)

        config.simulation_speed = int(simulation.speed_slider.value)

        for i, slider in enumerate(simulation.sliders_m):
            simulation.bodies[i].mass = slider.value

        for i, slider in enumerate(simulation.sliders_r):
            simulation.bodies[i].radius = slider.value

        config.time_step = 1 / config.fps * config.simulation_speed

        simulation.update()
        screen.fill((0, 0, 0))
        simulation.draw(screen, config.scale)  # Pass scale to draw method
        reset_button.draw(screen)

        pygame.display.flip()

        clock.tick(config.fps)

    pygame.quit()


if __name__ == "__main__":
    main()
