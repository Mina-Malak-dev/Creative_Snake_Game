class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.body = [(100, 100), (90, 100), (80, 100)]
        self.direction = "RIGHT"
        self.speed = 15
        self.growth_pending = 0

    def move(self):
        head = self.body[0]
        x, y = head
        
        if self.direction == "RIGHT": x += 10
        elif self.direction == "LEFT": x -= 10
        elif self.direction == "UP": y -= 10
        elif self.direction == "DOWN": y += 10

        self.body.insert(0, (x, y))
        
        if self.growth_pending > 0:
            self.growth_pending -= 1
        else:
            self.body.pop()

    def grow(self, amount=1):
        self.growth_pending += amount

    def check_collision(self, screen_width, screen_height):
        head = self.body[0]
        return (
            head[0] >= screen_width or head[0] < 0 or
            head[1] >= screen_height or head[1] < 0 or
            head in self.body[1:]
        )