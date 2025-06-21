import tkinter as tk
from tkinter import ttk, messagebox
from datetime import timedelta
from ..db.scores import get_players, add_player, get_player_stats

class PlayerWindow:
    def __init__(self, master, callback):
        self.master = master
        self.callback = callback
        
        self.window = tk.Toplevel(master)
        self.window.title("Player Selection")
        self.window.geometry("500x400")
        self.window.resizable(False, False)
        self.window.grab_set()
        
        self.create_widgets()
        self.load_players()

    def create_widgets(self):
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Existing Players
        existing_frame = ttk.LabelFrame(main_frame, text=" Existing Players ")
        existing_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.player_list = ttk.Treeview(
            existing_frame,
            columns=('name', 'play_time'),
            show='headings',
            height=5
        )
        self.player_list.heading('name', text='Name')
        self.player_list.heading('play_time', text='Play Time')
        self.player_list.column('name', width=150)
        self.player_list.column('play_time', width=100, anchor='center')
        self.player_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Button(
            existing_frame,
            text="Select Player",
            command=self.select_existing_player,
            style='Accent.TButton'
        ).pack(pady=5)
        
        # New Player
        new_frame = ttk.LabelFrame(main_frame, text=" New Player ")
        new_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(new_frame, text="Name:").pack(pady=(5, 0))
        self.name_entry = ttk.Entry(new_frame)
        self.name_entry.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(
            new_frame,
            text="Add Player",
            command=self.add_new_player,
            style='Accent.TButton'
        ).pack(pady=5)
        
        # Stats
        self.stats_frame = ttk.LabelFrame(main_frame, text=" Player Stats ")
        self.stats_frame.pack(fill=tk.BOTH, expand=True)
        
        self.stats_text = tk.Text(
            self.stats_frame,
            height=6,
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def load_players(self):
        for item in self.player_list.get_children():
            self.player_list.delete(item)
            
        players = get_players()
        if not players:
            self.player_list.insert('', 'end', values=("No players found", ""))
            self.player_list.config(selectmode='none')
        else:
            self.player_list.config(selectmode='browse')
            for player_id, name in players:
                self.player_list.insert('', 'end', values=(name, ""), tags=(player_id,))
            self.player_list.selection_set(self.player_list.get_children()[0])
            self.show_player_stats(self.player_list.selection()[0])

        self.player_list.bind('<<TreeviewSelect>>', self.on_player_select)

    def on_player_select(self, event):
        selected = self.player_list.selection()
        if selected:
            self.show_player_stats(selected[0])

    def show_player_stats(self, item_id):
        player_id = self.player_list.item(item_id, 'tags')[0]
        stats = get_player_stats(player_id)
        
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        
        if stats:
            stats_text = f"Name: {stats[0]}\n"
            stats_text += f"Total Play Time: {str(timedelta(seconds=stats[1]))}\n"
            stats_text += f"Games Played: {stats[2]}\n"
            stats_text += f"High Score: {stats[3]}\n"
            stats_text += f"Average Score: {int(stats[4]) if stats[4] else 0}"
            
            self.stats_text.insert(tk.END, stats_text)
        
        self.stats_text.config(state=tk.DISABLED)

    def select_existing_player(self):
        selected = self.player_list.selection()
        if not selected or "No players" in self.player_list.item(selected[0], 'values'):
            messagebox.showwarning("Warning", "Please select a valid player or add a new one")
            return
            
        player_id = self.player_list.item(selected[0], 'tags')[0]
        player_name = self.player_list.item(selected[0], 'values')[0]
        self.window.destroy()
        self.callback(player_id, player_name)

    def add_new_player(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Please enter a player name")
            return
            
        if len(name) > 20:
            messagebox.showwarning("Warning", "Name must be 20 characters or less")
            return
            
        player_id = add_player(name)
        self.window.destroy()
        self.callback(player_id, name)