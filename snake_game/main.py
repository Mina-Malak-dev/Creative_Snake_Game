import argparse
import tkinter as tk
from tkinter import ttk
from game.ui.tk_gui import SnakeGameGUI

def main():
    parser = argparse.ArgumentParser(description="Advanced Snake Game")
    parser.add_argument("--cli", action="store_true", help="Run in command-line mode")
    args = parser.parse_args()

    if args.cli:
        from game.ui.cli import main as cli_main
        cli_main()
    else:
        root = tk.Tk()
        
        # Set theme
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Accent.TButton', foreground='white', background='#4a6984')
        
        game = SnakeGameGUI(root)
        root.mainloop()

if __name__ == "__main__":
    main()