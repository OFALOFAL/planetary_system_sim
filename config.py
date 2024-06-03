import json


class Config:
    def __init__(self, config_file='config.json'):
        with open(config_file, 'r') as file:
            data = json.load(file)

        self.screen_width = data['screen_width']
        self.screen_height = data['screen_height']
        self.fps = data['fps']
        self.simulation_speed = data['simulation_speed']
        self.time_step = 1 / self.fps * self.simulation_speed
        self.G = data['G']
        self.scale = data['scale']
        self.screen_offset = data['screen_offset']
        self.bodies = data['bodies']
        self.debug = data['debug']

        print(f"Configuration loaded: {self.bodies}")
