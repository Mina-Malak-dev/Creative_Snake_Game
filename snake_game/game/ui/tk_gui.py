import tkinter as tk
from tkinter import ttk, messagebox
import time
from datetime import timedelta
#from ..core.snake import Snake
from game.core.snake import Snake
from ..core.food import Food
from ..core.level import LevelSystem
from ..db.scores import save_score, get_high_scores
from .player_window import PlayerWindow

class SnakeGameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Advanced Snake Game")
        self.player_id = None
        self.player_name = ""
        self.start_time = None
        self.game_active = False
        self.paused = False
        
        # Initialize key bindings
        self.bind_keys()
        
        self.show_player_selection()

    def bind_keys(self):
        self.master.bind("<Left>", lambda e: self.change_direction("LEFT"))
        self.master.bind("<Right>", lambda e: self.change_direction("RIGHT"))
        self.master.bind("<Up>", lambda e: self.change_direction("UP"))
        self.master.bind("<Down>", lambda e: self.change_direction("DOWN"))
        self.master.bind("<Escape>", lambda e: self.pause_game())

    def show_player_selection(self):
        if self.game_active:
            self.end_game()
            
        def start_callback(player_id, player_name):
            self.start_game(player_id, player_name)
            
        PlayerWindow(self.master, start_callback)

    def start_game(self, player_id, player_name):
        self.player_id = player_id
        self.player_name = player_name
        self.start_time = time.time()
        self.game_active = True
        self.paused = False
        
        # Clear previous game if exists
        if hasattr(self, 'canvas'):
            self.canvas.destroy()
        if hasattr(self, 'score_frame'):
            self.score_frame.destroy()
        
        # Game Setup
        self.canvas = tk.Canvas(self.master, width=600, height=400, bg="black")
        self.canvas.pack()
        
        # Score Display
        self.score_frame = ttk.Frame(self.master)
        self.score_frame.pack(fill=tk.X, pady=5)
        
        self.player_label = ttk.Label(
            self.score_frame,
            text=f"Player: {self.player_name}",
            font=('Arial', 10, 'bold'),
            width=20
        )
        self.player_label.pack(side=tk.LEFT, padx=10)
        
        self.score_label = ttk.Label(
            self.score_frame,
            text=f"Score: 0",
            font=('Arial', 10),
            width=15
        )
        self.score_label.pack(side=tk.LEFT)
        
        self.level_label = ttk.Label(
            self.score_frame,
            text=f"Level: 1",
            font=('Arial', 10),
            width=15
        )
        self.level_label.pack(side=tk.LEFT)
        
        self.time_label = ttk.Label(
            self.score_frame,
            text="Time: 00:00",
            font=('Arial', 10),
            width=15
        )
        self.time_label.pack(side=tk.RIGHT, padx=10)
        
        # Game Objects
        self.snake = Snake()
        self.food = Food(600, 400)
        self.level_system = LevelSystem()
        self.score = 0
        
        self.update()

    def change_direction(self, new_dir):
        if self.game_active and not self.paused:
            opposite_dirs = {"LEFT": "RIGHT", "RIGHT": "LEFT", "UP": "DOWN", "DOWN": "UP"}
            if self.snake.direction != opposite_dirs[new_dir]:
                self.snake.direction = new_dir

    def update(self):
        if not self.game_active or self.paused:
            return
            
        # Update time
        elapsed = int(time.time() - self.start_time)
        self.time_label.config(text=f"Time: {str(timedelta(seconds=elapsed)).split('.')[0]}")
        
        self.snake.move()
        
        # Check food collision
        if self.snake.body[0] == self.food.position:
            self.handle_food_collision()
        
        # Check game over
        if self.snake.check_collision(600, 400):
            self.game_over()
            return
        
        # Redraw
        self.draw_game()
        self.master.after(100, self.update)

    def handle_food_collision(self):
        if self.food.type == "normal":
            self.score += 10
            self.snake.grow()
        elif self.food.type == "bonus":
            self.score += 25
            self.snake.grow(2)
        elif self.food.type == "speed_boost":
            self.score += 15
            self.snake.speed = max(5, self.snake.speed - 2)
        
        self.food.spawn()
        if self.level_system.check_level_up(self.score):
            self.snake.speed = self.level_system.get_speed(15)
        
        self.score_label.config(text=f"Score: {self.score}")
        self.level_label.config(text=f"Level: {self.level_system.current_level}")

    def draw_game(self):
        self.canvas.delete("all")
        
        # Draw snake
        for segment in self.snake.body:
            self.canvas.create_rectangle(
                segment[0], segment[1], 
                segment[0]+10, segment[1]+10, 
                fill="green"
            )
        
        # Draw food
        food_color = self.food.get_color()
        self.canvas.create_oval(
            self.food.position[0], self.food.position[1], 
            self.food.position[0]+10, self.food.position[1]+10, 
            fill=food_color
        )

    def pause_game(self):
        if not self.game_active:
            return
            
        self.paused = not self.paused
        if self.paused:
            self.pause_time = time.time()
            self.canvas.create_text(
                300, 200, 
                text="PAUSED\nPress ESC to continue",
                fill="white",
                font=('Arial', 24),
                justify='center'
            )
        else:
            self.start_time += time.time() - self.pause_time
            self.update()

    def game_over(self):
        play_time = int(time.time() - self.start_time)
        save_score(self.player_id, self.score, self.level_system.current_level, play_time)
        
        # Game Over Display
        self.canvas.create_rectangle(50, 150, 550, 300, fill="black", outline="red", width=3)
        
        # Player info
        self.canvas.create_text(
            300, 180,
            text=f"Player: {self.player_name}",
            fill="white",
            font=('Arial', 14, 'bold')
        )
        
        # Score
        self.canvas.create_text(
            300, 210,
            text=f"Final Score: {self.score}",
            fill="gold",
            font=('Arial', 16, 'bold')
        )
        
        # Time
        time_str = str(timedelta(seconds=play_time)).split('.')[0]
        self.canvas.create_text(
            300, 240,
            text=f"Time Played: {time_str}",
            fill="cyan",
            font=('Arial', 12)
        )
        
        # Buttons
        btn_frame = ttk.Frame(self.canvas)
        self.canvas.create_window(300, 280, window=btn_frame)
        
        ttk.Button(
            btn_frame,
            text="Play Again",
            command=self.show_player_selection,
            style='Accent.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Exit",
            command=self.master.quit
        ).pack(side=tk.LEFT)
        
        self.game_active = False

    def end_game(self):
        if hasattr(self, 'canvas'):
            self.canvas.destroy()
        if hasattr(self, 'score_frame'):
            self.score_frame.destroy()
        self.game_active = False