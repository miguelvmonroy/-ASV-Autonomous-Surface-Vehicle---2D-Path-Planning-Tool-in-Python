import math
import random
import tkinter as tk
from tkinter import font as tkfont

class Ammeter(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, bg='black', highlightthickness=0)
        self.max_current = 50
        self.target_current = 0
        self.display_current = 0.0

        self.bind("<Configure>", self.redibujar)
        self.after(16, self.animate_current)
        self.after(1000, self.set_new_target_current)

    def redibujar(self, event=None):
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()
        self.cx, self.cy = w // 2, h // 2
        self.radio = min(w, h) // 2.5

        self.create_oval(self.cx - self.radio, self.cy - self.radio,
                         self.cx + self.radio, self.cy + self.radio,
                         outline='gray', fill='#141414', width=2)

        self.create_current_marks()

        angle = 180 - (self.display_current / self.max_current) * 180
        x, y = self.polar_to_cartesian(self.cx, self.cy, self.radio * 0.75, angle)
        self.needle = self.create_line(self.cx, self.cy, x, y, fill='green', width=4)

        self.current_text = self.create_text(self.cx, self.cy + self.radio * 0.6,
                                             text=f"{int(self.display_current)} A",
                                             font=tkfont.Font(size=int(self.radio * 0.12), weight='bold'),
                                             fill='white')

    def create_current_marks(self):
        for i in range(0, self.max_current + 1, 5):
            angle = 180 - (i / self.max_current) * 180
            x1, y1 = self.polar_to_cartesian(self.cx, self.cy, self.radio * 0.85, angle)
            x2, y2 = self.polar_to_cartesian(self.cx, self.cy, self.radio * 1.0, angle)
            self.create_line(x1, y1, x2, y2, fill='white', width=2)

            xt, yt = self.polar_to_cartesian(self.cx, self.cy, self.radio * 0.7, angle)
            self.create_text(xt, yt, text=str(i),
                             font=tkfont.Font(size=int(self.radio * 0.08), weight='bold'),
                             fill='white')

    def polar_to_cartesian(self, cx, cy, radius, angle):
        rad = math.radians(angle)
        return cx + radius * math.cos(rad), cy - radius * math.sin(rad)

    def animate_current(self):
        speed = 0.1
        self.display_current += (self.target_current - self.display_current) * speed
        if hasattr(self, "needle"):
            angle = 180 - (self.display_current / self.max_current) * 180
            x, y = self.polar_to_cartesian(self.cx, self.cy, self.radio * 0.75, angle)
            self.coords(self.needle, self.cx, self.cy, x, y)
            self.itemconfig(self.current_text, text=f"{int(self.display_current)} A")
        self.after(16, self.animate_current)

    def set_new_target_current(self):
        self.target_current = random.randint(0, self.max_current)
        self.after(1000, self.set_new_target_current)
