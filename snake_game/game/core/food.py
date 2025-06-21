import random

class Food:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.position = (0, 0)
        self.type = "normal"
        self.spawn()

    def spawn(self):
        self.position = (
            random.randint(1, (self.screen_width - 20) // 10) * 10,
            random.randint(1, (self.screen_height - 20) // 10) * 10
        )
        self.type = random.choices(
            ["normal", "bonus", "speed_boost"],
            weights=[0.7, 0.2, 0.1]
        )[0]

    def get_color(self):
        return {
            "normal": "red",
            "bonus": "gold",
            "speed_boost": "cyan"
        }[self.type]