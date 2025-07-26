import tkinter as tk
from tkinter import Canvas
import math
import random

class Voltmeter(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg='black')
        self.max_voltage = 250
        self.target_voltage = 0
        self.display_voltage = 0.0

        self.canvas = Canvas(self, bg='black', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.bind("<Configure>", self.redibujar)
        self.setup_timers()

    def redibujar(self, event):
        self.canvas.delete("all")
        w, h = event.width, event.height
        self.cx, self.cy = w // 2, h // 2
        self.radio = min(w, h) // 2.5

        self.canvas.create_oval(
            self.cx - self.radio, self.cy - self.radio,
            self.cx + self.radio, self.cy + self.radio,
            outline='gray', fill='#0f0f0f'
        )

        self.create_voltage_marks()
        angle = 180 - (self.display_voltage / self.max_voltage) * 180
        x, y = self.polar_to_cartesian(self.cx, self.cy, self.radio * 0.75, angle)
        self.needle = self.canvas.create_line(self.cx, self.cy, x, y, fill='cyan', width=3)

        self.voltage_text = self.canvas.create_text(
            self.cx, self.cy + self.radio * 0.6,
            text=f"{int(self.display_voltage)} V",
            font=('Arial', int(self.radio * 0.12), 'bold'),
            fill='white'
        )

    def create_voltage_marks(self):
        for i in range(0, self.max_voltage + 1, 50):
            angle = 180 - (i / self.max_voltage) * 180
            x1, y1 = self.polar_to_cartesian(self.cx, self.cy, self.radio * 0.85, angle)
            x2, y2 = self.polar_to_cartesian(self.cx, self.cy, self.radio * 1.0, angle)
            self.canvas.create_line(x1, y1, x2, y2, fill='white', width=2)

            xt, yt = self.polar_to_cartesian(self.cx, self.cy, self.radio * 0.7, angle)
            self.canvas.create_text(xt, yt, text=str(i), font=('Arial', int(self.radio * 0.08)), fill='white')

    def polar_to_cartesian(self, cx, cy, radius, angle):
        rad = math.radians(angle)
        x = cx + radius * math.cos(rad)
        y = cy - radius * math.sin(rad)
        return x, y

    def animate_voltage(self):
        speed = 0.08
        self.display_voltage += (self.target_voltage - self.display_voltage) * speed
        if hasattr(self, "needle"):
            angle = 180 - (self.display_voltage / self.max_voltage) * 180
            x, y = self.polar_to_cartesian(self.cx, self.cy, self.radio * 0.75, angle)
            self.canvas.coords(self.needle, self.cx, self.cy, x, y)
            self.canvas.itemconfig(self.voltage_text, text=f"{int(self.display_voltage)} V")
        self.after(16, self.animate_voltage)

    def set_new_target_voltage(self):
        self.target_voltage = random.randint(0, self.max_voltage)

    def setup_timers(self):
        self.animate_voltage()
        self.after(1000, self.update_voltage)

    def update_voltage(self):
        self.set_new_target_voltage()
        self.after(1000, self.update_voltage)
