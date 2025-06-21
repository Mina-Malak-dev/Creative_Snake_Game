class LevelSystem:
    def __init__(self):
        self.current_level = 1
        self.level_thresholds = [100 * (i**2) for i in range(1, 10)]

    def check_level_up(self, score):
        if self.current_level < len(self.level_thresholds):
            if score >= self.level_thresholds[self.current_level - 1]:
                self.current_level += 1
                return True
        return False

    def get_speed(self, base_speed):
        return base_speed + (self.current_level - 1) * 2