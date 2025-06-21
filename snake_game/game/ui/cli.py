import curses
from ..db.scores import get_players, add_player, save_score
#from ..core.snake import Snake
from game.core.snake import Snake

from ..core.food import Food

class SnakeGameCLI:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.screen_height, self.screen_width = stdscr.getmaxyx()
        self.player_id = self.select_player()
        self.snake = Snake()
        self.food = Food(self.screen_width * 10, (self.screen_height - 2) * 10)
        self.score = 0
        curses.curs_set(0)
        self.game_loop()

    def select_player(self):
        while True:
            self.stdscr.clear()
            self.stdscr.border(0)
            self.stdscr.addstr(1, 2, "SELECT PLAYER:")
            
            players = get_players()
            for i, (player_id, name) in enumerate(players, 1):
                self.stdscr.addstr(i+2, 4, f"{i}. {name}")
            
            self.stdscr.addstr(len(players)+3, 4, "0. Add New Player")
            self.stdscr.addstr(len(players)+5, 4, "Selection: ")
            
            curses.echo()
            selection = self.stdscr.getstr(len(players)+5, 14).decode('utf-8')
            curses.noecho()
            
            if selection == "0":
                return self.add_new_player()
            elif selection.isdigit() and 0 < int(selection) <= len(players):
                return players[int(selection)-1][0]

    def add_new_player(self):
        self.stdscr.clear()
        self.stdscr.border(0)
        self.stdscr.addstr(1, 2, "CREATE NEW PLAYER")
        self.stdscr.addstr(3, 4, "Enter name: ")
        
        curses.echo()
        name = self.stdscr.getstr(3, 16).decode('utf-8')
        curses.noecho()
        
        if not name.strip():
            return self.select_player()
        
        return add_player(name[:20])  # Truncate to 20 chars

    def game_loop(self):
        while True:
            self.stdscr.clear()
            self.draw_border()
            self.draw_game()
            
            key = self.stdscr.getch()
            if key == curses.KEY_LEFT: self.snake.direction = "LEFT"
            elif key == curses.KEY_RIGHT: self.snake.direction = "RIGHT"
            elif key == curses.KEY_UP: self.snake.direction = "UP"
            elif key == curses.KEY_DOWN: self.snake.direction = "DOWN"
            elif key == ord('q'): break
            
            if self.check_collision():
                save_score(self.player_id, self.score, 1)
                self.game_over()
                break
            
            curses.napms(100)

    def draw_border(self):
        self.stdscr.border(0)
        self.stdscr.addstr(0, 2, f"Score: {self.score}")

    def draw_game(self):
        # Draw snake
        for y, x in self.snake.body:
            try:
                self.stdscr.addch(y // 10 + 1, x // 10 + 1, 'O')
            except curses.error:
                pass
        
        # Draw food
        fy, fx = self.food.position
        try:
            self.stdscr.addch(fy // 10 + 1, fx // 10 + 1, 'X')
        except curses.error:
            pass

    def check_collision(self):
        head = self.snake.body[0]
        return (
            head[0] >= (self.screen_width - 2) * 10 or
            head[0] < 0 or
            head[1] >= (self.screen_height - 4) * 10 or
            head[1] < 0 or
            head in self.snake.body[1:]
        )

    def game_over(self):
        self.stdscr.clear()
        self.stdscr.border(0)
        self.stdscr.addstr(self.screen_height//2 - 1, self.screen_width//2 - 5, "GAME OVER!")
        self.stdscr.addstr(self.screen_height//2 + 1, self.screen_width//2 - 8, f"Score: {self.score}")
        self.stdscr.addstr(self.screen_height//2 + 3, self.screen_width//2 - 10, "Play again? (y/n)")
        self.stdscr.refresh()
        
        if self.stdscr.getch() == ord('y'):
            self.__init__(self.stdscr)

def main():
    curses.wrapper(SnakeGameCLI)

if __name__ == "__main__":
    main()