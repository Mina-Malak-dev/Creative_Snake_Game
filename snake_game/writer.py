import tkinter as tk
from tkinter import ttk, messagebox
import keyboard
import time
import threading

class AutoTyperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Typer")
        self.root.geometry("600x500")
        
        # Variables
        self.countdown_var = tk.StringVar(value="5")
        self.speed_var = tk.StringVar(value="0.05")
        self.stay_on_top_var = tk.BooleanVar(value=True)
        self.running = False
        self.countdown_active = False
        
        # Set window to stay on top by default
        self.toggle_stay_on_top()
        
        # Create UI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Text input
        tk.Label(self.root, text="Text to Type:").pack(pady=(10, 0))
        self.text_input = tk.Text(self.root, height=10, wrap=tk.WORD)
        self.text_input.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Default text
        default_text = """Subject: Exclusive Property Opportunity

Dear Mr. Thompson,

I'm excited to present a stunning 5-bedroom oceanfront villa in Malibu from our portfolio. This 7,000 sq.ft. modern masterpiece boasts floor-to-ceiling windows, a private infinity pool, and a gourmet kitchen. With direct beach access and panoramic Pacific views, it's perfect for luxurious living or entertaining. Priced at $12.5M, this gem won't last long. Schedule a private tour today!

Best regards, [Your Name] Real Estate Agent"""
        self.text_input.insert("1.0", default_text)
        
        # Controls frame
        controls_frame = tk.Frame(self.root)
        controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Settings frame
        settings_frame = tk.Frame(controls_frame)
        settings_frame.grid(row=0, column=0, sticky="w")
        
        # Countdown setting
        tk.Label(settings_frame, text="Delay before start (seconds):").grid(row=0, column=0, sticky="w")
        self.countdown_entry = ttk.Entry(settings_frame, textvariable=self.countdown_var, width=5)
        self.countdown_entry.grid(row=0, column=1, sticky="w", padx=5)
        
        # Typing speed
        tk.Label(settings_frame, text="Typing speed (seconds per key):").grid(row=1, column=0, sticky="w")
        self.speed_entry = ttk.Entry(settings_frame, textvariable=self.speed_var, width=5)
        self.speed_entry.grid(row=1, column=1, sticky="w", padx=5)
        
        # Stay on top checkbox
        self.stay_on_top_cb = ttk.Checkbutton(
            settings_frame, 
            text="Stay on top", 
            variable=self.stay_on_top_var,
            command=self.toggle_stay_on_top
        )
        self.stay_on_top_cb.grid(row=2, column=0, columnspan=2, sticky="w", pady=(5,0))
        
        # Button frame
        button_frame = tk.Frame(controls_frame)
        button_frame.grid(row=0, column=1, sticky="e")
        
        # Start button
        self.start_button = ttk.Button(button_frame, text="Start Typing", command=self.start_typing)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        # Stop button
        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_typing, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT)
        
        # Status label
        self.status_label = tk.Label(self.root, text="Ready", fg="blue")
        self.status_label.pack(pady=5)
        
        # Countdown label
        self.countdown_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.countdown_label.pack(pady=5)
    
    def toggle_stay_on_top(self):
        """Toggle whether the window stays on top of others"""
        self.root.attributes('-topmost', self.stay_on_top_var.get())
    
    def start_typing(self):
        if self.running:
            return
            
        try:
            delay = float(self.countdown_var.get())
            speed = float(self.speed_var.get())
            text = self.text_input.get("1.0", tk.END).strip()
            
            if not text:
                messagebox.showwarning("Warning", "Please enter some text to type")
                return
                
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(text="Starting soon...", fg="orange")
            
            # Start typing in a separate thread
            threading.Thread(
                target=self.type_text,
                args=(text, delay, speed),
                daemon=True
            ).start()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for delay and speed")
            self.running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
    
    def stop_typing(self):
        self.running = False
        self.countdown_active = False
        self.status_label.config(text="Stopped", fg="red")
        self.countdown_label.config(text="")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    def type_text(self, text, delay, speed):
        self.countdown_active = True
        remaining_time = delay
        
        # Countdown
        while remaining_time > 0 and self.countdown_active:
            self.root.after(0, self.update_countdown, remaining_time)
            time.sleep(1)
            remaining_time -= 1
            
            if not self.running:
                self.root.after(0, self.stop_typing)
                return
        
        if not self.running:
            return
            
        self.root.after(0, self.update_countdown, "Typing...")
        
        # Type the text
        try:
            for char in text:
                if not self.running:
                    break
                    
                keyboard.write(char)
                time.sleep(speed)
                
            if self.running:
                self.root.after(0, lambda: self.status_label.config(text="Typing complete!", fg="green"))
                self.root.after(0, lambda: self.countdown_label.config(text=""))
        except Exception as e:
            self.root.after(0, lambda: self.status_label.config(text=f"Error: {str(e)}", fg="red"))
        
        self.running = False
        self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL))
        self.root.after(0, lambda: self.stop_button.config(state=tk.DISABLED))
    
    def update_countdown(self, text):
        self.countdown_label.config(text=str(text))

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoTyperApp(root)
    root.mainloop()

    