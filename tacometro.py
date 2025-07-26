import tkinter as tk
from tkinter import Canvas, font as tkfont
import math
import random

class Speedometer(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg='black')
        self.speed = 0
        self.max_speed = 150

        self.canvas = Canvas(self, bg='black', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)

        self.canvas.bind("<Configure>", self.redibujar)

        self.after(500, self.update_speed)

    def redibujar(self, event=None):
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        self.cx, self.cy = w // 2, h // 2
        self.radio = min(w, h) // 2.5

        self.canvas.create_oval(
            self.cx - self.radio, self.cy - self.radio,
            self.cx + self.radio, self.cy + self.radio,
            fill='#1e1e1e', outline='white'
        )

        self.create_speed_marks()

        angle = 180 - (self.speed / self.max_speed) * 180
        x, y = self.polar_to_cartesian(self.cx, self.cy, self.radio * 0.75, angle)
        self.needle = self.canvas.create_line(self.cx, self.cy, x, y, fill='red', width=4)

        self.speed_text = self.canvas.create_text(
            self.cx, self.cy + self.radio * 0.6,
            text=f"{self.speed} RPM",
            font=tkfont.Font(size=int(self.radio * 0.12), weight='bold'),
            fill='white'
        )

    def create_speed_marks(self):
        for i in range(0, self.max_speed + 1, 20):
            angle = 180 - (i / self.max_speed) * 180
            x1, y1 = self.polar_to_cartesian(self.cx, self.cy, self.radio * 0.85, angle)
            x2, y2 = self.polar_to_cartesian(self.cx, self.cy, self.radio * 1.0, angle)
            self.canvas.create_line(x1, y1, x2, y2, fill='white', width=2)

            xt, yt = self.polar_to_cartesian(self.cx, self.cy, self.radio * 0.7, angle)
            self.canvas.create_text(xt, yt, text=str(i),
                                    font=tkfont.Font(size=int(self.radio * 0.08), weight='bold'),
                                    fill='white')

    def polar_to_cartesian(self, cx, cy, radius, angle):
        rad = math.radians(angle)
        return cx + radius * math.cos(rad), cy - radius * math.sin(rad)

    def update_speed(self):
        self.speed = random.randint(0, self.max_speed)
        if hasattr(self, "needle"):
            angle = 180 - (self.speed / self.max_speed) * 180
            x, y = self.polar_to_cartesian(self.cx, self.cy, self.radio * 0.75, angle)
            self.canvas.coords(self.needle, self.cx, self.cy, x, y)
            self.canvas.itemconfig(self.speed_text, text=f"{self.speed} RPM")
        self.after(500, self.update_speed)
